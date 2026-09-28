"""VisionControl application entry point."""

import time

import cv2

from config import CONFIG
from controller import MouseController
from gesture_recognizer import classify_gesture
from hand_tracker import HandTracker


def run() -> None:
    capture = cv2.VideoCapture(CONFIG.camera_index)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, CONFIG.frame_width)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, CONFIG.frame_height)
    if not capture.isOpened():
        raise RuntimeError("Unable to open the webcam. Check the camera index and permissions.")

    tracker = HandTracker(CONFIG)
    controller = MouseController(CONFIG)
    previous_time = time.monotonic()
    try:
        while True:
            success, frame = capture.read()
            if not success:
                continue
            landmarks = tracker.process(frame)
            recognition = classify_gesture(landmarks, CONFIG)
            controller.update(recognition.gesture, recognition.fingertip, frame.shape[1::-1])
            tracker.draw(frame)

            now = time.monotonic()
            fps = 1.0 / max(now - previous_time, 1e-6)
            previous_time = now
            cv2.putText(frame, f"Gesture: {recognition.gesture.value}", (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 220, 120), 2)
            cv2.putText(frame, f"Control: {'ENABLED' if controller.enabled else 'PAUSED'}  FPS: {fps:.1f}", (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)
            cv2.imshow("VisionControl", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        capture.release()
        tracker.close()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    try:
        run()
    except RuntimeError as error:
        print(f"VisionControl: {error}")