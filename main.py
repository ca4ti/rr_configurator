from PyQt5 import QtWidgets, QtSerialPort
from PyQt5.QtCore import QObject, QThread, QIODevice, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton
import sys
import gui_device, gui_serial_select, rr_device, ser
import time, threading


class Worker(QObject):
    finished = pyqtSignal()
    update = pyqtSignal(int)


    @pyqtSlot()
    def procCounter(self): # A slot takes no params
        for i in range(1, 100):
            time.sleep(0.1)
            self.update.emit(i)

        self.finished.emit()

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(2000, 200, 1024, 768)
        self.setWindowTitle("this is the title")

        self.ser = ser.SerialConnection(self)
        

        self.current_device = None # rr_device.RR_Device()

        self.device_page = gui_device.GUI_DevicePage(self)
        self.connect_page = gui_serial_select.GUI_SerialSelectPage(self)

        self.connect_page.show()
        # threading.Timer(1, self.main_loop).start()
        # self.clicked_btn("bobby")

        # Init Update Thread
        self.obj = Worker()
        self.thread = QThread()
        self.obj.update.connect(self.update)
        self.obj.moveToThread(self.thread)
        self.obj.finished.connect(self.thread.quit)
        self.thread.started.connect(self.obj.procCounter)
        self.thread.start()

    def main_loop(self):
        print(self.current_device)

        threading.Timer(.1, self.main_loop).start()

    def reset(self, error=""):
        self.device_page.hide()
        self.current_device = None
        self.ser.close()
        self.connect_page.show()
        self.connect_page.set_error_message(error)

    def commit_to_eeprom(self):
        self.ser.commit_to_eeprom()

    def update(self):
        self.ser.update()

        pass

    def on_handshake_failed(self):
        self.connect_page.show()

    def init_device(self, data):
        self.current_device = rr_device.RR_Device()
        self.current_device.init_from_header(data)
        print(self.current_device.__dict__)
        self.device_page.show()

    def send_gpio_config_update(self, gpio_index):
        self.ser.send_gpio_config_update(gpio_index)

    

app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec_())