
from PyQt5 import QtWidgets, QtSerialPort
from PyQt5.QtCore import QObject, QThread, QIODevice, pyqtSignal
import sys, glob, serial


class SerialConnection:
    def __init__(self, interface):
        self.serial = QtSerialPort.QSerialPort(
            '??',
            baudRate=115200,
            readyRead=self.receive
        )
        
        #print(self.serial)

    def try_connect(self, port):
        self.serial = QtSerialPort.QSerialPort(
            port,
            baudRate=115200,
            readyRead=self.receive
        )
        self.serial.open(QIODevice.ReadWrite)


    def receive(self):
        print("received")
        while self.serial.canReadLine():
            text = self.serial.readLine().data().decode()
            #text = text.rstrip('\r\n')
            print(text)
            #self.output_te.append(text)        

def to_string(packet_bytes):
    count = 0
    for b in packet_bytes:
        print(str(count) + ": " + str(b))
        count += 1


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

