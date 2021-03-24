from PyQt5 import QtWidgets, QtSerialPort
from PyQt5.QtCore import Qt, QObject, QThread, QIODevice, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QMenuBar
import sys
import gui_device, gui_serial_select, rr_device, ser
import time, threading

QtWidgets.QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True) #enable highdpi scaling
QtWidgets.QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True) #use highdpi icons



class Worker(QObject):
    finished = pyqtSignal()
    update = pyqtSignal(int)


    @pyqtSlot()
    def procCounter(self): # A slot takes no params
        count = 0
        while True:
            time.sleep(0.1)
            self.update.emit(count)
            count+=1

        self.finished.emit()

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 760, 600)
        self.setWindowTitle("RealRobots Configurator")


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

    def send_device_name_update(self, new_name):
        self.ser.send_device_name_update(new_name)

    def send_device_address_update(self, new_address):
        self.ser.send_device_address_update(new_address)

    def commit_to_eeprom(self):
        self.ser.commit_to_eeprom()

    def select_sub_device(self, sub_device_index):
        self.ser.select_sub_device(sub_device_index)

    def update(self):
        self.ser.update()

        pass

    def on_handshake_failed(self):
        self.connect_page.show()

    def show_device_page(self):        
        self.device_page.show()

    def init_device(self, data):
        self.current_device = rr_device.RR_Device()
        self.current_device.init_from_header(data)
        print(self.current_device.__dict__)

    def init_sub_device(self, data):
        sub_device = rr_device.RR_Device()
        sub_device.init_from_header(data)
        self.current_device.add_sub_device(sub_device)
        print(data)

    def send_gpio_config_update(self, gpio_index):
        self.ser.send_gpio_config_update(gpio_index)

    def request_device_config(self, sub_device_index):
        self.ser.request_device_config(sub_device_index)

    def create_menu_bar(self):
        self.menuBar = QMenuBar(self)
        self.setMenuBar(self.menuBar)



    

app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec_())