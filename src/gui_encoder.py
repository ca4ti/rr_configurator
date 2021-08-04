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


        self.grid.addWidget(QLabel("Pin A"), 1, 0, 1, 1)
        self.grid.addWidget(QLabel("Pin B"), 1, 1, 1, 1)
        self.grid.addWidget(QLabel("Digital"), 1, 2, 1, 1)
        self.grid.addWidget(QLabel("Left Assignment"), 1, 3, 1, 1)
        self.grid.addWidget(QLabel("Right Assignment"), 1, 4, 1, 1)

        self.pin_A_combo_box = QComboBox()
        self.pin_A_combo_box.setGeometry(200, 150, 120, 30)
        self.pin_A_combo_box.activated[str].connect(self.on_pin_A_combo_change)
        self.pin_A_combo_box.addItems(self.win.current_device.get_pin_label_list())
        self.grid.addWidget(self.pin_A_combo_box, 2, 0, 1, 1)
        
        self.pin_B_combo_box = QComboBox()
        self.pin_B_combo_box.setGeometry(200, 150, 120, 30)
        self.pin_B_combo_box.activated[str].connect(self.on_pin_A_combo_change)
        self.pin_B_combo_box.addItems(self.win.current_device.get_pin_label_list())
        self.grid.addWidget(self.pin_B_combo_box, 2, 1, 1, 1)

        self.is_digital = QCheckBox()
        self.grid.addWidget(self.is_digital, 2, 2, 1, 1)

        self.left_assignment_combo_box = QComboBox()
        self.left_assignment_combo_box.setGeometry(200, 150, 120, 30)
        self.left_assignment_combo_box.activated[str].connect(partial(self.on_left_assignment_combo_change, 0))
        
        self.left_assignment_combo_box.addItems(constant.list_assigned_input)
        self.grid.addWidget(self.left_assignment_combo_box, 2, 3, 1, 1)
        
        self.right_assignment_combo_box = QComboBox()
        self.right_assignment_combo_box.setGeometry(200, 150, 120, 30)
        self.right_assignment_combo_box.activated[str].connect(self.on_right_assignment_combo_change)
        self.right_assignment_combo_box.addItems(constant.list_assigned_input)
        self.grid.addWidget(self.right_assignment_combo_box, 2, 4, 1, 1)


        #self.grid.parent = self.layout
        self.frame.setFixedHeight(444)
        self.frame.setFixedWidth(900)
        self.frame.setLayout(self.grid)
      

    def on_pin_A_combo_change(self):
        pass

    def on_pin_B_combo_change(self):
        pass

    def on_left_assignment_combo_change(self, encoderIdx):
        pass

    def on_right_assignment_combo_change(self):
        pass

    def pin_is_in_matrix(self, pin):
        for i in range(0, 16):
            if self.win.current_device.get_matrix_row_pin(i) == pin:
                return True
            if self.win.current_device.get_matrix_col_pin(i) == pin:
                return True
        return False

    def UpdateEncoderGUIValues(self):
        print("GUI UPDATE")
        device = self.win.current_device
        
        

    def hide(self):
        self.frame.hide()

    def show(self):
        self.frame.show()
