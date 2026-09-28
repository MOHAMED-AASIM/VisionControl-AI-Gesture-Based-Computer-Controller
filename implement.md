# VisionControl Implementation Checklist

This checklist is the execution companion to `plan.md`. It is intentionally prepared before implementation so the work can be reviewed and approved as a complete scope.

## Status Legend

- `[ ]` Not started
- `[-]` In progress
- `[x]` Complete
- `[!]` Blocked or needs a decision

## Review Gate

- [ ] User reviewed `plan.md`.
- [ ] User reviewed `implement.md`.
- [ ] User approved implementation to begin.
- [ ] Open decisions in `plan.md` are resolved or explicitly accepted.

## Phase 1: Foundation

- [x] Create the Python project structure.
- [x] Add `requirements.txt` with pinned compatible versions.
- [x] Add `config.py` as the single source for thresholds and tunables.
- [x] Add non-ASCII path validation.
- [x] Add `setup_windows.bat`.
- [x] Add `setup_unix.sh`.
- [x] Add initial `README.md`.
- [x] Verify setup scripts fail clearly when the project path is unsupported.

## Phase 2: Hand Tracking

- [x] Implement `hand_tracker.py`.
- [x] Configure MediaPipe for one hand only.
- [x] Convert normalized landmarks to pixel coordinates.
- [x] Handle camera-open failure clearly.
- [x] Handle missing hands and tracking loss safely.
- [x] Render hand landmarks in the debug frame.

## Phase 3: Gesture Recognition

- [x] Implement pure landmark geometry helpers.
- [x] Implement index-finger movement classification.
- [x] Implement pinch left-click classification.
- [x] Implement index-plus-middle right-click classification.
- [x] Implement fist pause classification.
- [x] Implement open-palm resume classification.
- [x] Implement `unknown` and no-hand states.
- [x] Add unit tests for normal and boundary threshold cases.

## Phase 4: Mouse Controller

- [x] Implement `controller.py`.
- [x] Map the configured active zone to screen coordinates.
- [x] Add cursor smoothing.
- [x] Add click cooldown/debouncing.
- [x] Add enabled/paused state handling.
- [x] Keep PyAutoGUI failsafe enabled.
- [x] Prevent cursor movement during no-hand and paused states.
- [x] Add mocked controller tests.

## Phase 5: Application Loop

- [x] Implement `main.py` orchestration.
- [x] Open and configure the webcam.
- [x] Connect tracker, recognizer, and controller.
- [x] Render gesture, status, and FPS diagnostics.
- [x] Add `Q` exit handling.
- [x] Release camera, MediaPipe resources, and OpenCV windows on exit.
- [x] Surface actionable runtime errors.

## Phase 6: Verification

- [ ] Run all automated tests.
- [x] Run a syntax/import check.
- [ ] Verify at least 15 FPS on target hardware where available.
- [ ] Manually test cursor movement.
- [ ] Manually test left click and debounce behavior.
- [ ] Manually test right click and debounce behavior.
- [ ] Manually test fist pause.
- [ ] Manually test open-palm resume.
- [ ] Manually test loss of hand tracking.
- [ ] Manually test PyAutoGUI corner failsafe.
- [ ] Manually test clean `Q` exit.
- [ ] Check privacy behavior: no network, recordings, or persisted gesture data.

## Phase 7: Documentation and Release Readiness

- [ ] Complete README installation and usage instructions.
- [ ] Document recommended lighting and camera placement.
- [ ] Document macOS Accessibility and Screen Recording permissions.
- [ ] Document PyAutoGUI failsafe behavior.
- [ ] Document the non-ASCII path limitation and resolution.
- [ ] Document known limitations and v1 non-goals.
- [ ] Compare results with the PRD success metrics.
- [ ] Record unresolved risks or platform-specific gaps.

## Validation Commands

These commands are proposed and may be adjusted after the project structure is created:

```text
python -m pytest
python -m compileall .
python main.py
```

## Change Log

| Date | Change | Status |
|---|---|---|
| 2026-09-27 | Initial implementation checklist created from PRD | Awaiting review |
| 2026-09-27 | Foundation, core modules, app loop, and focused tests implemented | Automated checks pass; pytest and webcam validation pending |
