"""MediaPipe hand tracking adapter for legacy and Tasks APIs."""

from pathlib import Path
from shutil import copyfileobj
from tempfile import NamedTemporaryFile
from threading import Lock
from typing import Any, Optional, Sequence, Tuple
from urllib.request import urlopen

import cv2
import mediapipe as mp

from config import Config, CONFIG

Point = Tuple[float, float]
MODEL_URL = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
MODEL_DOWNLOAD_LOCK = Lock()
CONNECTIONS = (
    (0, 1), (1, 2), (2, 3), (3, 4),
    (0, 5), (5, 6), (6, 7), (7, 8),
    (5, 9), (9, 10), (10, 11), (11, 12),
    (9, 13), (13, 14), (14, 15), (15, 16),
    (13, 17), (17, 18), (18, 19), (19, 20), (0, 17),
)


def _load_model_asset(model_path: Path) -> bytes:
    with MODEL_DOWNLOAD_LOCK:
        if model_path.is_file() and model_path.stat().st_size > 0:
            return model_path.read_bytes()

        temporary_path = None
        try:
            model_path.parent.mkdir(parents=True, exist_ok=True)
            with NamedTemporaryFile(
                dir=model_path.parent,
                prefix=f".{model_path.name}.",
                suffix=".tmp",
                delete=False,
            ) as temporary_file:
                temporary_path = Path(temporary_file.name)
                with urlopen(MODEL_URL, timeout=30) as response:
                    copyfileobj(response, temporary_file)

            if temporary_path.stat().st_size == 0:
                raise ValueError("The downloaded model file is empty.")
            temporary_path.replace(model_path)
            return model_path.read_bytes()
        except Exception as error:
            if temporary_path is not None:
                temporary_path.unlink(missing_ok=True)
            raise RuntimeError(
                f"Unable to load the hand model at {model_path}. Check your network connection "
                f"or set HAND_MODEL_PATH to a valid model file. Model URL: {MODEL_URL}"
            ) from error


class HandTracker:
    def __init__(self, config: Config = CONFIG) -> None:
        self._config = config
        self._last_results: Any = None
        self._timestamp_ms = 0
        self._legacy = hasattr(mp, "solutions")
        if self._legacy:
            self._hands = mp.solutions.hands.Hands(
                static_image_mode=False,
                max_num_hands=config.max_num_hands,
                min_detection_confidence=config.min_detection_confidence,
                min_tracking_confidence=config.min_tracking_confidence,
            )
        else:
            from mediapipe.tasks.python import vision
            from mediapipe.tasks.python.core.base_options import BaseOptions

            model_path = Path(getattr(config, "hand_model_path", ".cache/hand_landmarker.task"))
            if not model_path.is_absolute():
                model_path = Path(__file__).resolve().parent / model_path
            options = vision.HandLandmarkerOptions(
                base_options=BaseOptions(model_asset_buffer=_load_model_asset(model_path)),
                running_mode=vision.RunningMode.VIDEO,
                num_hands=config.max_num_hands,
                min_hand_detection_confidence=config.min_detection_confidence,
                min_hand_presence_confidence=config.min_detection_confidence,
                min_tracking_confidence=config.min_tracking_confidence,
            )
            self._hands = vision.HandLandmarker.create_from_options(options)

    def process(self, frame_bgr: Any) -> Optional[Sequence[Point]]:
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        if self._legacy:
            results = self._hands.process(frame_rgb)
            self._last_results = results
            if not results.multi_hand_landmarks:
                return None
            height, width = frame_bgr.shape[:2]
            return tuple(
                (landmark.x * width, landmark.y * height)
                for landmark in results.multi_hand_landmarks[0].landmark
            )

        image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
        self._timestamp_ms += 33
        results = self._hands.detect_for_video(image, self._timestamp_ms)
        self._last_results = results
        if not results.hand_landmarks:
            return None
        height, width = frame_bgr.shape[:2]
        return tuple(
            (landmark.x * width, landmark.y * height)
            for landmark in results.hand_landmarks[0]
        )

    def draw(self, frame_bgr: Any) -> None:
        if self._last_results is None:
            return
        if self._legacy:
            for hand_landmarks in self._last_results.multi_hand_landmarks or []:
                mp.solutions.drawing_utils.draw_landmarks(
                    frame_bgr, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS
                )
            return
        height, width = frame_bgr.shape[:2]
        for hand_landmarks in self._last_results.hand_landmarks or []:
            points = [(int(point.x * width), int(point.y * height)) for point in hand_landmarks]
            for start, end in CONNECTIONS:
                cv2.line(frame_bgr, points[start], points[end], (70, 210, 140), 2)
            for point in points:
                cv2.circle(frame_bgr, point, 4, (20, 120, 255), -1)

    def close(self) -> None:
        self._hands.close()