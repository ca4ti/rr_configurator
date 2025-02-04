# RealRobots Configurator

## UPDATE ##

If you're using an ESP32 or RP2040 based microcontroller then use the new, web based version instead at https://realrobots.net/configurator


## What is it?

The configurator is an app that runs on a PC and communicates with the RealRobots Modular [game controller firmware](https://gitlab.com/realrobots/rr_controller), allowing configuration of all analog and digital inputs as Joystick axis and buttons.

## How to use it?

Connect your device to a USB port on your PC

If you haven't already, upload the [rr_controller](https://gitlab.com/realrobots/rr_controller) firmware to it using the Arduino IDE

Download the [current distribution](./rr_configurator.zip) and decompress.

Run rr_configurator.exe

![](./choose_port.jpg)

Select the correct port and press "Connect".

You are now connected and can configure your device.

![](./main_page.jpg)

### on Linux
If you want to use this software on any Linux distribution, first make sure that you have Python 3 installed and then create a virtual environment in `src` directory of this project by running the command below in terminal:

`python3 -m venv venvname`

Then activate the virtual environment by the following command:

`source venv/bin/activate`

Now you are inside the venv you just created. You need to install rr_configurator's dependencies before running it. To do so enter the following command:

`pip install pyqt5 pyserial`

If everything went fine, you can run the app. Remeber that accessing serial ports requires superuser priviliges!

`sudo python3 rr_configurator.py`

## Tips

The device that you intend to be the parent device that will connecd to the USB has to be assigned address 0. Only a device with address 0 will attempt to connect to other devices connected to it and send HID joystick inputs to the computer.

Each device requires a unique address 0..255

For bluetooth connectivity device 0 MUST be an ESP32. ESP32s do not currently work as subdevices.

All changes are instantly applied to the device, but will revert when the device is power cycled unless "Commit to EEPROM" is used to commit the values to EEPROM. Committing to EEPROM only applies to the currently selected device.

Pins D2 and D3 (ATMEGA32U4) are special cases as they are used for communication between devices. If no child devices are connected they **should** be assignable and work normally, though this hasn't been tested.

## Supported microcontrollers
- HID master devices
    - ATMEGA32U4 (eg. Arduino Pro Micro)
    - ESP32 (bluetooth only, no USB HID)

- Secondary slave devices
    - ATMEGA32U4
    - ESP32
    - ATMEGA2560 (eg Arduino Mega 2560)
    - ATMEGA328  (eg Arduino Uno)


**Choose Device**: Will list connected devices if you are connected to device address 0 using USB and other devices have unique addresses 1..255.

Choose a device from this dropdown to configure it.

**PinMode**: "INPUT" sets a GPIO pin to receive inputs, "INPUT_PULLUP" does the same but also activates an internal pullup resistor. "OUTPUT" does nothing at the moment.

**Mode**:  "DIGITAL" converts an input into a binary 0 or 1. "ANALOG" provides the voltage applied to the pin in a 0..1023 value representing 0..5v input.

**Inverted**: If toggled flip a value, 0s become 1s and 1023 becomes 0 and vice versa.

**Min**: The minimum calibrated value, at or below this any input will be considered a 0. Only applies to analog inputs.

**Mid**: The center value, should be assigned whatever the raw_value is at rest, related to "DeadZone". Only applies to analog inputs.

**Max**: The maximum calibrated value, any value at or above this will be considered a 1023. Only applies to analog inputs.

**DeadZone**: A range around the Mid value, any input within this range will be reported at a 511 (halfway between 0 and 1023)

**Assignment**: The button or axis assigned to this input and which will be reported via HID as a joystick input to the PC.

**Raw Value**: The raw value being reported by the input pin.

**Calibrated Value**: The value after calibration and which will be reported via HID as a joystick input to the PC.


##### Get full DIY kits, ready to assemble from RealRobots [here](https://www.realrobots.net).

##### Support RealRobots on [Patreon](https://www.patreon.com/realrobots).

![](./pic2_xs.jpg)
