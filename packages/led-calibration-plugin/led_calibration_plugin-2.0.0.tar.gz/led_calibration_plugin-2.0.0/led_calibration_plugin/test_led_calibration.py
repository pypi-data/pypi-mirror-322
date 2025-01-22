# -*- coding: utf-8 -*-
from __future__ import annotations

import time

import pytest
from pioreactor.exc import CalibrationError
from pioreactor.utils import local_intermittent_storage
from pioreactor.utils import local_persistent_storage
from pioreactor.utils.timing import current_utc_datetime
from pioreactor.whoami import get_unit_name

from .calibrated_light_dark_cycle import CalibratedLightDarkCycle
from .led_calibration import LEDCalibration


def pause(n=1) -> None:
    time.sleep(n * 0.5)


def test_led_fails_if_calibration_not_present():
    experiment = "test_led_fails_if_calibration_not_present"
    unit = get_unit_name()

    with local_persistent_storage("active_calibrations") as cache:
        if "led_C" in cache:
            cache.pop("led_C")
        if "led_D" in cache:
            cache.pop("led_D")

    with pytest.raises(CalibrationError):

        with CalibratedLightDarkCycle(
            duration=1,
            light_intensity=-1,
            light_duration_minutes=16,
            dark_duration_minutes=8,
            unit=unit,
            experiment=experiment,
        ):

            pass


def test_set_intensity_au_above_max() -> None:
    experiment = "test_set_intensity_au_above_max"
    unit = get_unit_name()

    cal = LEDCalibration(
        created_at=current_utc_datetime(),
        calibrated_on_pioreactor_unit=unit,
        calibration_name=experiment,
        curve_data_=[1, 0],
        curve_type="poly",
        recorded_data={"x": [0, 1], "y": [0, 1]},
        x="LED intensity",
        y="Light sensor reading",
    )
    cal.set_as_active_calibration_for_device("led_C")
    cal.set_as_active_calibration_for_device("led_D")

    with CalibratedLightDarkCycle(
        duration=1,
        light_intensity=1500,
        light_duration_minutes=16,
        dark_duration_minutes=8,
        unit=unit,
        experiment=experiment,
    ) as lc:
        pause(10)
        assert lc.light_intensity == 1500  # test returns light_intensity (au)

        lc.set_light_intensity(2000)

        assert lc.light_intensity == 2000


def test_set_intensity_au_negative() -> None:
    experiment = "test_set_intensity_au_negative"
    unit = get_unit_name()

    cal = LEDCalibration(
        created_at=current_utc_datetime(),
        calibrated_on_pioreactor_unit=unit,
        calibration_name=experiment,
        curve_data_=[1, 0],
        curve_type="poly",
        recorded_data={"x": [0, 1], "y": [0, 1]},
        x="LED intensity",
        y="Light sensor reading",
    )
    cal.set_as_active_calibration_for_device("led_C")
    cal.set_as_active_calibration_for_device("led_D")

    with CalibratedLightDarkCycle(
        duration=1,
        light_intensity=-1,
        light_duration_minutes=16,
        dark_duration_minutes=8,
        unit=unit,
        experiment=experiment,
    ) as lc:

        assert lc.light_intensity == -1
        pause(8)

        with local_intermittent_storage("leds") as led_cache:
            assert float(led_cache["C"]) == 0.0
            assert float(led_cache["D"]) == 0.0
