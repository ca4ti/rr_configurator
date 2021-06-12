## List of upcoming changes 

- Support for i2c/spi modules like MPU6050 and ADXL345

- toggle on/off button options

- Implement bluetooth HID code to USBHID and discontinue use of Joystick.h for own code

- increase possible inputs
    - all eleven axes enabled
    - keyboard input
    - mouse input

- confirmed rotary encoder support

- expanded compatibility
    - Teensy boards
    - easy way for users to add boards themselves?

- change name reported to OS
- toggleable button debouncing

- outputs (biggest thing is implementing an interface)
    - WS2812b compatibility 
    - buzzer (mostly want tactile response on throttle positions)



## Wish List 

- Force Feedback
- 5-pin din compatibility with other devices (legal?)


## Known Bugs

- ESP32 limited to 16 inputs (will be updated soon now that more inputs are implemented in GUI and i2c code)

- Applying "RESERVED" tag manually does not wipe config from pins and so causes weirdness as it was not initially designed as a user applied tag but one automatically applied when a pin is assigned to a matrix so users know not to use it. This will be fixed soon to be more intuitive but in the meantime don't set pins to RESERVED, it doesn't do anything that leaving a pin with no assigned button does.