from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QPushButton, QLabel, QComboBox, QGridLayout, QWidget
import ser

class GUI_SerialSelectPage():
    def __init__(self, win):
        self.win = win
        self.controls = {}
        self.offset = [10, 10]
        self.ygap = 30
        
        self.w = QWidget(self.win)
        self.layout = QGridLayout(self.w)

        widget = QLabel()
        widget.setText("Choose Serial Port:")
        self.layout.addWidget(widget, 0, 0)
        self.controls["desc"] = widget

        widget = QComboBox()
        self.layout.addWidget(widget, 1, 0)
        self.controls["choose_port"] = widget

        widget = QPushButton("Refresh")
        self.layout.addWidget(widget, 1, 1)
        widget.clicked.connect(self.refresh_com_ports)
        self.controls["refresh"] = widget

        widget = QPushButton("Connect")
        self.layout.addWidget(widget, 2, 0, 1, 1)
        widget.clicked.connect(self.connect)
        self.controls["connect_to_port"] = widget

        widget = QLabel()
        widget.setText("Try Again")
        self.layout.addWidget(widget, 2, 3, 1, 1)     
        self.controls["warning"] = widget

        self.w.show()

    def refresh_com_ports(self):
        print("refresh com ports")
        ports = ser.get_serial_ports()
        self.controls["choose_port"].clear()
        for i in range(0, len(ports)):
            print(ports[i])
            self.controls["choose_port"].addItem(ports[i])

    def connect(self):
        selected_port = self.controls["choose_port"].currentText()
        if selected_port == "":
            self.controls["warning"].setText("invalid selection")
            self.controls["warning"].show()    

        self.win.ser.try_connect(selected_port)    

        self.hide()

    def set_error_message(self, message):
        self.controls["warning"].setText(message)
        self.controls["warning"].show()    

    def hide(self):
        self.controls["desc"].hide()
        self.controls["choose_port"].hide()
        self.controls["refresh"].hide()
        self.controls["connect_to_port"].hide()
        self.controls["warning"].hide()

    def show(self):
        self.refresh_com_ports()
        self.controls["desc"].show()
        self.controls["choose_port"].show()
        self.controls["refresh"].show()
        self.controls["connect_to_port"].show()
        self.controls["warning"].hide()