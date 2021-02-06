import constant

class RR_Device():
    def __init__(self):
        self.device_name = "unknown device"
        self.firmware_version = -1
        self.microcontroller = -1
        self.sub_device_count = 0
        self.address = 0        
        self.gpios = []
        self.sub_devices = []

        # 0 == this device, subdevices are index+1
        self.selected_sub_device = 0

        self.widgets = {}

    def get_selected_device_name(self):
        if self.selected_sub_device == 0:
            return self.device_name
        else:
            return self.sub_devices[self.selected_sub_device-1].device_name  

    def get_selected_device_type(self):
        if self.selected_sub_device == 0:
            return constant.list_device_types[self.microcontroller]
        else:
            return constant.list_device_types[self.sub_devices[self.selected_sub_device-1].microcontroller]

    def get_selected_firmware_version(self):
        if self.selected_sub_device == 0:
            return str(self.firmware_version)
        else:
            return str(self.sub_devices[self.selected_sub_device-1].firmware_version)

    def get_selected_device_address(self):
        if self.selected_sub_device == 0:
            return str(self.address)
        else:
            return str(self.sub_devices[self.selected_sub_device-1].address)

    def get_selected_device(self):
        if self.selected_sub_device == 0:
            return self
        else:
            return self.sub_devices[self.selected_sub_device-1]

    def init_from_header(self, header):
        self.device_name = header["device_name"]
        self.firmware_version = header["firmware_version"]
        self.microcontroller = header["device_type"]
        self.address = header["address"]
        if self.address == 0:
            self.sub_device_count = header["sub_device_count"]

        self.init_gpios()

    def add_sub_device(self, sub_device):
        self.sub_devices.append(sub_device)

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

        
