"""Central configuration for VisionControl."""

from dataclasses import dataclass
import os

from dotenv import load_dotenv


load_dotenv()


def _env_int(name: str, default: int) -> int:
    return int(os.getenv(name, default))


def _env_float(name: str, default: float) -> float:
    return float(os.getenv(name, default))


@dataclass(frozen=True)
class Config:
    camera_index: int = _env_int("CAMERA_INDEX", 0)
    hand_model_path: str = os.getenv("HAND_MODEL_PATH", ".cache/hand_landmarker.task")
    frame_width: int = _env_int("FRAME_WIDTH", 960)
    frame_height: int = _env_int("FRAME_HEIGHT", 540)
    camera_fps: int = _env_int("CAMERA_FPS", 30)
    max_num_hands: int = _env_int("MAX_NUM_HANDS", 1)
    min_detection_confidence: float = _env_float("MIN_DETECTION_CONFIDENCE", 0.7)
    min_tracking_confidence: float = _env_float("MIN_TRACKING_CONFIDENCE", 0.7)
    pinch_distance_ratio: float = _env_float("PINCH_DISTANCE_RATIO", 0.35)
    finger_extension_ratio: float = _env_float("FINGER_EXTENSION_RATIO", 1.15)
    active_zone_left: float = _env_float("ACTIVE_ZONE_LEFT", 0.1)
    active_zone_right: float = _env_float("ACTIVE_ZONE_RIGHT", 0.9)
    active_zone_top: float = _env_float("ACTIVE_ZONE_TOP", 0.1)
    active_zone_bottom: float = _env_float("ACTIVE_ZONE_BOTTOM", 0.9)
    smoothing_factor: float = _env_float("SMOOTHING_FACTOR", 0.35)
    click_cooldown_seconds: float = _env_float("CLICK_COOLDOWN_SECONDS", 0.6)


CONFIG = Config()