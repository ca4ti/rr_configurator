from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QPushButton, QLabel, QComboBox, QCheckBox, QLineEdit
from PyQt5.QtGui import QIntValidator
from functools import partial
import constant


class GUI_DevicePage():
    def __init__(self, win):
        self.win = win
        self.offset = [120, 200]
        self.ygap = 30

    def init_device_controls(self):
        device = self.win.current_device
        for i in range(0, len(self.win.current_device.gpios)):            

            # Label
            widget = QLabel(self.win)
            widget.setText(device.gpios[i].get_pin_label())
            xpos = 0
            widget.move(self.offset[0], self.offset[1] + i*self.ygap +3)
            widget.show()
            device.gpios[i].widgets["label"] = widget

            # PinMode combobox            
            widget = QComboBox(self.win)
            for m in range(0, len(constant.list_input_modes)):
                widget.addItem(constant.list_input_modes[m])
            xpos += 50
            widget.move(self.offset[0]+xpos, self.offset[1] + i*self.ygap)
            widget.show()
            device.gpios[i].widgets["pin_mode"] = widget

            # InputType combobox            
            widget = QComboBox(self.win)
            for m in range(0, len(constant.list_analog_modes)):
                widget.addItem(constant.list_analog_modes[m])
            xpos += 100
            widget.move(self.offset[0]+xpos, self.offset[1] + i*self.ygap)
            widget.show()
            device.gpios[i].widgets["input_type"] = widget

            # isInverted Checkbox
            widget = QCheckBox(self.win)
            xpos += 85
            widget.move(self.offset[0]+xpos, self.offset[1] + 4 + i*self.ygap)
            #widget.setChecked(True)
            widget.show()
            device.gpios[i].widgets["is_inverted"] = widget

            # Min
            widget = QLineEdit(self.win)
            widget.setValidator(QIntValidator())
            xpos += 30
            widget.setGeometry(self.offset[0]+xpos, self.offset[1] + i*self.ygap, 40, 20)
            widget.show()
            device.gpios[i].widgets["min"] = widget

            # Mid
            widget = QLineEdit(self.win)
            widget.setValidator(QIntValidator())
            xpos += 42
            widget.setGeometry(self.offset[0]+xpos, self.offset[1] + i*self.ygap, 40, 20)
            widget.show()
            device.gpios[i].widgets["mid"] = widget

            # Max
            widget = QLineEdit(self.win)
            widget.setValidator(QIntValidator())
            xpos += 42
            widget.setGeometry(self.offset[0]+xpos, self.offset[1] + i*self.ygap, 40, 20)
            widget.show()
            device.gpios[i].widgets["max"] = widget

            # DeadZone
            widget = QLineEdit(self.win)
            widget.setValidator(QIntValidator())
            xpos += 42
            widget.setGeometry(self.offset[0]+xpos, self.offset[1] + i*self.ygap, 40, 20)
            widget.show()
            device.gpios[i].widgets["dead_zone"] = widget

            # Button Assignment
            widget = QComboBox(self.win)
            for m in range(0, len(constant.list_assigned_input)):
                widget.addItem(constant.list_assigned_input[m])
            xpos += 42
            widget.move(self.offset[0]+xpos, self.offset[1] + i*self.ygap + 3)
            widget.show()
            device.gpios[i].widgets["assigned_input"] = widget

            widget = QLabel(self.win)
            widget.setText("0")
            xpos += 150
            widget.move(self.offset[0]+xpos, self.offset[1] + i*self.ygap + 3)
            widget.show()
            device.gpios[i].widgets["raw_val"] = widget

            widget = QLabel(self.win)
            widget.setText("0")
            xpos += 80
            widget.move(self.offset[0]+xpos, self.offset[1] + i*self.ygap + 3)
            widget.show()
            device.gpios[i].widgets["calibrated_val"] = widget
