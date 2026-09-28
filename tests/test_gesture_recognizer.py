from config import Config
from gesture_recognizer import Gesture, classify_gesture


def landmarks(*extended):
    points = [(0.0, 0.0)] * 21
    for tip, pip in ((8, 6), (12, 10), (16, 14), (20, 18)):
        points[pip] = (0.0, 1.0)
        points[tip] = (0.0, 3.0 if tip in extended else 1.1)
    points[9] = (1.0, 0.0)
    points[4] = (0.0, 0.1)
    points[8] = (0.0, 3.0 if 8 in extended else 1.1)
    return points


def test_missing_hand_is_safe():
    assert classify_gesture(None).gesture == Gesture.NO_HAND


def test_index_finger_moves():
    assert classify_gesture(landmarks(8)).gesture == Gesture.MOVE


def test_two_fingers_right_click():
    assert classify_gesture(landmarks(8, 12)).gesture == Gesture.RIGHT_CLICK


def test_fist_pauses():
    assert classify_gesture(landmarks()).gesture == Gesture.PAUSE


def test_open_palm_resumes():
    assert classify_gesture(landmarks(8, 12, 16, 20)).gesture == Gesture.RESUME


def test_custom_extension_threshold_is_used():
    config = Config(finger_extension_ratio=2.0)
    assert classify_gesture(landmarks(8), config).gesture == Gesture.PAUSE