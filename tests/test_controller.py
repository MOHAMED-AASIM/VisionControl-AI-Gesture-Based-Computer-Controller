from config import Config
from controller import MouseController
from gesture_recognizer import Gesture


def test_active_zone_mapping_and_smoothing():
    moves = []
    controller = MouseController(Config(smoothing_factor=1.0), lambda x, y: moves.append((x, y)), lambda **kwargs: None, (1000, 800))
    controller.update(Gesture.MOVE, (10, 10), (100, 100))
    assert moves == [(0.0, 0.0)]


def test_click_is_debounced():
    clicks = []
    now = [0.0]
    controller = MouseController(Config(click_cooldown_seconds=1.0), lambda *args: None, lambda **kwargs: clicks.append(kwargs["button"]), (1000, 800), lambda: now[0])
    controller.update(Gesture.LEFT_CLICK, None, (100, 100))
    controller.update(Gesture.LEFT_CLICK, None, (100, 100))
    now[0] = 1.1
    controller.update(Gesture.LEFT_CLICK, None, (100, 100))
    assert clicks == ["left", "left"]


def test_pause_blocks_movement_until_resume():
    moves = []
    controller = MouseController(Config(), lambda x, y: moves.append((x, y)), lambda **kwargs: None, (1000, 800))
    controller.update(Gesture.PAUSE, None, (100, 100))
    controller.update(Gesture.MOVE, (50, 50), (100, 100))
    assert moves == []
    controller.update(Gesture.RESUME, None, (100, 100))
    controller.update(Gesture.MOVE, (50, 50), (100, 100))
    assert moves == [(0.0, 0.0)]