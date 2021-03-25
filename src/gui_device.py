from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QPushButton, QLabel, QComboBox, QCheckBox, QLineEdit, QGridLayout
from PyQt5.QtGui import QIntValidator
from functools import partial
import constant


class GUI_DevicePage():
    def __init__(self, win):
        self.win = win
        self.offset = [20, 20]
        self.ygap = 30
        self.is_ready = False  # prevents sending update to device on init

    def init_device_controls(self):
        device = self.win.current_device
        xpos = 0
        ypos = 0

        widget = QPushButton(self.win)
        widget.setText("Disconnect")
        widget.move(self.offset[0]+ 645, self.offset[1])
        widget.show()
        widget.clicked.connect(lambda: self.win.reset(""))
        device.widgets["btn_disconnect"] = widget

        widget = QPushButton(self.win)
        widget.setText("Commit to EEPROM")
        widget.move(self.offset[0]+ 620, self.offset[1]+25)
        widget.show()
        widget.clicked.connect(lambda: self.win.commit_to_eeprom())
        device.widgets["btn_commit_to_eeprom"] = widget       

        # Device Details
        widget = QLabel(self.win)
        widget.setText("Choose Device")
        widget.move(self.offset[0], self.offset[1])
        widget.show()
        device.widgets["label_sub_device_picker"] = widget

        widget = QComboBox(self.win)        
        widget.addItem(device.device_name)
        for sub_device in device.sub_devices:
            widget.addItem(sub_device.device_name)
        widget.move(self.offset[0], self.offset[1]+20)
        widget.activated[str].connect(partial(self.on_combo_change, 0, "combo_sub_device_picker"))            
        widget.show()
        device.widgets["combo_sub_device_picker"] = widget

        widget = QLabel(self.win)
        widget.setText("Device Name:")
        widget.move(self.offset[0] + 200, self.offset[1])
        widget.show()
        device.widgets["label_device_name"] = widget

        widget = QLineEdit(self.win)
        widget.setText(device.device_name)
        widget.setGeometry(self.offset[0] + 295, self.offset[1]-2, 100, 20)
        widget.textChanged.connect(partial(self.on_combo_change, -1, "input_device_name")) 
        
        widget.show()
        device.widgets["input_device_name"] = widget


        widget = QLabel(self.win)
        widget.setText("Microcontroller:\t" + constant.list_device_types[device.microcontroller])
        widget.move(self.offset[0] + 200, self.offset[1]+20)
        widget.show()
        device.widgets["label_device_type"] = widget

        widget = QLabel(self.win)
        widget.setText("Firmware Version:\t" + str(device.firmware_version))
        widget.move(self.offset[0] + 200, self.offset[1]+40)
        widget.show()
        device.widgets["label_firmware_version"] = widget

        widget = QLabel(self.win)
        widget.setText("Address: ")
        widget.move(self.offset[0] + 420, self.offset[1])
        widget.show()
        device.widgets["label_device_address"] = widget

        widget = QLineEdit(self.win)
        widget.setValidator(QIntValidator())
        widget.setText(str(device.address))
        widget.setGeometry(self.offset[0] + 470, self.offset[1]-2, 40, 20)
        widget.textChanged.connect(partial(self.on_combo_change, -1, "input_device_address"))   
        widget.show()
        device.widgets["input_device_address"] = widget


        # GPIO control labels
        widget = QLabel(self.win)
        widget.setText("GPIO")
        widget.move(self.offset[0]+5, self.offset[1] + 70)
        widget.show()
        device.widgets["label_GPIO"] = widget

        widget = QLabel(self.win)
        widget.setText("Pin Mode")
        widget.move(self.offset[0]+78, self.offset[1] + 70)
        widget.show()
        device.widgets["label_pin_mode"] = widget

        widget = QLabel(self.win)
        widget.setText("Mode")
        widget.move(self.offset[0]+170, self.offset[1] + 70)
        widget.show()
        device.widgets["label_mode"] = widget

        widget = QLabel(self.win)
        widget.setText("Inverted")
        widget.move(self.offset[0]+221, self.offset[1] + 70)
        widget.show()
        device.widgets["label_inverted"] = widget

        widget = QLabel(self.win)
        widget.setText("Min")
        widget.move(self.offset[0]+276, self.offset[1] + 70)
        widget.show()
        device.widgets["label_min"] = widget

        widget = QLabel(self.win)
        widget.setText("Mid")
        widget.move(self.offset[0]+278+40, self.offset[1] + 70)
        widget.show()
        device.widgets["label_mid"] = widget

        widget = QLabel(self.win)
        widget.setText("Max")
        widget.move(self.offset[0]+278+80, self.offset[1] + 70)
        widget.show()
        device.widgets["label_max"] = widget

        widget = QLabel(self.win)
        widget.setText("DeadZone")
        widget.move(self.offset[0]+394, self.offset[1] + 70)
        widget.show()
        device.widgets["label_dead_zone"] = widget

        widget = QLabel(self.win)
        widget.setText("Assignment")
        widget.move(self.offset[0]+470, self.offset[1] + 70)
        widget.show()
        device.widgets["label_assignment"] = widget

        widget = QLabel(self.win)
        widget.setText("Raw_Value")
        widget.move(self.offset[0]+570, self.offset[1] + 70)
        widget.show()
        device.widgets["label_raw_val"] = widget

        widget = QLabel(self.win)
        widget.setText("Calibrated_Value")
        widget.move(self.offset[0]+640, self.offset[1] + 70)
        widget.show()
        device.widgets["label_calibrated_val"] = widget


        ypos += 90
        # GPIO controls
        for i in range(0, len(self.win.current_device.gpios)):            

            # Label
            widget = QLabel(self.win)
            widget.setText(device.gpios[i].get_pin_label())
            xpos = 0
            widget.move(self.offset[0], self.offset[1] + ypos + i*self.ygap +3)
            widget.show()
            device.gpios[i].widgets["label"] = widget

            # PinMode combobox            
            widget = QComboBox(self.win)
            for m in range(0, len(constant.list_input_modes)):
                widget.addItem(constant.list_input_modes[m])
            xpos += 50
            widget.move(self.offset[0]+xpos, self.offset[1] + ypos + i*self.ygap)
            widget.activated[str].connect(partial(self.on_combo_change, i, "pin_mode"))
            widget.show()
            device.gpios[i].widgets["pin_mode"] = widget

            # InputType combobox            
            widget = QComboBox(self.win)
            for m in range(0, len(constant.list_analog_modes)):
                widget.addItem(constant.list_analog_modes[m])
            xpos += 100
            widget.move(self.offset[0]+xpos, self.offset[1] + ypos + i*self.ygap)
            widget.activated[str].connect(partial(self.on_combo_change, i, "input_type"))
            widget.show()
            device.gpios[i].widgets["input_type"] = widget

            # isInverted Checkbox
            widget = QCheckBox(self.win)
            xpos += 85
            widget.move(self.offset[0]+xpos, self.offset[1] + ypos + 4 + i*self.ygap)
            #widget.setChecked(True)
            widget.toggled.connect(partial(self.on_combo_change, i, "is_inverted"))            
            widget.show()
            device.gpios[i].widgets["is_inverted"] = widget

            # Min
            widget = QLineEdit(self.win)
            widget.setValidator(QIntValidator())
            xpos += 30
            widget.setGeometry(self.offset[0]+xpos, self.offset[1] + ypos + i*self.ygap, 40, 20)
            widget.textChanged.connect(partial(self.on_combo_change, i, "min"))  
            widget.show()
            device.gpios[i].widgets["min"] = widget

            # Mid
            widget = QLineEdit(self.win)
            widget.setValidator(QIntValidator())
            xpos += 42
            widget.setGeometry(self.offset[0]+xpos, self.offset[1] + ypos + i*self.ygap, 40, 20)
            widget.textChanged.connect(partial(self.on_combo_change, i, "mid"))              
            widget.show()
            device.gpios[i].widgets["mid"] = widget

            # Max
            widget = QLineEdit(self.win)
            widget.setValidator(QIntValidator())
            xpos += 42
            widget.setGeometry(self.offset[0]+xpos, self.offset[1] + ypos + i*self.ygap, 40, 20)
            widget.textChanged.connect(partial(self.on_combo_change, i, "max"))  
            widget.show()
            device.gpios[i].widgets["max"] = widget

            # DeadZone
            widget = QLineEdit(self.win)
            widget.setValidator(QIntValidator())
            xpos += 50
            widget.setGeometry(self.offset[0]+xpos, self.offset[1] + ypos + i*self.ygap, 40, 20)
            widget.textChanged.connect(partial(self.on_combo_change, i, "dead_zone"))  
            widget.show()
            device.gpios[i].widgets["dead_zone"] = widget

            # Button Assignment
            widget = QComboBox(self.win)
            for m in range(0, len(constant.list_assigned_input)):
                widget.addItem(constant.list_assigned_input[m])
            xpos += 50
            widget.move(self.offset[0]+xpos, self.offset[1] + ypos + i*self.ygap)
            widget.activated[str].connect(partial(self.on_combo_change, i, "assigned_input"))            
            widget.show()
            device.gpios[i].widgets["assigned_input"] = widget

            widget = QLabel(self.win)
            widget.setText("9999")
            xpos += 150
            widget.move(self.offset[0]+xpos, self.offset[1] + ypos + i*self.ygap + 3)
            widget.show()
            device.gpios[i].widgets["raw_val"] = widget

            widget = QLabel(self.win)
            widget.setText("9999")
            xpos += 80
            widget.move(self.offset[0]+xpos, self.offset[1] + ypos + i*self.ygap + 3)
            widget.show()
            device.gpios[i].widgets["calibrated_val"] = widget

    def on_change_selected_device(self, sub_device_index):
        device = self.win.current_device
        self.win.current_device.selected_sub_device = sub_device_index
        #device.widgets["label_device_name"].setText("Device Name:")
        device.widgets["input_device_name"].setText(device.get_selected_device_name())
        device.widgets["label_device_type"].setText("Microcontroller:\t" + device.get_selected_device_type())      
        device.widgets["label_firmware_version"].setText("Firmware Version:\t" + device.get_selected_firmware_version())
        device.widgets["input_device_address"].setText(str(device.get_selected_device_address()))
        #self.win.select_sub_device(sub_device_index)
        self.win.request_device_config(sub_device_index)

    def on_combo_change(self, gpio_index, control):
        gpio = self.win.current_device.gpios[gpio_index]

        if control == "combo_sub_device_picker":
            self.on_change_selected_device(self.win.current_device.widgets[control].currentIndex())            
            return
        elif control == "input_device_name":   
            if not self.win.current_device.widgets[control].hasFocus():
                return         
            text = self.win.current_device.widgets[control].text()            
            if len(text) < 16:
                diff = 16 - len(text)
                for i in range(0, diff):
                    text += " "
            elif len(text) > 16:
                text = text[0:16]

            self.win.current_device.get_selected_device().device_name = text
            self.win.send_device_name_update(text)
            return
        elif control == "input_device_address":
            if not self.win.current_device.widgets[control].hasFocus():
                return
            val = self.win.current_device.widgets[control].text() 
            val = int(val)
            if val < 0:
                val = 0
            if val > 255:
                val = 255
            
            self.win.current_device.get_selected_device().address = val
            self.win.send_device_address_update(val)
            return
        elif control == "pin_mode":
            #print(gpio.widgets[control].currentIndex())
            gpio.pin_mode = gpio.widgets[control].currentIndex()
        elif control == "input_type":
            #print(gpio.widgets[control].currentIndex())
            gpio.is_analog = gpio.widgets[control].currentIndex()
        elif control == "is_inverted":
            #print(gpio.widgets[control].isChecked())
            gpio.is_inverted = gpio.widgets[control].isChecked()
        elif control == "min":
            if not gpio.widgets[control].hasFocus():
                return
            #print(gpio.widgets[control].text())
            gpio.min_val = int(gpio.widgets[control].text())
        elif control == "mid":
            if not gpio.widgets[control].hasFocus():
                return
            #print(gpio.widgets[control].text())
            gpio.mid_val = int(gpio.widgets[control].text())
        elif control == "max":
            if not gpio.widgets[control].hasFocus():
                return
            #print(gpio.widgets[control].text())
            gpio.max_val = int(gpio.widgets[control].text())
        elif control == "dead_zone":
            if not gpio.widgets[control].hasFocus():
                return
            #print(gpio.widgets[control].text())
            gpio.dead_zone = int(gpio.widgets[control].text())
        elif control == "assigned_input":
            #print(gpio.widgets[control].currentIndex())
            gpio.assigned_input = gpio.widgets[control].currentIndex()

        if self.is_ready:
            self.win.send_gpio_config_update(gpio_index)
    
    def update_gpio_controls(self):
        device = self.win.current_device
        for i in range(0, len(self.win.current_device.gpios)):  
            gpio = device.gpios[i]
            
            gpio.widgets["pin_mode"].setCurrentIndex(gpio.pin_mode)
            gpio.widgets["input_type"].setCurrentIndex(gpio.is_analog)
            gpio.widgets["is_inverted"].setChecked(gpio.is_inverted)
            gpio.widgets["min"].setText(str(gpio.min_val))
            gpio.widgets["mid"].setText(str(gpio.mid_val))
            gpio.widgets["max"].setText(str(gpio.max_val))
            gpio.widgets["dead_zone"].setText(str(gpio.dead_zone))
            gpio.widgets["assigned_input"].setCurrentIndex(gpio.assigned_input)

        self.is_ready = True

    def update_gpio_controls_values(self):
        device = self.win.current_device
        for i in range(0, len(self.win.current_device.gpios)):  
            gpio = device.gpios[i]
            
            gpio.widgets["raw_val"].setText(str(gpio.raw_val))
            gpio.widgets["calibrated_val"].setText(str(gpio.calibrated_value))
            gpio.widgets["calibrated_val"].adjustSize()

    def show(self):
        print("showing device page")
        self.init_device_controls()

    def hide(self):
        # print(self.win.current_device.widgets)
        if self.win.current_device == None:
            return
        for key, value in self.win.current_device.widgets.items():
            value.hide()

        for gpio in self.win.current_device.gpios:
            for key, value in gpio.widgets.items():
                value.hide()
        self.is_ready = False