import sys
from PyQt5.QtWidgets import QApplication, QAbstractItemView, QCheckBox, QVBoxLayout, QFrame, QWidget, QLabel, QGridLayout, QPushButton, QComboBox
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import pyqtSlot
from functools import partial
import constant

class GUI_EncoderPage():
    def __init__(self, win):
        self.win = win
        self.frame = QFrame()
        # self.grid.show()

        self.selected_input_assignment = 0

    def init_encoder_gui(self):
        self.grid = QGridLayout()

        device = self.win.current_device
        self.encoders = device.encoders


        self.grid.addWidget(QLabel("Pin A"), 1, 1, 1, 1)
        self.grid.addWidget(QLabel("Pin B"), 1, 2, 1, 1)
        # self.grid.addWidget(QLabel("Digital"), 1, 3, 1, 1)
        self.grid.addWidget(QLabel("Left Assignment"), 1, 4, 1, 1)
        self.grid.addWidget(QLabel("Right Assignment"), 1, 5, 1, 1)

        for i in range(0, len(self.encoders)):
            self.grid.addWidget(QLabel("Encoder " + str(i)), 2+i, 0, 1, 1)

            self.encoders[i].widgets["pin_a_combo_box"] = QComboBox()

            self.pin_A_combo_box = QComboBox()
            self.encoders[i].widgets["pin_a_combo_box"].setGeometry(200, 150, 120, 30)
            self.encoders[i].widgets["pin_a_combo_box"].activated[str].connect(partial(self.on_pin_A_combo_change, i))
            self.encoders[i].widgets["pin_a_combo_box"].addItem("N/A")
            self.encoders[i].widgets["pin_a_combo_box"].addItems(self.win.current_device.get_pin_label_list())
            self.grid.addWidget(self.encoders[i].widgets["pin_a_combo_box"], 2+i, 1, 1, 1)
            
            self.encoders[i].widgets["pin_b_combo_box"] = QComboBox()
            self.encoders[i].widgets["pin_b_combo_box"].setGeometry(200, 150, 120, 30)
            self.encoders[i].widgets["pin_b_combo_box"].activated[str].connect(partial(self.on_pin_B_combo_change, i))
            self.encoders[i].widgets["pin_b_combo_box"].addItem("N/A")
            self.encoders[i].widgets["pin_b_combo_box"].addItems(self.win.current_device.get_pin_label_list())
            self.grid.addWidget(self.encoders[i].widgets["pin_b_combo_box"], 2+i, 2, 1, 1)

            self.encoders[i].widgets["left_assignment_combo_box"] = QComboBox()
            self.encoders[i].widgets["left_assignment_combo_box"].setGeometry(200, 150, 120, 30)
            self.encoders[i].widgets["left_assignment_combo_box"].activated[str].connect(partial(self.on_left_assignment_combo_change, i))
            
            self.encoders[i].widgets["left_assignment_combo_box"].addItems(constant.list_assigned_input)
            self.grid.addWidget(self.encoders[i].widgets["left_assignment_combo_box"], 2+i, 4, 1, 1)
            
            self.encoders[i].widgets["right_assignment_combo_box"] = QComboBox()
            self.encoders[i].widgets["right_assignment_combo_box"].setGeometry(200, 150, 120, 30)
            self.encoders[i].widgets["right_assignment_combo_box"].activated[str].connect(partial(self.on_right_assignment_combo_change, i))
            self.encoders[i].widgets["right_assignment_combo_box"].addItems(constant.list_assigned_input)
            self.grid.addWidget(self.encoders[i].widgets["right_assignment_combo_box"], 2+i, 5, 1, 1)

        self.grid.addWidget(QLabel(""), 7, 5, 10, 5)

        #self.grid.parent = self.layout
        self.frame.setFixedHeight(444)
        self.frame.setFixedWidth(900)
        self.frame.setLayout(self.grid)
      

    def on_pin_A_combo_change(self, encoderIdx):
        pin_idx = self.encoders[encoderIdx].widgets["pin_a_combo_box"].currentIndex()-1
        self.encoders[encoderIdx].set_pin_a(pin_idx)

        self.win.current_device.set_reserved_pin(pin_idx)
        self.win.device_page.update_gpio_controls()    
        self.win.send_encoder_config_update(encoderIdx)

    def on_pin_B_combo_change(self, encoderIdx):
        pin_idx = self.encoders[encoderIdx].widgets["pin_b_combo_box"].currentIndex()-1
        self.encoders[encoderIdx].set_pin_b(pin_idx)
        
        self.win.current_device.set_reserved_pin(pin_idx)

        self.win.device_page.update_gpio_controls()    
        self.win.send_encoder_config_update(encoderIdx)  

    def on_left_assignment_combo_change(self, encoderIdx):
        self.encoders[encoderIdx].set_left_assignment(self.encoders[encoderIdx].widgets["left_assignment_combo_box"].currentIndex())
        self.win.send_encoder_config_update(encoderIdx)  

    def on_right_assignment_combo_change(self, encoderIdx):
        self.encoders[encoderIdx].set_right_assignment(self.encoders[encoderIdx].widgets["right_assignment_combo_box"].currentIndex())
        self.win.send_encoder_config_update(encoderIdx)  
    

    def UpdateEncoderGUIValues(self):
        print("GUI UPDATE")
        #device = self.win.current_device
        
        for i in range(0, len(self.encoders)):
            self.encoders[i].widgets["pin_a_combo_box"].setCurrentIndex(self.encoders[i].get_pin_a())
            self.encoders[i].widgets["pin_b_combo_box"].setCurrentIndex(self.encoders[i].get_pin_b())

            self.encoders[i].widgets["left_assignment_combo_box"].setCurrentIndex(self.encoders[i].get_left_assignment())
            self.encoders[i].widgets["right_assignment_combo_box"].setCurrentIndex(self.encoders[i].get_right_assignment())
        

    def hide(self):
        self.frame.hide()

    def show(self):
        self.frame.show()
