
from PyQt5 import QtWidgets, QtSerialPort
from PyQt5.QtCore import QObject, QThread, QIODevice, pyqtSignal, QByteArray
from enum import Enum
import sys, glob, serial, time
import constant

class SerAction(Enum):
    DISCONNECTED = 0
    WAITING_ON_HANDSHAKE = 1 
    CONNECTED = 2
    WAITING_ON_GPIO_CONFIG = 3

HANDSHAKE_TIMEOUT = 1
class SerialConnection:
    def __init__(self, interface):
        self.action = SerAction.DISCONNECTED
        self.actionStartTime = 0
        self.win = interface

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
        
        self.serial.write((chr(constant.HEADER_HANDSHAKE) + "\r\n").encode())
        self.start_action(SerAction.WAITING_ON_HANDSHAKE)
        
    def start_action(self, action):
        self.action = action
        self.actionStartTime = time.time()

    def on_handshake_failed(self):
        self.start_action(SerAction.DISCONNECTED)
        print("connection failed")
        self.serial.close()
        self.win.reset("ERROR: Handshake failed (is it the correct port?)")

    def close(self):
        self.serial.close()

    def receive(self):
        #print("received")
        while self.serial.canReadLine():
            text = self.serial.readLine().data()
            #print(text)
            
            if text[0] == constant.HEADER_INPUT_VALUES:
                self.decode_gpio_input_values(text)
            elif text[0] == constant.HEADER_HANDSHAKE_RESPONSE:
                print("GOT A RESPONSE")
                self.start_action(SerAction.CONNECTED)
                self.serial.write((chr(constant.HEADER_REQUEST_ID) + "\r\n").encode())
            
            elif text[0] == constant.HEADER_ID_RESPONSE:
                print("GOT device name resonpose")
                self.decode_id_packet(text)

                #self.start_action(SerAction.CONNECTED)

            elif text[0] == constant.HEADER_REQUEST_GPIO_CONFIG_RESPONSE:
                print("received config")
                print(len(text))
                self.decode_gpio_config_packet(text)

            elif text[0] == constant.HEADER_SEND_GPIO_CONFIG_UPDATE_RESPONSE:
                print("received config update confirmation")
                print(len(text))
                cnt = 0
                for t in text:
                    print(str(cnt) + "\t" + str(t))
                    cnt += 1
                #self.decode_gpio_config_packet(text)

            #text = text.rstrip('\r\n')
            


    def update(self):
        if self.action == SerAction.WAITING_ON_HANDSHAKE:
            if time.time() - self.actionStartTime > HANDSHAKE_TIMEOUT:
                self.on_handshake_failed()

    def commit_to_eeprom(self):        
        ba = bytearray()
        ba.append(constant.HEADER_COMMIT_TO_EEPROM)
        
        ba.append(0)  # address
        ba.append(ord('\r'))
        ba.append(ord('\n'))  # 18 bytes

        b = bytes(ba)
        self.serial.write(b)
        self.start_action(SerAction.CONNECTED)


    def decode_id_packet(self, data):
        if len(data) != constant.ID_PACKET_LENGTH:
            print("ERROR: Incorrect ID packet length " + str(len(data)))
            print(data)
            self.win.reset("ERROR: Incorrect ID packet length: " + str(len(data)))
            return

        device = {}
        device["device_name"] = data[1: 1+16].decode()
        device["firmware_version"] = data[17]
        device["device_type"] = data[18]
        device["sub_device_count"] = data[19]
        device["address"] = data[20]

        self.win.init_device(device)
        ba = QByteArray()
        ba.append(chr(constant.HEADER_REQUEST_GPIO_CONFIG))
        ba.append(str(chr(0)))
        # ba[0] = 1#(chr(constant.HEADER_REQUEST_GPIO_CONFIG))
        # ba[1] = 0
        ba.append('\r')
        ba.append('\n')
        self.serial.write(ba)
        self.start_action(SerAction.WAITING_ON_GPIO_CONFIG)

    def decode_gpio_input_values(self, data):
        current_byte = 1
        if self.win.current_device == None:
            return

        if len(data) < len(self.win.current_device.gpios)*4 + 3:
            print("incorrect number of bytes: " + str(len(data)))
            
            cnt = 0
            for t in data:
                print(str(cnt) + "\t" + str(t))
                cnt += 1
            return

        for i in range(0, len(self.win.current_device.gpios)):
            gpio = self.win.current_device.gpios[i]

            gpio.raw_val = data[current_byte] << 8
            gpio.raw_val += data[current_byte+1]
            current_byte += 2            

            gpio.calibrated_value = data[current_byte] << 8
            gpio.calibrated_value += data[current_byte+1]
            current_byte += 2

        self.win.device_page.update_gpio_controls_values()

    def decode_gpio_config_packet(self, data):
        if len(data) != len(self.win.current_device.gpios) * constant.GPIO_CONFIG_LENGTH + 4:
            print("ERROR: Incorrect GPIO Config packet length " + str(len(data)))
            self.win.reset("ERROR: Incorrect GPIO Config packet length: " + str(len(data)))
            return

        current_byte = 1 #skip header byte
        input_count = data[current_byte]
        if input_count != len(self.win.current_device.gpios):
            print("ERROR: Incorrect GPIO count " + str(len(self.win.current_device.gpios)))
            self.win.reset("ERROR: Incorrect GPIO count: " + str(len(self.win.current_device.gpios)))
            return

        current_byte += 1  # first byte of first gpio config
        for i in range(0, input_count):
            gpio = self.win.current_device.gpios[i]
            
            #  current_gpio.pin_number = data[current_byte]
            current_byte += 1
            gpio.pin_mode = data[current_byte]
            current_byte += 1
            gpio.is_analog = data[current_byte]
            current_byte += 1
            gpio.is_inverted = data[current_byte]
            current_byte += 1
            gpio.min_val = data[current_byte] << 8
            gpio.min_val += data[current_byte+1]
            current_byte += 2
            gpio.mid_val = data[current_byte] << 8
            gpio.mid_val += data[current_byte+1]
            current_byte += 2
            gpio.max_val = data[current_byte] << 8
            gpio.max_val += data[current_byte+1]
            current_byte += 2
            gpio.dead_zone = data[current_byte] << 8
            gpio.dead_zone += data[current_byte+1]
            current_byte += 2
            gpio.assigned_input = data[current_byte]
            current_byte += 1

        self.win.device_page.update_gpio_controls()


    def send_gpio_config_update(self, gpio_index):
        print("sedning... " + str(gpio_index))
        gpio = self.win.current_device.gpios[gpio_index]

        # ba = QByteArray()
        # ba.append(chr(constant.HEADER_SEND_GPIO_CONFIG_UPDATE))

        #b = bytes([constant.HEADER_SEND_GPIO_CONFIG_UPDATE, 0, 100, 180, 255, 13, 10])
        ba = bytearray()
        ba.append(constant.HEADER_SEND_GPIO_CONFIG_UPDATE)
        
        ba.append(0)  # address
        ba.append(gpio.gpio_index)  # 2
        ba.append(gpio.pin_number)  # 3
        ba.append(gpio.pin_mode)    # 4
        ba.append(gpio.is_analog)
        ba.append(gpio.is_inverted)
        ba.append(constant.int_to_2_bytes(gpio.min_val)[0])     
        ba.append(constant.int_to_2_bytes(gpio.min_val)[1])
        ba.append(constant.int_to_2_bytes(gpio.mid_val)[0])
        ba.append(constant.int_to_2_bytes(gpio.mid_val)[1])
        ba.append(constant.int_to_2_bytes(gpio.max_val)[0])
        ba.append(constant.int_to_2_bytes(gpio.max_val)[1])
        ba.append(constant.int_to_2_bytes(gpio.dead_zone)[0])
        ba.append(constant.int_to_2_bytes(gpio.dead_zone)[1])
        ba.append(gpio.assigned_input)  # 15
        ba.append(ord('\r'))
        ba.append(ord('\n'))  # 18 bytes

        # print("BA>LENGTH")
        # print(ba.length())
        b = bytes(ba)
        self.serial.write(b)
        self.start_action(SerAction.CONNECTED)


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

