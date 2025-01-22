
## Pioreactor LED calibration plugin

![CI tests](https://github.com/pioreactor/pioreactor-led-calibration-plugin/actions/workflows/ci.yaml/badge.svg)

The LED automations available on the Pioreactor are limited: light intensity percentages are based on the power supplied to the LED wires. For specific research and for comparing results between Pioreactors, this plugin can be used to determine the exact LED intensity values.

This plugin offers the ability to calibrate your LEDs using an **external light probe**. It functions in two parts:
1) a command line calibration that creates a line-of-best-fit and
2) a calibrated light/dark cycle automation available on the Pioreactor web interface.

## Installation instructions

Install from the command line.

```
pio plugins install led-calibration-plugin  ## to install on a single Pioreactor

## OR, on the command line of the leader Pioreactor

pios plugins install led-calibration-plugin ## to install on all Pioreactors in a cluster
```

This plugin is also available on the Pioreactor web interface, in the _Plugins_ tab. Downloading from the web interface will install on all Pioreactors in a cluster.

## Run your calibration

Type into your command line:

```
pio calibrations run --device led_C --protocol-name led_calibration
pio calibrations run --device led_D --protocol-name led_calibration
```

To perform this calibration, insert your vial containing media into the Pioreactor and submerge your light probe. Follow the prompts on the command line. The plugin will increase the light intensity, and prompt you to record the readings from your light probe. A calibration line of best fit will be generated based on your light probe readings.

## Use the calibration on the UI

An automation will become available on the web interface. To use this automation, use two LED cables in each of channels C and D, and insert the bulbs into the X2 and X3 pockets on the Pioreactor vial holder. **Calibrations for LEDs in channels "C" and "D" must exist.**

In the _Pioreactors_ tab, under _Manage_, you can _Start_ an _LED automation_. A new option becomes available in the drop-down menu called "Calibrated Light/Dark Cycle". Input your desired light intensity in AU (ex. 1000 AU). The automation will set the percent light intensity such that an output of 1000 AU occurs on **both** LEDs.

## When to perform an LED calibration

Calibrations should be performed on a case-by-case basis. A new calibration must be performed per channel, and/or for new LED cables, and with any change in media that can alter the light intensity within the vial.

## Plugin documentation

Documentation for plugins can be found on the [Pioreactor wiki](https://docs.pioreactor.com/developer-guide/intro-plugins).
