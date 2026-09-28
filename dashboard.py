"""Real-time Streamlit interface for the VisionControl pipeline."""

from __future__ import annotations

import threading
import time
from collections import Counter
from dataclasses import dataclass, field
from typing import Any

import av
import cv2
import streamlit as st
from streamlit_webrtc import WebRtcMode, VideoProcessorBase, webrtc_streamer

from config import CONFIG
from controller import MouseController
from gesture_recognizer import Gesture, Recognition, classify_gesture
from hand_tracker import HandTracker


st.set_page_config(page_title="VisionControl", page_icon="✋", layout="wide")


@dataclass
class ProcessorStats:
    gesture: str = Gesture.NO_HAND.value
    control_enabled: bool = False
    frames: int = 0
    hands_detected: int = 0
    fps: float = 0.0
    history: list[str] = field(default_factory=list)


class VisionVideoProcessor(VideoProcessorBase):
    """Thread-safe real-time OpenCV, MediaPipe, and controller pipeline."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._tracker = HandTracker(CONFIG)
        self._controller = MouseController(CONFIG)
        self._controller.set_enabled(False)
        self._stats = ProcessorStats()
        self._last_frame_time = time.monotonic()

    def set_enabled(self, enabled: bool) -> None:
        with self._lock:
            self._controller.set_enabled(enabled)
            self._stats.control_enabled = enabled

    def snapshot(self) -> ProcessorStats:
        with self._lock:
            return ProcessorStats(
                gesture=self._stats.gesture,
                control_enabled=self._stats.control_enabled,
                frames=self._stats.frames,
                hands_detected=self._stats.hands_detected,
                fps=self._stats.fps,
                history=list(self._stats.history),
            )

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        image = frame.to_ndarray(format="bgr24")
        landmarks = self._tracker.process(image)
        recognition: Recognition = classify_gesture(landmarks, CONFIG)
        with self._lock:
            self._controller.update(recognition.gesture, recognition.fingertip, image.shape[1::-1])
            now = time.monotonic()
            elapsed = max(now - self._last_frame_time, 1e-6)
            self._last_frame_time = now
            self._stats.gesture = recognition.gesture.value
            self._stats.control_enabled = self._controller.enabled
            self._stats.frames += 1
            self._stats.hands_detected += int(landmarks is not None)
            self._stats.fps = 1.0 / elapsed
            self._stats.history = (self._stats.history + [recognition.gesture.value])[-30:]

        self._tracker.draw(image)
        cv2.rectangle(
            image,
            (int(image.shape[1] * CONFIG.active_zone_left), int(image.shape[0] * CONFIG.active_zone_top)),
            (int(image.shape[1] * CONFIG.active_zone_right), int(image.shape[0] * CONFIG.active_zone_bottom)),
            (55, 190, 125),
            2,
        )
        cv2.putText(image, f"Gesture: {recognition.gesture.value}", (20, 34), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (55, 220, 140), 2)
        cv2.putText(image, f"Control: {'ON' if self._controller.enabled else 'PAUSED'}", (20, 68), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)
        return av.VideoFrame.from_ndarray(image, format="bgr24")

    def __del__(self) -> None:
        tracker = getattr(self, "_tracker", None)
        if tracker is not None:
            tracker.close()


def render_styles() -> None:
    st.markdown(
        """
        <style>
        [data-testid="stAppViewContainer"] { background: #f4f7f5; }
        [data-testid="stHeader"] { background: transparent; }
        .brand { color: #12372a; font-family: Georgia, serif; font-size: 2.8rem; line-height: 1; }
        .eyebrow { color: #4f7565; font-size: .76rem; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; }
        .status { border-left: 4px solid #1f8a5b; background: #e3f2e9; color: #174b35; padding: .75rem 1rem; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def get_stats(ctx: Any) -> ProcessorStats:
    processor = getattr(ctx, "video_processor", None)
    if processor is None:
        return ProcessorStats()
    return processor.snapshot()


def render_status(ctx: Any) -> None:
    stats = get_stats(ctx)
    st.subheader("System status")
    label = "ENABLED" if stats.control_enabled else "PAUSED"
    st.markdown(f'<div class="status">Cursor control is <strong>{label}</strong></div>', unsafe_allow_html=True)
    first, second, third = st.columns(3)
    first.metric("Gesture", stats.gesture.title())
    second.metric("FPS", f"{stats.fps:.1f}")
    third.metric("Hands", stats.hands_detected)

    if stats.history:
        st.subheader("Gesture activity")
        st.bar_chart(Counter(stats.history))


def main() -> None:
    render_styles()
    st.markdown('<div class="eyebrow">Python · NumPy · OpenCV · MediaPipe</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand">VisionControl</div>', unsafe_allow_html=True)
    st.caption("Webcam → OpenCV → hand landmarks → gesture → computer action")

    with st.sidebar:
        st.subheader("Control settings")
        st.warning("Cursor control starts paused.")
        st.caption("Enable it only when your hand is visible and the active zone is clear.")

    ctx = webrtc_streamer(
        key="visioncontrol",
        mode=WebRtcMode.SENDRECV,
        video_processor_factory=VisionVideoProcessor,
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True,
    )

    if ctx.video_processor:
        with st.sidebar:
            enabled = st.toggle("Enable cursor control", value=ctx.video_processor.snapshot().control_enabled)
            ctx.video_processor.set_enabled(enabled)
        render_status(ctx)
    else:
        st.info("Start the camera above to begin real-time hand tracking.")

    st.subheader("Gesture map")
    st.dataframe(
        {
            "Gesture": ["Index finger", "Thumb + index pinch", "Index + middle", "Closed fist", "Open palm"],
            "Action": ["Move cursor", "Left click", "Right click", "Pause control", "Resume control"],
        },
        hide_index=True,
        use_container_width=True,
    )


if __name__ == "__main__":
    main()
