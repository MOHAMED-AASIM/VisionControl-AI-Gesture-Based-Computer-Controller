"""Mouse side effects, coordinate mapping, smoothing, and debouncing."""

import time
from typing import Callable, Optional, Tuple

from config import Config, CONFIG
from gesture_recognizer import Gesture


class MouseController:
    def __init__(
        self,
        config: Config = CONFIG,
        move_to: Optional[Callable[[float, float], None]] = None,
        click: Optional[Callable[[str], None]] = None,
        screen_size: Optional[Tuple[int, int]] = None,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        if move_to is None or click is None or screen_size is None:
            import pyautogui

            pyautogui.FAILSAFE = True
            move_to = move_to or pyautogui.moveTo
            click = click or pyautogui.click
            screen_size = screen_size or pyautogui.size()
        self._config = config
        self._move_to = move_to
        self._click = click
        self._screen_width, self._screen_height = screen_size
        self._clock = clock
        self._last_position: Optional[Tuple[float, float]] = None
        self._last_click_time = {Gesture.LEFT_CLICK: -float("inf"), Gesture.RIGHT_CLICK: -float("inf")}
        self.enabled = True

    def set_enabled(self, enabled: bool) -> None:
        self.enabled = enabled
        if not enabled:
            self._last_position = None

    def map_position(self, point: Tuple[float, float], frame_size: Tuple[int, int]) -> Tuple[float, float]:
        frame_width, frame_height = frame_size
        x_ratio = (point[0] / frame_width - self._config.active_zone_left) / (self._config.active_zone_right - self._config.active_zone_left)
        y_ratio = (point[1] / frame_height - self._config.active_zone_top) / (self._config.active_zone_bottom - self._config.active_zone_top)
        x_ratio = min(1.0, max(0.0, x_ratio))
        y_ratio = min(1.0, max(0.0, y_ratio))
        return x_ratio * self._screen_width, y_ratio * self._screen_height

    def update(self, gesture: Gesture, point: Optional[Tuple[float, float]], frame_size: Tuple[int, int]) -> None:
        if gesture == Gesture.PAUSE:
            self.set_enabled(False)
            return
        if gesture == Gesture.RESUME:
            self.set_enabled(True)
            return
        if not self.enabled:
            return
        if gesture == Gesture.MOVE and point is not None:
            target = self.map_position(point, frame_size)
            if self._last_position is None:
                self._last_position = target
            else:
                factor = self._config.smoothing_factor
                self._last_position = tuple(
                    previous + (current - previous) * factor
                    for previous, current in zip(self._last_position, target)
                )
            self._move_to(*self._last_position)
            return
        if gesture in self._last_click_time:
            now = self._clock()
            if now - self._last_click_time[gesture] >= self._config.click_cooldown_seconds:
                button = "left" if gesture == Gesture.LEFT_CLICK else "right"
                self._click(button=button)
                self._last_click_time[gesture] = now