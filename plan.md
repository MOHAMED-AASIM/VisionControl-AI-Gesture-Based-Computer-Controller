# VisionControl Implementation Plan

## Project Goal

Build a local Python desktop utility that uses a standard webcam and a single hand to control mouse movement, left click, right click, pause, and resume through gestures.

## Scope for v1

### Included

- Real-time webcam capture at a target resolution of 960x540.
- Single-hand tracking with MediaPipe Hands.
- OpenCV debug window with camera feed, landmarks, gesture label, and control status.
- Gesture classification for:
  - Index finger extended: move cursor.
  - Thumb and index finger pinch: left click.
  - Index and middle fingers extended: right click.
  - Closed fist: pause or disable control.
  - Open palm: resume or enable control.
- Active-zone mapping from camera coordinates to screen coordinates.
- Cursor smoothing.
- Click cooldown/debouncing.
- PyAutoGUI corner failsafe left enabled.
- Clean exit on `Q`, including camera and MediaPipe cleanup.
- Centralized configuration for thresholds and tunable values.
- Unit-testable gesture recognition without I/O.
- Windows and macOS/Linux setup scripts.
- Pinned dependency manifest and README troubleshooting guidance.
- Fail-fast validation for unsupported non-ASCII project paths.

### Explicitly excluded from v1

- Keyboard replacement or text entry.
- Multi-hand gestures.
- Gesture remapping UI.
- Cloud services, accounts, telemetry, or persisted video/gesture data.
- Packaged installers.
- Mobile or tablet support.
- Voice control, eye tracking, scrolling, and air drawing.

## Proposed Structure

```text
VisionControl/
├── config.py
├── hand_tracker.py
├── gesture_recognizer.py
├── controller.py
├── main.py
├── requirements.txt
├── setup_windows.bat
├── setup_unix.sh
├── README.md
└── tests/
    ├── test_gesture_recognizer.py
    └── test_controller.py
```

## Implementation Phases

### Phase 1: Project foundation

- Add dependency manifest with compatible version pins for Python 3.9-3.12.
- Add the centralized configuration module.
- Add path validation with a clear error message for non-ASCII paths.
- Add setup scripts for Windows and macOS/Linux.
- Add initial README setup and permissions guidance.

### Phase 2: Vision pipeline

- Implement webcam capture and cleanup.
- Implement MediaPipe single-hand tracking.
- Convert normalized landmarks to pixel coordinates.
- Add debug landmark rendering.
- Handle no-hand and tracking-loss states without exceptions.

### Phase 3: Gesture recognition

- Implement pure geometry helpers for finger states, fingertip position, and pinch distance.
- Implement deterministic classification for the v1 gesture vocabulary.
- Return `unknown` when a pose does not meet the configured thresholds.
- Add unit tests for valid poses, ambiguous poses, pinch thresholds, and missing hands.

### Phase 4: Mouse controller

- Implement active-zone coordinate mapping.
- Implement configurable cursor smoothing.
- Implement pause/resume state transitions.
- Implement click cooldown for left and right clicks.
- Keep PyAutoGUI failsafe enabled.
- Ensure tracking loss cannot cause runaway cursor movement.
- Add focused controller tests with mocked OS effects.

### Phase 5: Orchestration and debug UI

- Connect tracker, recognizer, and controller in the frame loop.
- Render gesture, status, FPS, and active-zone information.
- Handle `Q` for clean shutdown.
- Show actionable startup and runtime errors.

### Phase 6: Verification and documentation

- Run unit tests and static checks.
- Perform manual tests for every gesture, pause/resume, tracking loss, and failsafe behavior.
- Verify setup scripts on the supported operating systems where available.
- Document lighting, camera placement, macOS permissions, and troubleshooting.
- Check the stated success metrics against a small manual test set.

## Acceptance Criteria

- A new user can follow README instructions to create an isolated environment and start the app.
- The app opens a webcam debug view and recognizes at most one hand.
- Cursor movement follows the index finger inside the active zone with visibly reduced jitter.
- Pinch and two-finger gestures trigger at most one click per cooldown interval.
- A fist stops cursor actions; an open palm resumes them.
- No-hand frames do not crash the app or move the cursor unexpectedly.
- `Q` releases the camera and exits cleanly.
- PyAutoGUI corner failsafe remains enabled.
- Gesture recognition tests run without a webcam or OS mouse access.
- Unsupported non-ASCII project paths fail with a clear setup message.
- No video, images, gesture data, accounts, or telemetry are written or sent by default.

## Review Gate

Implementation must not begin until this file and `implement.md` have been reviewed and approved. After approval, work should proceed phase by phase, validating each phase before starting the next one.

## Decisions Needed Before Implementation

- Confirm exact dependency versions after checking Python 3.9-3.12 compatibility.
- Confirm whether the project folder should use an ASCII-only name to satisfy the MediaPipe path constraint.
- Confirm the preferred test runner (`pytest` is proposed).
- Confirm whether manual OS-level testing will be performed on Windows only or also on macOS/Linux.
