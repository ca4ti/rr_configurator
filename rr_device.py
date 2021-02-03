import constant

class RR_Device():
    def __init__(self):
        self.device_name = "unknown device"
        self.firmware_version = -1
        self.microcontroller = -1
        self.sub_device_count = 0
        self.address = 0        
        self.gpios = []

        self.widgets = {}

        

    def init_from_header(self, header):
        self.device_name = header["device_name"]
        self.firmware_version = header["firmware_version"]
        self.microcontroller = header["device_type"]
        self.sub_device_count = header["sub_device_count"]
        self.address = header["address"]

        self.init_gpios()

    # GPIO count and labels based on microcontroller presets
    def init_gpios(self):
        for i in range(0, len(constant.pro_micro_pin_idx)):
            gpio = RR_GPIO(self.address, i)
            gpio.pin_number = constant.pro_micro_pin_idx[i]
            gpio.pin_label = constant.pro_micro_pin_label[i]
            self.gpios.append(gpio)


class RR_GPIO():
    def __init__(self, device_address, idx):
        self.raw_val = 0
        self.calibrated_value = 0
        self.pin_number = None
        self.pin_label = "?"
        self.pin_mode = constant.INPUT_PULLUP
        self.is_analog = constant.DIGITAL
        self.is_inverted = 0

        self.min_val = 0
        self.mid_val = 127
        self.max_val = 255
        self.dead_zone = 0  # radius of deadzone

        self.assigned_input = constant.NOAXIS

        self.device_address = device_address
        self.gpio_index = idx

        self.widgets = {}

    def get_pin_label(self):
        return str(self.pin_label) + "/" + str(self.pin_number)

        
