
from PyQt5 import QtWidgets, QtSerialPort
from PyQt5.QtCore import QObject, QThread, QIODevice, pyqtSignal, QByteArray
from enum import Enum
import sys
import glob
import serial
import time
import constant


class SerAction(Enum):
    DISCONNECTED = 0
    WAITING_ON_HANDSHAKE = 1
    CONNECTED = 2
    WAITING_ON_GPIO_CONFIG = 3
    WAITING_ON_GPIO_UPDATE_CONFIRMATION = 4
    WAITING_ON_MATRIX_UPDATE_CONFIRMATION = 5
    WAITING_ON_RESET_TO_DEFAULTS_CONFIRMATION = 6
    WAITING_ON_ENCODER_UPDATE_CONFIRMATION = 7


HANDSHAKE_TIMEOUT = 2


class SerialConnection:
    def __init__(self, interface):
        self.action = SerAction.DISCONNECTED
        self.actionStartTime = 0
        self.win = interface

        self.char_buffer = QByteArray()
        self.eol = QByteArray()
        self.eol.append("\r\n")

        self.queuedGPIOUpdates = []

        self.serial = QtSerialPort.QSerialPort(
            '??',
            baudRate=115200,
            readyRead=self.receive
        )

        # print(self.serial)

    def try_connect(self, port):
        self.port = port
        self.serial = QtSerialPort.QSerialPort(
            port,
            baudRate=115200,
            readyRead=self.receive
        )
        self.serial.open(QIODevice.ReadWrite)

        #self.serial.write((chr(constant.HEADER_HANDSHAKE) + "\r\n").encode())

        # ba = bytearray()
        # ba.append(ord('J'))

        # ba.append(ord('\r'))
        # ba.append(ord('\n'))

        # b = bytes(ba)
        # self.serial.write(b)

        self.start_action(SerAction.WAITING_ON_HANDSHAKE)
        self.handshake_tries = 0

    def start_action(self, action):
        print("Action: " + str(action))
        self.action = action
        self.actionStartTime = time.time()

    def on_handshake_failed(self):

        if self.handshake_tries > 3:
            self.start_action(SerAction.DISCONNECTED)
            print("connection failed")
            self.serial.close()
            self.win.reset("ERROR: Handshake failed (is it the correct port?)")
        else:
            self.handshake_tries += 1
            # self.serial.close()

            # self.serial = QtSerialPort.QSerialPort(
            #     self.port,
            #     baudRate=115200,
            #     readyRead=self.receive
            # )
            # self.serial.open(QIODevice.ReadWrite)
            # self.serial.write(
            #     (chr(constant.HEADER_HANDSHAKE) + "\r\n").encode())
            self.serial.write((chr(constant.HEADER_HANDSHAKE) + "\r\n").encode())
            self.start_action(SerAction.WAITING_ON_HANDSHAKE)

    def close(self):
        self.start_action(SerAction.DISCONNECTED)
        self.serial.close()

    def receive(self):
        
        self.char_buffer += self.serial.readAll()

        if self.char_buffer.contains(self.eol):
            idx = self.char_buffer.indexOf(self.eol)
            msg = self.char_buffer[0: idx+2]
            # print(msg)
            # print(self.char_buffer)
            self.char_buffer = self.char_buffer[idx+2: len(self.char_buffer)]
            # print(self.char_buffer)

            text = msg.data()  # self.serial.readLine().data()
            # print(text)
            # cnt = 0
            # for t in text:
            #     print(str(cnt) + "\t" + str(t))
            #     cnt += 1

            if text[0] == constant.HEADER_INPUT_VALUES:
                self.decode_gpio_input_values(text)
            elif text[0] == constant.HEADER_RECEIVE_TEXT_MESSAGE:
                print("Received text message from device")
                try:
                    print(text[1:len(text)].decode())
                except:
                    pass

                cnt = 0
                for t in text:
                    print(str(cnt) + "\t" + str(t) + "\t" + chr(t))
                    cnt += 1

            elif text[0] == constant.HEADER_HANDSHAKE_RESPONSE:
                print("Received Handshake from Device")
                self.start_action(SerAction.CONNECTED)
                print(text)
                self.serial.write(
                    (chr(constant.HEADER_REQUEST_ID) + "\r\n").encode())

            elif text[0] == constant.HEADER_ID_RESPONSE:
                print("Received Device ID Packet")
                self.decode_id_packet(text)

                # self.start_action(SerAction.CONNECTED)

            elif text[0] == constant.HEADER_RESET_TO_DEFAULTS:
                print("Received Reset to defaults confirmation")
                self.start_action(SerAction.CONNECTED)
                self.request_device_config(0)

            elif text[0] == constant.HEADER_REQUEST_GPIO_CONFIG_RESPONSE:
                print("Received config")
                print(len(text))
                self.decode_gpio_config_packet(text)
                self.start_action(SerAction.CONNECTED)

            elif text[0] == constant.HEADER_SEND_GPIO_CONFIG_UPDATE_RESPONSE:
                print("Received config update confirmation")
                print(len(text))
                cnt = 0
                for t in text:
                    print(str(cnt) + "\t" + str(t))
                    cnt += 1
                # self.decode_gpio_config_packet(text)
                self.start_action(SerAction.CONNECTED)                

            elif text[0] == constant.HEADER_SEND_MATRIX_CONFIG_UPDATE_RESPONSE:
                print("Received config update confirmation")
                print(len(text))
                cnt = 0
                for t in text:
                    print(str(cnt) + "\t" + str(t))
                    cnt += 1
                if len(self.queuedGPIOUpdates) == 0:
                    self.start_action(SerAction.CONNECTED)
                else:
                    self.send_gpio_config_update(self.queuedGPIOUpdates[0])
                    self.queuedGPIOUpdates.remove(self.queuedGPIOUpdates[0])

            else:
                print("unknown packet")
                print(text)
                cnt = 0
                for t in text:
                    print(str(cnt) + "\t" + str(t))
                    cnt += 1
            #text = text.rstrip('\r\n')

    def update(self):
        #print(str(time.time() - self.actionStartTime))
        if self.action == SerAction.WAITING_ON_HANDSHAKE:
            if time.time() - self.actionStartTime > HANDSHAKE_TIMEOUT:
                print("handshake timeout")
                self.on_handshake_failed()

        elif self.action == SerAction.WAITING_ON_GPIO_UPDATE_CONFIRMATION:

            if time.time() - self.actionStartTime > 0.2:
                print("config update failed")
                self.try_resend_config_update_packet()

        elif self.action == SerAction.WAITING_ON_ENCODER_UPDATE_CONFIRMATION:

            if time.time() - self.actionStartTime > 0.2:
                print("encoder config update failed")
                self.try_resend_encoder_update_packet()

        elif self.action == SerAction.WAITING_ON_MATRIX_UPDATE_CONFIRMATION:

            if time.time() - self.actionStartTime > 2:
                print("matrix config update failed")
                self.try_resend_matrix_config_update_packet()

        elif self.action == SerAction.WAITING_ON_RESET_TO_DEFAULTS_CONFIRMATION:

            if time.time() - self.actionStartTime > 5:
                print("reset to defaults timeout...")
                self.reset_to_defaults()

    def commit_to_eeprom(self):
        ba = bytearray()
        ba.append(constant.HEADER_COMMIT_TO_EEPROM)

        ba.append(ord('\r'))
        ba.append(ord('\n'))

        b = bytes(ba)
        self.serial.write(b)
        self.start_action(SerAction.CONNECTED)

    def reset_to_defaults(self):
        print("resettnig to defaults")
        ba = bytearray()
        ba.append(constant.HEADER_RESET_TO_DEFAULTS)

        ba.append(ord('\r'))
        ba.append(ord('\n'))

        b = bytes(ba)
        self.serial.write(b)
        self.start_action(SerAction.WAITING_ON_RESET_TO_DEFAULTS_CONFIRMATION)

    def send_device_name_update(self, new_name):
        if len(new_name) != 16:
            print("ERROR: name not 16 characters")
            return
        ba = bytearray()
        ba.append(constant.HEADER_UPDATE_DEVICE_NAME)
        for c in new_name:
            ba.append(ord(c))
        ba.append(ord('\r'))
        ba.append(ord('\n'))

        b = bytes(ba)
        self.serial.write(b)
        self.start_action(SerAction.CONNECTED)

    def send_device_address_update(self, new_address):
        ba = bytearray()
        ba.append(constant.HEADER_UPDATE_DEVICE_ADDRESS)
        ba.append(new_address)
        ba.append(ord('\r'))
        ba.append(ord('\n'))

        b = bytes(ba)
        self.serial.write(b)
        self.start_action(SerAction.CONNECTED)

    def request_device_config(self, sub_device_index):
        ba = QByteArray()
        ba.append(chr(constant.HEADER_REQUEST_GPIO_CONFIG))
        ba.append(str(chr(sub_device_index)))
        ba.append('\r')
        ba.append('\n')
        self.serial.write(ba)
        self.start_action(SerAction.WAITING_ON_GPIO_CONFIG)

    def select_sub_device(self, sub_device_index):
        ba = bytearray()
        ba.append(constant.HEADER_SELECT_SUB_DEVICE)

        ba.append(sub_device_index)  # address
        ba.append(ord('\r'))
        ba.append(ord('\n'))  # 18 bytes

        b = bytes(ba)
        self.serial.write(b)
        self.start_action(SerAction.CONNECTED)
        #print("changed subdevice selection to: " + str(sub_device_index))

    def decode_id_packet(self, data):
        print("************ Decoding ID Packet ******************")
        # if len(data) != constant.ID_PACKET_LENGTH:
        #     print("ERROR: Incorrect ID packet length " + str(len(data)))
        #     print(data)
        #     self.win.reset("ERROR: Incorrect ID packet length: " + str(len(data)))
        #     return
        # cnt = 0
        # for d in data:
        #     print(str(cnt) + ": " + str(d))
        #     cnt+=1

        device = {}
        device["device_name"] = data[1: 1+16].decode()
        device["firmware_version"] = data[17]
        device["device_type"] = data[18]
        device["address"] = data[19]
        device["sub_device_count"] = data[20]
        self.win.init_device(device)

        current_byte = 21
        for i in range(0, device["sub_device_count"]):
            current_byte = 21 + (19*i)
            sub_device = {}
            sub_device["device_name"] = data[current_byte: current_byte+16].decode()
            sub_device["firmware_version"] = data[current_byte+16]
            sub_device["device_type"] = data[current_byte+17]
            sub_device["address"] = data[current_byte+18]

            # current_byte += 20
            self.win.init_sub_device(sub_device)

        self.win.show_device_page()

        # continue to request gpio config for master device
        self.request_device_config(0)

    def decode_gpio_input_values(self, data):
        current_byte = 1
        if self.win.current_device == None:
            return

        if len(data) < len(self.win.current_device.gpios)*4 + 3:
            #print("incorrect number of bytes: " + str(len(data)))

            # cnt = 0
            # for t in data:
            #     print(str(cnt) + "\t" + str(t))
            #     cnt += 1
            return

        # cnt = 0
        # for t in data:
        #     print(str(cnt) + "\t" + str(t))
        #     cnt += 1

        for i in range(0, len(self.win.current_device.gpios)):
            if len(data) < current_byte + 9:
                continue

            gpio = self.win.current_device.gpios[i]

            gpio.raw_val = data[current_byte] << 8
            gpio.raw_val += data[current_byte+1]
            current_byte += 2

            gpio.calibrated_value = data[current_byte] << 8
            gpio.calibrated_value += data[current_byte+1]
            if gpio.calibrated_value > 32767:
                gpio.calibrated_value = gpio.calibrated_value - 32767*2
            current_byte += 2

        count = 0
        button_state = []
        for i in range(current_byte, len(data)-2):
            column = []
            for z in range(0, 8):
                column.append(data[current_byte] >> z & 1)
            button_state.append(column)


            #self.win.current_device.set_matrix_button_state(count, data[current_byte])
            # print(str(i) + "\t" + str(data[current_byte]))
            count += 1
            current_byte += 1

        self.win.current_device.set_matrix_button_state_all(button_state)
        #print(str(len(button_state)) + ", " + str(len(button_state[0])))

        self.win.device_page.update_gpio_controls_values()

    def decode_gpio_config_packet(self, data):
        expected_packet_len = len(self.win.current_device.gpios) * constant.GPIO_CONFIG_LENGTH + constant.BUTTON_MATRIX_CONFIG_LENGTH + 4
        # if len(data) != expected_packet_len:
        #     print("ERROR: Incorrect GPIO Config packet length " + str(len(data)))
        #     print("Should be: " + str(expected_packet_len))
        #     print(data)
        #     count = 0
        #     for d in data:
        #         print(str(count) + "\t" + str(d))
        #         count += 1
        #     self.win.reset(
        #         "ERROR: Incorrect GPIO Config packet length: " + str(len(data)))
        #     return

        # print("HERE IS THE DATA>>>")
        # print(data)

        current_byte = 1  # skip header byte
        input_count = data[current_byte]       
        
        # if gpio count doesn't match device count then config hasn't update yet
        if len(self.win.current_device.gpios) != input_count:
            print("Count doesn't match")
            self.win.current_device.init_gpios_forced(self.win.current_device.get_selected_device().microcontroller)
            #return

        # if input_count != len(self.win.current_device.gpios):
        #     print("ERROR: Incorrect GPIO count " +
        #           str(len(self.win.current_device.gpios)))
        #     self.win.reset("ERROR: Incorrect GPIO count: " +
        #                    str(len(self.win.current_device.gpios)))
        #     return

        current_byte += 1  # first byte of first gpio config
        print("RECEIVING CONFIG!!!")
        print("Inputs: " + str(len(self.win.current_device.gpios)))
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

        print("Receiving Encoder Config") # 4 groups of 10 bytes each
        for enc in range(0, 4):
            encoder = self.win.current_device.encoders[enc]
            encoder.set_pin_a(data[current_byte + 0])
            encoder.set_pin_b(data[current_byte + 1])
            encoder.set_left_assignment(data[current_byte + 2])
            encoder.set_right_assignment(data[current_byte + 3])
            print(str(enc) + " a:" + str(data[current_byte + 0])+ " b:" + str(data[current_byte + 1]))
            
            current_byte += 10

        print("Receiving Matrix Config")


        # Load Row Pins
        print("*** rows ***")
        for i in range(0, 16):            
            pin = data[current_byte]
            
            print(str(current_byte) + "\t" + str(data[current_byte]))
            self.win.current_device.set_matrix_row_pin(i, pin)

            current_byte += 1

        # Load Col Pins        
        print("*** cols ***")
        for i in range(0, 16):            
            pin = data[current_byte]
            print(str(current_byte) + "\t" + str(data[current_byte]))
            self.win.current_device.set_matrix_col_pin(i, pin)

            current_byte += 1

        # Load Button Assignments
        print("*** assignments ***")
        for i in range(0, 256):
            print(str(current_byte) + "\t" + str(data[current_byte]))
            self.win.current_device.set_matrix_assignment(
                i, data[current_byte])
            current_byte += 1

        # for y in range(0, 256):
        #     print(self.win.current_device.matrix_assignments[y])

    def send_gpio_config_update(self, gpio_index):
        print("Sending Config Update for gpio " + str(gpio_index))
        gpio = self.win.current_device.gpios[gpio_index]
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
        bstring = ""
        for b in ba:
            bstring += str(b) + '\t'
        print(bstring)

        b = bytes(ba)
        self.config_update_packet = b # store in case need to resend
        self.serial.write(b)
        self.start_action(SerAction.WAITING_ON_GPIO_UPDATE_CONFIRMATION)

    def send_encoder_config_update(self, encoder_index):
        print("Sending Config Update for encoder " + str(encoder_index))
        encoder = self.win.current_device.encoders[encoder_index]
        ba = bytearray()
        ba.append(constant.HEADER_SEND_ENCODER_CONFIG_UPDATE)
        ba.append(encoder_index)
        ba.append(encoder.get_pin_a())
        ba.append(encoder.get_pin_b())
        ba.append(encoder.get_left_assignment())
        ba.append(encoder.get_right_assignment())

        ba.append(0)
        ba.append(0)
        ba.append(0)
        ba.append(0)
        ba.append(0)
        ba.append(0)

        ba.append(ord('\r'))
        ba.append(ord('\n')) # 14 bytes total

        b = bytes(ba)
        self.config_update_packet = b # store in case need to resend
        self.serial.write(b)
        self.start_action(SerAction.WAITING_ON_ENCODER_UPDATE_CONFIRMATION)

    def try_resend_config_update_packet(self):
        self.serial.write(self.config_update_packet)
        self.start_action(SerAction.WAITING_ON_GPIO_UPDATE_CONFIRMATION)

    def try_resend_encoder_update_packet(self):
        self.serial.write(self.config_update_packet)
        self.start_action(SerAction.WAITING_ON_ENCODER_UPDATE_CONFIRMATION)

    def try_resend_matrix_config_update_packet(self):
        self.serial.write(self.config_update_packet)
        self.start_action(SerAction.WAITING_ON_MATRIX_UPDATE_CONFIRMATION)

    def send_button_matrix_config_update(self, changed_gpios):
        for i in range(0, len(changed_gpios)):
            if changed_gpios[i] == 254:
                continue
            else:
                self.queuedGPIOUpdates.append(changed_gpios[i])

        print("Sending Config Update for button matrix")
        device = self.win.current_device
        ba = bytearray()
        ba.append(constant.HEADER_SEND_BUTTON_MATRIX_CONFIG_UPDATE)
        
        for i in range(0, 16):
            pin = device.get_matrix_row_pin(i)
            print("send_row:" + str(pin))
            ba.append(pin)
        for i in range(0, 16):
            pin = device.get_matrix_col_pin(i)
            print("send_col:" + str(pin))
            ba.append(pin)
        for i in range(0, 256):
            ba.append(device.get_matrix_assignment(i))

        ba.append(ord('\r'))
        ba.append(ord('\n')) # 291 bytes total
        print("len: " + str(len(ba)))

        for i in range(0, len(ba)):
            print(str(i) + "\t" + str(ba[i]))
        b = bytes(ba)
        self.config_update_packet = b # store in case need to resend
        self.serial.write(b)
        self.start_action(SerAction.WAITING_ON_MATRIX_UPDATE_CONFIRMATION)


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
