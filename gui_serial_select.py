from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QPushButton, QLabel, QComboBox
import ser

class GUI_SerialSelectPage():
    def __init__(self, win):
        self.win = win
        self.controls = {}
        self.offset = [10, 10]
        self.ygap = 30
        

        widget = QLabel(self.win)
        widget.setText("Choose Serial Port:")
        widget.move(self.offset[0]+2, self.offset[1])
        widget.hide()
        self.controls["desc"] = widget

        widget = QComboBox(self.win)
        widget.move(self.offset[0]+1, self.offset[1]+20)
        widget.hide()
        self.controls["choose_port"] = widget

        widget = QPushButton("Refresh", self.win)
        widget.move(self.offset[0]+80, self.offset[1]+20)
        widget.clicked.connect(self.refresh_com_ports)
        widget.hide()
        self.controls["refresh"] = widget

        widget = QPushButton("Connect", self.win)
        widget.move(self.offset[0]+0, self.offset[1]+45)
        widget.clicked.connect(self.connect)
        widget.hide()
        self.controls["connect_to_port"] = widget

        widget = QLabel(self.win)
        widget.setText("Try Again")
        widget.move(self.offset[0]+82, self.offset[1]+50)        
        self.controls["warning"] = widget
        widget.hide()
        

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