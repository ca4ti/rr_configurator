import sys
from PyQt5.QtWidgets import QApplication, QAbstractItemView , QVBoxLayout, QFrame, QWidget, QLabel, QGridLayout, QPushButton, QComboBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import constant

class GUI_ButtonMatrixPage():
    def __init__(self, win):
        self.win = win
        self.frame = QFrame()
        # self.grid.show()

    def init_matrix_gui(self):
        self.grid = QGridLayout()

        device = self.win.current_device


        self.grid.addWidget(QLabel("R"), 4, 0, 1, 1)
        self.grid.addWidget(QLabel("O"), 5, 0, 1, 1)
        self.grid.addWidget(QLabel("W"), 6, 0, 1, 1)
        self.grid.addWidget(QLabel("S"), 7, 0, 1, 1)

        self.grid.addWidget(QLabel("C"), 0, 6, 1, 1)
        self.grid.addWidget(QLabel("O"), 0, 7, 1, 1)
        self.grid.addWidget(QLabel("L"), 0, 8, 1, 1)
        self.grid.addWidget(QLabel("U"), 0, 9, 1, 1)
        self.grid.addWidget(QLabel("M"), 0, 10, 1, 1)
        self.grid.addWidget(QLabel("N"), 0, 11, 1, 1)
        self.grid.addWidget(QLabel("S"), 0, 12, 1, 1)

        for y in range(0, 17):
            for x in range(0, 18):
                if (x == 0 and y == 0):
                    #self.grid.addWidget(widget, y, x*2)
                    pass

                elif x == 0 and y >= 0:
                    widget = QComboBox()
                    self.grid.addWidget(widget, y+2, x*2+1, 1, 3)
                    device.widgets["matrix_row_label_" + str(y-1)] = widget
                    widget.addItem("N/A")
                    for m in range(0, len(device.get_pin_label_list())):
                        widget.addItem(device.get_pin_label_list()[m])

                    

                elif x >= 0 and y == 0:
                    widget = QComboBox()
                    self.grid.addWidget(widget, 1, x*2+2, 1, 2)
                    device.widgets["matrix_col_label_" + str(x-1)] = widget
                    widget.addItem("N/A")
                    for m in range(0, len(device.get_pin_label_list())):
                        widget.addItem(device.get_pin_label_list()[m])

                else:
                    widget = QLabel("0")
                    self.grid.addWidget(widget, y+2, x*2+2)
                    device.widgets["matrix_val_" + str(x-1) + "," + str(y-1)] = widget

                    widget = QLabel("N/A")
                    self.grid.addWidget(widget, y+2, x*2+3)
                    device.widgets["matrix_assignment_" + str(x-1) + "," + str(y-1)] = widget

        #self.grid.parent = self.layout
        self.frame.setFixedHeight(444)
        self.frame.setFixedWidth(900)
        self.frame.setLayout(self.grid)

    def UpdateMatrixGUIValues(self):
        device = self.win.current_device
        for row in range(0, 16):
            pass
            # if device.matrix_row_pins[row] == 254:
            #     device.widgets["matrix_row_label_" + str(row)].setText("RowPin")
            # else:
            #     device.widgets["matrix_row_label_" + str(row)].setText(constant.pro_micro_pin_label[device.matrix_row_pins[row]])

            # if device.matrix_col_pins[row] == 254:
            #     device.widgets["matrix_col_label_" + str(row)].setText("ColPin")
            # else:
            #     device.widgets["matrix_col_label_" + str(row)].setText(constant.pro_micro_pin_label[device.matrix_col_pins[row]])


    def hide(self):
        self.frame.hide()

    def show(self):
        self.frame.show()
