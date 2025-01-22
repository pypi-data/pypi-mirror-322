# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Optional

from pioreactor.automations import events
from pioreactor.automations.led.base import LEDAutomationJobContrib
from pioreactor.calibrations import load_active_calibration
from pioreactor.exc import CalibrationError
from pioreactor.types import LedChannel
from pioreactor.utils import clamp
from pioreactor.utils import local_persistent_storage


class CalibratedLightDarkCycle(LEDAutomationJobContrib):
    """
    Follows as min light / min dark cycle. Starts light ON.
    """

    automation_name: str = "calibrated_light_dark_cycle"
    published_settings = {
        "duration": {
            "datatype": "float",
            "settable": False,
            "unit": "min",
        },
        "light_intensity": {"datatype": "float", "settable": True, "unit": "%"},
        "light_duration_minutes": {"datatype": "integer", "settable": True, "unit": "min"},
        "dark_duration_minutes": {"datatype": "integer", "settable": True, "unit": "min"},
    }

    def __init__(
        self,
        light_intensity: float | str,
        light_duration_minutes: int | str,
        dark_duration_minutes: int | str,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.minutes_online: int = -1
        self.light_active: bool = False
        self.channels: list[LedChannel] = ["D", "C"]
        self.set_light_intensity(light_intensity)
        self.light_duration_minutes = float(light_duration_minutes)
        self.dark_duration_minutes = float(dark_duration_minutes)

        with local_persistent_storage("active_calibrations") as cache:
            for channel in self.channels:
                if self.channel_to_led_device(channel) not in cache:
                    raise CalibrationError(f"Calibration for {channel} does not exist.")

    def channel_to_led_device(self, channel: LedChannel) -> str:
        return f"led_{channel}"

    def execute(self) -> Optional[events.AutomationEvent]:
        # runs every minute
        self.minutes_online += 1
        return self.trigger_leds(self.minutes_online)

    def calculate_intensity_percent(self, channel: str) -> float:

        led_calibration = load_active_calibration(self.channel_to_led_device(channel))

        intensity_percent = led_calibration.ipredict(self.light_intensity)

        return clamp(0, intensity_percent, 100)

    def trigger_leds(self, minutes: int) -> Optional[events.AutomationEvent]:
        """
        Changes the LED state based on the current minute in the cycle.

        The light and dark periods are calculated as multiples of 60 minutes, forming a cycle.
        Based on where in this cycle the current minute falls, the light is either turned ON or OFF.

        Args:
            minutes: The current minute of the cycle.

        Returns:
            An instance of AutomationEvent, indicating that LEDs' status might have changed.
            Returns None if the LEDs' state didn't change.
        """
        cycle_duration_min = int(self.light_duration_minutes + self.dark_duration_minutes)
        if ((minutes % cycle_duration_min) < (self.light_duration_minutes)) and (
            not self.light_active
        ):
            self.light_active = True

            for channel in self.channels:
                intensity_percent = self.calculate_intensity_percent(channel)
                self.set_led_intensity(channel, intensity_percent)

            return events.ChangedLedIntensity(f"{minutes:.1f}min: turned on LEDs.")

        elif ((minutes % cycle_duration_min) >= (self.light_duration_minutes)) and (
            self.light_active
        ):
            self.light_active = False
            for channel in self.channels:
                self.set_led_intensity(channel, 0)
            return events.ChangedLedIntensity(f"{minutes:.1f}min: turned off LEDs.")

        else:
            return None

    # minutes setters
    def set_dark_duration_minutes(self, minutes: int):
        self.dark_duration_minutes = minutes

        self.trigger_leds(self.minutes_online)

    def set_light_duration_minutes(self, minutes: int):
        self.light_duration_minutes = minutes

        self.trigger_leds(self.minutes_online)

    def set_light_intensity(self, intensity_au):
        # this is the setter of light_intensity attribute, eg. called when updated over MQTT

        self.light_intensity = float(intensity_au)
        if self.light_active:
            # update now!

            for channel in self.channels:
                intensity_percent = self.calculate_intensity_percent(channel)
                self.set_led_intensity(channel, intensity_percent)
        else:
            pass

    def set_duration(self, duration: float) -> None:
        if duration != 1:
            self.logger.warning("Duration should be set to 1.")
        super().set_duration(duration)
