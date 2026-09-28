"""Pure landmark geometry and gesture classification."""

from dataclasses import dataclass
from enum import Enum
from math import hypot
from typing import Optional, Sequence, Tuple

from config import Config, CONFIG

Point = Tuple[float, float]


class Gesture(str, Enum):
    NO_HAND = "no hand"
    UNKNOWN = "unknown"
    MOVE = "move"
    LEFT_CLICK = "left click"
    RIGHT_CLICK = "right click"
    PAUSE = "pause"
    RESUME = "resume"


@dataclass(frozen=True)
class Recognition:
    gesture: Gesture
    fingertip: Optional[Point] = None
    pinch_distance: Optional[float] = None


def distance(first: Point, second: Point) -> float:
    return hypot(first[0] - second[0], first[1] - second[1])


def _finger_extended(landmarks: Sequence[Point], tip: int, pip: int, config: Config, wrist: int = 0) -> bool:
    return distance(landmarks[tip], landmarks[wrist]) > distance(landmarks[pip], landmarks[wrist]) * config.finger_extension_ratio


def _fingers_extended(landmarks: Sequence[Point], config: Config) -> Tuple[bool, bool, bool, bool]:
    return (
        _finger_extended(landmarks, 8, 6, config),
        _finger_extended(landmarks, 12, 10, config),
        _finger_extended(landmarks, 16, 14, config),
        _finger_extended(landmarks, 20, 18, config),
    )


def classify_gesture(landmarks: Optional[Sequence[Point]], config: Config = CONFIG) -> Recognition:
    """Classify one 21-point hand landmark set without side effects."""
    if not landmarks or len(landmarks) < 21:
        return Recognition(Gesture.NO_HAND)

    index_tip = landmarks[8]
    pinch_distance = distance(landmarks[4], index_tip) / max(distance(landmarks[0], landmarks[9]), 1e-6)
    index_extended, middle_extended, ring_extended, pinky_extended = _fingers_extended(landmarks, config)
    pinch = pinch_distance <= config.pinch_distance_ratio
    all_extended = index_extended and middle_extended and ring_extended and pinky_extended
    fist = not index_extended and not middle_extended and not ring_extended and not pinky_extended

    if all_extended:
        return Recognition(Gesture.RESUME, index_tip, pinch_distance)
    if fist:
        return Recognition(Gesture.PAUSE, index_tip, pinch_distance)
    if pinch and index_extended:
        return Recognition(Gesture.LEFT_CLICK, index_tip, pinch_distance)
    if index_extended and middle_extended and not ring_extended and not pinky_extended:
        return Recognition(Gesture.RIGHT_CLICK, index_tip, pinch_distance)
    if index_extended and not middle_extended and not ring_extended and not pinky_extended:
        return Recognition(Gesture.MOVE, index_tip, pinch_distance)
    return Recognition(Gesture.UNKNOWN, index_tip, pinch_distance)