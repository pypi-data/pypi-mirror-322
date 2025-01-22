# -*- coding: utf-8 -*-
from __future__ import annotations

import click
from pioreactor import structs
from pioreactor import types as pt
from pioreactor.actions.led_intensity import led_intensity
from pioreactor.calibrations import CalibrationProtocol
from pioreactor.calibrations import utils
from pioreactor.utils import is_pio_job_running
from pioreactor.utils import managed_lifecycle
from pioreactor.utils.timing import current_utc_datetime
from pioreactor.whoami import get_testing_experiment_name
from pioreactor.whoami import get_unit_name


class LEDCalibration(structs.CalibrationBase, kw_only=True, tag="led"):
    # see structs.BaseCalibration for other fields
    x: str = "LED intensity"
    y: str = "Light sensor reading"


def introduction():
    click.clear()
    click.echo(
        """This routine will calibrate the LEDs on your current Pioreactor using an external light sensor. You'll need:
    1. A Pioreactor
    2. At least 10mL of your media
    3. A light sensor (or any type of photometer)
"""
    )


def get_metadata_from_user(channel):

    name = click.prompt("Provide a name for this calibration", type=str).strip()

    click.confirm(
        f"Confirm using channel {channel} in the Pioreactor",
        abort=True,
        default=True,
    )

    return name, channel


def setup_probe_instructions():
    click.clear()
    click.echo(
        """ Setting up:
    1. Add 10ml of your media into the glass vial.
    2. Place into Pioreactor.
    3. Hold your light sensor in place within the vial, submerged in your media.
"""
    )


def start_recording(channel: pt.LedChannel, min_intensity, max_intensity):
    led_intensity(
        desired_state={"A": 0, "B": 0, "C": 0, "D": 0},
        unit=get_unit_name(),
        experiment=get_testing_experiment_name(),
        verbose=False,
    )

    lightprobe_readings: list[float] = []
    led_intensities_to_test = utils.linspace(min_intensity, max_intensity, num=6)

    for i, intensity in enumerate(led_intensities_to_test):
        if i != 0:
            utils.plot_data(
                led_intensities_to_test[:i],
                lightprobe_readings,
                title="LED Calibration (ongoing)",
                x_min=min_intensity,
                x_max=max_intensity,
                x_label="LED intensity",
                y_label="Light sensor reading",
            )

        click.echo(click.style(f"Changing the LED intensity to {intensity}%", fg="green"))
        click.echo("Record the light intensity reading from your light probe.")

        led_intensity(
            desired_state={channel: intensity},
            unit=get_unit_name(),
            experiment=get_testing_experiment_name(),
        )

        r = click.prompt(
            click.style("Enter reading on light probe", fg="green"),
            confirmation_prompt=click.style("Repeat for confirmation", fg="green"),
            type=float,
        )

        lightprobe_readings.append(r)
        click.clear()
        click.echo()

    led_intensity(
        desired_state={"A": 0, "B": 0, "C": 0, "D": 0},
        unit=get_unit_name(),
        experiment=get_testing_experiment_name(),
        verbose=False,
    )

    return lightprobe_readings, led_intensities_to_test


def to_struct(
    curve_data_: list[float],
    curve_type: str,
    lightprobe_readings: list[float],
    led_intensities: list[float],
    name: str,
    unit: str,
) -> LEDCalibration:
    data_blob = LEDCalibration(
        created_at=current_utc_datetime(),
        calibrated_on_pioreactor_unit=unit,
        calibration_name=name,
        curve_data_=curve_data_,
        curve_type=curve_type,
        x="LED intensity",
        y="Light sensor reading",
        recorded_data={"x": led_intensities, "y": lightprobe_readings},
    )

    return data_blob


## general schematic of what's gonna happen
def run_led_calibration(target_device: str, min_intensity: float, max_intensity: float):
    unit = get_unit_name()
    experiment = get_testing_experiment_name()
    curve_data_: list[float] = []
    curve_type = "poly"

    if any(is_pio_job_running(["stirring", "od_reading"])):
        raise ValueError("Stirring and OD reading should be turned off.")

    with managed_lifecycle(unit, experiment, "led_calibration"):

        introduction()
        channel = target_device.removeprefix("led_")
        name, channel = get_metadata_from_user(channel)
        setup_probe_instructions()

        # retrieve readings from the light probe and list of led intensities
        lightprobe_readings, led_intensities = start_recording(
            channel, min_intensity, max_intensity
        )

        cal = to_struct(
            curve_data_,
            curve_type,
            lightprobe_readings,
            led_intensities,
            name,
            unit,
        )
        cal = utils.crunch_data_and_confirm_with_user(cal)

        click.echo(click.style(f"Data for {name}", underline=True, bold=True))
        click.echo(cal)
        click.echo(f"Finished calibration of {name} ✅")
        return cal


class LEDCalibrationProtocol(CalibrationProtocol):
    target_device = ["led_A", "led_B", "led_C", "led_D"]
    protocol_name = "led_calibration"

    def run(
        self, target_device: str, min_intensity: float = 0, max_intensity: float = 90
    ) -> LEDCalibration:
        return run_led_calibration(target_device, min_intensity, max_intensity)
