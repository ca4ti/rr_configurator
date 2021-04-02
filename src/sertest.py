from PyQt5 import QtWidgets, QtSerialPort
from PyQt5.QtCore import QObject, QThread, QIODevice, pyqtSignal, QByteArray

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QMenuBar

import sys, glob, serial, time
import time

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 860, 100)
        self.setWindowTitle("RealRobots Configurator")

        self.ser = SerialConnection(self)

        

class SerialConnection:
    def __init__(self, interface):
        #self.action = SerAction.DISCONNECTED
        self.actionStartTime = 0
        self.win = interface
        self.char_buffer = QByteArray()

        self.eol = QByteArray()
        self.eol.append("\r\n")
        

        self.serial = QtSerialPort.QSerialPort(
            '??',
            baudRate=115200,
            readyRead=self.receive
        )
        self.try_connect(get_serial_ports()[0])

    def try_connect(self, port):
        self.port = port
        self.serial = QtSerialPort.QSerialPort(
            port,
            baudRate=115200,
            readyRead=self.receive
        )
        self.serial.open(QIODevice.ReadWrite)
        print("connected")

        

    def receive(self):
        print("received")

        self.char_buffer += self.serial.readAll()
        #print(self.char_buffer)

        if self.char_buffer.contains(self.eol):
            idx = self.char_buffer.indexOf(self.eol)
            msg = self.char_buffer[0: idx]
            print(msg)
            print(self.char_buffer)
            self.char_buffer = self.char_buffer[idx+2: len(self.char_buffer)]
            print(self.char_buffer)


def get_serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
        
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except:
            pass
    return result   


app = QApplication(sys.argv)
app.setStyle('Breeze')
app.setStyleSheet("QGroupBox {border: none;}")
app.setStyleSheet("QScrollArea {border: none;}")
window = Window()
window.show()
sys.exit(app.exec_())