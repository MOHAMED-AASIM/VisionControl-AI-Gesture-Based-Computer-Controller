"""Real-time Streamlit interface for the VisionControl pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from html import escape
import threading
import time
from typing import Any

import av
import cv2
import streamlit as st
from streamlit_webrtc import WebRtcMode, VideoProcessorBase, webrtc_streamer

from config import CONFIG, Config
from controller import MouseController
from gesture_recognizer import Gesture, Recognition, classify_gesture, distance
from hand_tracker import HandTracker
from styles import render_styles


st.set_page_config(page_title="VisionControl", page_icon="✋", layout="wide")


@dataclass
class ProcessorStats:
    gesture: str = Gesture.NO_HAND.value
    control_enabled: bool = False
    frames: int = 0
    hands_detected: int = 0
    fps: float = 0.0
    last_action: str = "Waiting for a gesture"
    history: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class DashboardSettings:
    smoothing_factor: float = CONFIG.smoothing_factor
    pinch_threshold_px: int = 35
    click_cooldown_seconds: float = CONFIG.click_cooldown_seconds
    active_zone_margin_px: int = 54
    show_landmarks: bool = True


class DashboardState:
    """Thread-safe settings and telemetry shared by Streamlit and the video worker."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._settings = DashboardSettings()
        self._stats = ProcessorStats()

    def settings_snapshot(self) -> DashboardSettings:
        with self._lock:
            return self._settings

    def update_settings(self, settings: DashboardSettings) -> None:
        with self._lock:
            self._settings = settings

    def stats_snapshot(self) -> ProcessorStats:
        with self._lock:
            return ProcessorStats(
                gesture=self._stats.gesture,
                control_enabled=self._stats.control_enabled,
                frames=self._stats.frames,
                hands_detected=self._stats.hands_detected,
                fps=self._stats.fps,
                last_action=self._stats.last_action,
                history=list(self._stats.history),
            )

    def update_control(self, enabled: bool) -> None:
        with self._lock:
            self._stats.control_enabled = enabled

    def update_frame(self, gesture: Gesture, enabled: bool, fps: float) -> None:
        action = {
            Gesture.MOVE: "Move cursor",
            Gesture.LEFT_CLICK: "Left click",
            Gesture.RIGHT_CLICK: "Right click",
            Gesture.PAUSE: "Pause control",
            Gesture.RESUME: "Resume control",
        }.get(gesture)
        with self._lock:
            self._stats.gesture = gesture.value
            self._stats.control_enabled = enabled
            self._stats.frames += 1
            self._stats.hands_detected += int(gesture != Gesture.NO_HAND)
            self._stats.fps = fps
            if action is not None:
                self._stats.last_action = action
            self._stats.history = (self._stats.history + [gesture.value])[-30:]


def runtime_config(settings: DashboardSettings, frame: Any, landmarks: Any) -> Config:
    height, width = frame.shape[:2]
    x_margin = min(settings.active_zone_margin_px / max(width, 1), 0.49)
    y_margin = min(settings.active_zone_margin_px / max(height, 1), 0.49)
    palm_width = distance(landmarks[0], landmarks[9]) if landmarks else 100.0
    pinch_ratio = settings.pinch_threshold_px / max(palm_width, 1.0)
    return replace(
        CONFIG,
        smoothing_factor=settings.smoothing_factor,
        pinch_distance_ratio=pinch_ratio,
        click_cooldown_seconds=settings.click_cooldown_seconds,
        active_zone_left=x_margin,
        active_zone_right=1.0 - x_margin,
        active_zone_top=y_margin,
        active_zone_bottom=1.0 - y_margin,
    )


class VisionVideoProcessor(VideoProcessorBase):
    """Thread-safe real-time OpenCV, MediaPipe, and controller pipeline."""

    def __init__(self, state: DashboardState) -> None:
        self._lock = threading.Lock()
        self._state = state
        self._tracker = HandTracker(CONFIG)
        self._controller = MouseController(CONFIG)
        self._controller.set_enabled(False)
        self._last_frame_time = time.monotonic()

    def set_enabled(self, enabled: bool) -> None:
        with self._lock:
            self._controller.set_enabled(enabled)
            self._state.update_control(enabled)

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        image = frame.to_ndarray(format="bgr24")
        settings = self._state.settings_snapshot()
        landmarks = self._tracker.process(image)
        config = runtime_config(settings, image, landmarks)
        recognition: Recognition = classify_gesture(landmarks, config)
        with self._lock:
            self._controller._config = config
            self._controller.update(recognition.gesture, recognition.fingertip, image.shape[1::-1])
            now = time.monotonic()
            elapsed = max(now - self._last_frame_time, 1e-6)
            self._last_frame_time = now
            enabled = self._controller.enabled
        self._state.update_frame(recognition.gesture, enabled, 1.0 / elapsed)

        if settings.show_landmarks:
            self._tracker.draw(image)
        cv2.rectangle(
            image,
            (int(image.shape[1] * config.active_zone_left), int(image.shape[0] * config.active_zone_top)),
            (int(image.shape[1] * config.active_zone_right), int(image.shape[0] * config.active_zone_bottom)),
            (0, 210, 255),
            2,
        )
        cv2.putText(image, f"Gesture: {recognition.gesture.value}", (20, 34), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (35, 211, 166), 2)
        cv2.putText(image, f"Control: {'ON' if self._controller.enabled else 'PAUSED'}", (20, 68), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)
        return av.VideoFrame.from_ndarray(image, format="bgr24")

    def __del__(self) -> None:
        tracker = getattr(self, "_tracker", None)
        if tracker is not None:
            tracker.close()


DEFAULT_WIDGETS = {
    "vc_smoothing": CONFIG.smoothing_factor,
    "vc_pinch_threshold": 35,
    "vc_click_cooldown": CONFIG.click_cooldown_seconds,
    "vc_zone_margin": 54,
    "vc_show_landmarks": True,
    "vc_control_enabled": False,
}


def reset_settings() -> None:
    for key, value in DEFAULT_WIDGETS.items():
        st.session_state[key] = value
    st.session_state["vc_control_touched"] = True


def mark_control_touched() -> None:
    st.session_state["vc_control_touched"] = True


def render_sidebar() -> tuple[DashboardSettings, bool]:
    for key, value in DEFAULT_WIDGETS.items():
        st.session_state.setdefault(key, value)

    with st.sidebar:
        st.markdown("## Settings")
        smoothing = st.slider(
            "Cursor smoothing",
            min_value=0.0,
            max_value=0.95,
            step=0.05,
            key="vc_smoothing",
            help="Higher values make cursor movement catch up more quickly.",
        )
        pinch_threshold = st.slider(
            "Pinch threshold",
            min_value=10,
            max_value=100,
            step=1,
            format="%d px",
            key="vc_pinch_threshold",
            help="Maximum thumb-to-index distance in frame pixels for a pinch click.",
        )
        click_cooldown = st.slider(
            "Click cooldown",
            min_value=0.1,
            max_value=1.5,
            step=0.1,
            format="%.1f s",
            key="vc_click_cooldown",
        )
        zone_margin = st.slider(
            "Active-zone margin",
            min_value=0,
            max_value=200,
            step=1,
            format="%d px",
            key="vc_zone_margin",
        )
        show_landmarks = st.toggle("Show landmarks", key="vc_show_landmarks")
        control_enabled = st.toggle(
            "Enable cursor control",
            key="vc_control_enabled",
            on_change=mark_control_touched,
            help="Keep this off until your hand is visible and the active zone is clear.",
        )
        st.button(
            "Reset to defaults",
            icon=":material/refresh:",
            on_click=reset_settings,
            width="stretch",
        )

        with st.expander("Help & troubleshooting", icon=":material/help:"):
            st.markdown(
                """
                - Use even lighting and keep your hand clearly visible.
                - Allow camera access in the browser's address-bar permissions, then restart the stream.
                - A closed fist pauses control; an open palm resumes it.
                - If MediaPipe reports a model-path error, an ASCII-only project path is a compatible fallback.
                """
            )

    settings = DashboardSettings(
        smoothing_factor=smoothing,
        pinch_threshold_px=pinch_threshold,
        click_cooldown_seconds=click_cooldown,
        active_zone_margin_px=zone_margin,
        show_landmarks=show_landmarks,
    )
    return settings, control_enabled


def render_header(stats: ProcessorStats) -> None:
    if stats.gesture == Gesture.NO_HAND.value:
        label, status_class = "No hand", "vc-status-no-hand"
    elif stats.control_enabled:
        label, status_class = "Control ON", "vc-status-on"
    else:
        label, status_class = "Paused", "vc-status-paused"

    title, status = st.columns([5, 1], vertical_alignment="center")
    with title:
        st.markdown('<div class="vc-eyebrow">Python · NumPy · OpenCV · MediaPipe</div>', unsafe_allow_html=True)
        st.markdown('<div class="vc-title">VisionControl</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="vc-subtitle">Webcam to hand landmarks to precise, gesture-driven control.</div>',
            unsafe_allow_html=True,
        )
    with status:
        st.markdown(
            f'<div class="vc-status-pill {status_class}">{escape(label)}</div>',
            unsafe_allow_html=True,
        )


def render_status_panel(stats: ProcessorStats) -> None:
    st.subheader("Live status")
    st.metric("Current gesture", stats.gesture.title(), border=True)
    st.metric("FPS", f"{stats.fps:.1f}", border=True)
    st.metric("Control state", "ON" if stats.control_enabled else "PAUSED", border=True)
    st.markdown(f"**Last action:** {escape(stats.last_action)}")


def render_gesture_cards(active_gesture: str) -> None:
    cards = (
        ("☝️", "Index finger", "Move cursor", Gesture.MOVE.value),
        ("🤏", "Thumb + index pinch", "Left click", Gesture.LEFT_CLICK.value),
        ("✌️", "Index + middle", "Right click", Gesture.RIGHT_CLICK.value),
        ("✊", "Closed fist", "Pause control", Gesture.PAUSE.value),
        ("🖐️", "Open palm", "Resume control", Gesture.RESUME.value),
    )
    markup = []
    for icon, name, action, gesture in cards:
        active_class = " is-active" if active_gesture == gesture else ""
        markup.append(
            f'<div class="vc-gesture-card{active_class}">'
            f'<div class="vc-gesture-icon">{icon}</div>'
            f'<div class="vc-gesture-name">{escape(name)}</div>'
            f'<div class="vc-gesture-action">{escape(action)}</div>'
            "</div>"
        )
    st.markdown('<div class="vc-gesture-grid">' + "".join(markup) + "</div>", unsafe_allow_html=True)


@st.fragment(run_every="1s")
def render_live_header(state: DashboardState) -> None:
    render_header(state.stats_snapshot())


@st.fragment(run_every="1s")
def render_live_status(state: DashboardState) -> None:
    render_status_panel(state.stats_snapshot())


@st.fragment(run_every="1s")
def render_live_gesture_cards(state: DashboardState) -> None:
    render_gesture_cards(state.stats_snapshot().gesture)


def main() -> None:
    render_styles()
    state = st.session_state.setdefault("visioncontrol_state", DashboardState())
    control_was_touched = st.session_state.pop("vc_control_touched", False)
    if not control_was_touched:
        st.session_state["vc_control_enabled"] = state.stats_snapshot().control_enabled
    settings, control_enabled = render_sidebar()
    state.update_settings(settings)

    render_live_header(state)
    main_column, status_column = st.columns([1.85, 1], gap="large")
    with main_column:
        with st.container(border=True):
            st.markdown('<div class="vc-section-label">Live camera</div>', unsafe_allow_html=True)
            camera_error = None
            try:
                ctx = webrtc_streamer(
                    key="visioncontrol",
                    mode=WebRtcMode.SENDRECV,
                    video_processor_factory=lambda: VisionVideoProcessor(state),
                    media_stream_constraints={"video": True, "audio": False},
                    async_processing=True,
                )
            except (OSError, RuntimeError) as error:
                ctx = None
                camera_error = str(error)

            if camera_error:
                st.error(f"Camera processing could not start: {camera_error}", icon=":material/error:")
            elif ctx is None or ctx.video_processor is None:
                st.info("Start the camera to begin hand tracking.", icon=":material/videocam:")
                st.caption("If the camera is blocked or in use, allow browser access or close other apps using it, then retry.")
            else:
                ctx.video_processor.set_enabled(control_enabled)
            st.markdown('<div class="vc-hint">Keep your hand inside the yellow zone.</div>', unsafe_allow_html=True)

    with status_column:
        render_live_status(state)

    st.markdown("### Gesture guide")
    st.caption("A closed fist pauses cursor control. An open palm resumes it.")
    render_live_gesture_cards(state)


if __name__ == "__main__":
    main()
