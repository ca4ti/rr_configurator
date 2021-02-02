from PyQt5 import QtWidgets, QtSerialPort
from PyQt5.QtCore import QObject, QThread, QIODevice, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton
import sys
import gui_device, gui_serial_select, rr_device, ser
import time 


    

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(2000, 200, 1024, 768)
        self.setWindowTitle("this is the title")

        self.ser = ser.SerialConnection(self)
        

        self.current_device = rr_device.RR_Device()

        self.device_page = gui_device.GUI_DevicePage(self)
        self.connect_page = gui_serial_select.GUI_SerialSelectPage(self)

        self.connect_page.show()
        # self.clicked_btn("bobby")


    def clicked_btn(self, arg):
        print("don't do that " + str(arg))

        if (arg == "bobby"):
            self.device_page.init_device_controls()
            print("added controls")

    

app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec_())