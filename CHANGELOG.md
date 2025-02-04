# v1.0.6 (06-08-2021)
- Added rotary encoder support
    - 4 encoders max, per device (more with subdevices)

# v1.0.5 (11-06-2021)
- More secondary, non-HID devices now supported
    - Atmega328 (Arduino Uno)
    - Atmega2560 (Arduino Mega) *66 inputs on this monster
    
# v1.0.4 (26-04-2021)
- Button matrices of up to 16x16 are now supported

- Outputs are partially implemented, a pin can now be assigned to permananently provide 5v, flash or pulse.

# v1.0.3 (02-04-2021)
- GUI now scrolls to accomodate more GPIOs and hopefully larger fonts

- Empty input boxes now revert to '0' rather than crashing the software

# v1.0.2 (29-03-2021)

- ESP32 compatibility implemented
    - ESP32 uses bluetooth HID (usb still required for configuration)
    - ESP32 only works as master device, cannot be slave. Supports Atmega32U4 slaves as usual.

- 8 default analog axis are now fixed, as changing HID identifier packet requires removing and resubscribing bluetooth device

- Software now retries sending serial packets on failure. Connection still fails occasionally, bypassed by user clicking connect again.

# v1.0.1 (09-02-2021) 

- simultaneous release to firmware v3

- increase possible inputs
    - max button inputs: 128 (up from 32)
    - hat inputs: 2 x 8 way hats

- labels for Atmega32u4 changed to reflect Pro Micro pin labels

# v1.0.0 (07-02-2021)

- Initial release

