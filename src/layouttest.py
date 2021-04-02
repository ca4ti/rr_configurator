from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QGridLayout, QComboBox, QWidget, QLineEdit, QScrollArea, QVBoxLayout, QGroupBox, QLabel, QPushButton, QFormLayout
import sys


class Window(QWidget):
    def __init__(self, val):
        super().__init__()
        self.title = "PyQt5 Scroll Bar"
        self.setGeometry(100, 100, 860, 100)
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)

        scrollingGridLayout = QGridLayout()
        groupBox = QGroupBox()

        self.columnSpans = [1, 4, 4, 4, 1, 1, 2, 1, 1, 1, 4]

        for r in range(0, 50):
            widgets = []
            widget = QLabel(self)
            if r % 2 == 0:
                widget.setText("hi1asdfdasfdasfdasfads there")
            else:
                widget.setText("hi1here")
            widgets.append(widget)
            widget = QComboBox(self)
            widget.addItem("1")
            widget.addItem("2")
            widgets.append(widget)
            widget = QComboBox(self)
            widget.addItem("fasdfdsfd1")
            widget.addItem("2")
            widgets.append(widget)
            widget = QComboBox(self)
            widgets.append(widget)

            for x in range(0, len(widgets)):
                scrollingGridLayout.addWidget(widgets[x], r, x, 1, 1)

       
       
        groupBox.setLayout(scrollingGridLayout)
        gpio_scroll_area = QScrollArea()
        gpio_scroll_area.setWidget(groupBox)
        gpio_scroll_area.setWidgetResizable(True)
        gpio_scroll_area.setFixedHeight(400)


        topButtonsGridLayout = QGridLayout()
        topButtonsGridLayout.addWidget(QLabel("Choose Device:"), 0, 0, 1, 1)
        topButtonsGridLayout.addWidget(QComboBox(self), 1, 0, 1, 2)

        labels = []
        labels.append(QLabel("Device Name:"))
        labels.append(QLabel("Microcontroller:"))
        labels.append(QLabel("Firmware Version:"))
        labels.append(QLabel("Address:"))

        for lbl in labels:
            lbl.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        topButtonsGridLayout.addWidget(labels[0], 0, 2, 1, 1)
        topButtonsGridLayout.addWidget(labels[1], 1, 2, 1, 1)
        topButtonsGridLayout.addWidget(labels[2], 2, 2, 1, 1)
        topButtonsGridLayout.addWidget(labels[3], 0, 4, 1, 1)

        topButtonsGridLayout.addWidget(QLineEdit(self), 0, 3, 1, 1)
        topButtonsGridLayout.addWidget(QLineEdit(self), 0, 5, 1, 1)

        topButtonsGridLayout.addWidget(QPushButton("Disconnect"),       0, 6, 1, 1)
        topButtonsGridLayout.addWidget(QPushButton("Commit to EEPROM"), 1, 6, 1, 1)

        topButtonsGridLayout.addWidget(QLabel("Atmega32U4"), 1, 3, 1, 1)
        topButtonsGridLayout.addWidget(QLabel("2"),          2, 3, 1, 1)

        gui_device_layout = QVBoxLayout(self)
        gui_device_layout.addLayout(topButtonsGridLayout)
        gui_device_layout.addWidget(gpio_scroll_area)


        self.show()
App = QApplication(sys.argv)
window = Window(30)
sys.exit(App.exec())
