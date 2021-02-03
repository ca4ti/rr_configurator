INPUT = 0
OUTPUT = 1
INPUT_PULLUP = 2

NOAXIS = 0
XAXIS = 1
YAXIS = 2
ZAXIS = 3
XROTATION = 4
YROTATION = 5
ZROTATION = 6

RUDDERAXIS = 7
THROTTLEAXIS = 8
ACCELERATORAXIS = 9
BRAKEAXIS = 10
STEERINGAXIS = 11

ANALOG = 1
DIGITAL = 0

ID_PACKET_LENGTH = 23
GPIO_CONFIG_LENGTH = 13  # length for each gpio config

# Incoming serial leading bytes
HEADER_INPUT_CONFIG = "C"
HEADER_INPUT_VALUES = 84
HEADER_DEVICE_ID = "Q"
HEADER_HELP = "H"
HEADER_HANDSHAKE_RESPONSE = 73
HEADER_ID_RESPONSE = 77
HEADER_REQUEST_GPIO_CONFIG_RESPONSE = 81
HEADER_SEND_GPIO_CONFIG_UPDATE_RESPONSE = 83

# Outgoing serial leading bytes
HEADER_HANDSHAKE = 74
HEADER_REQUEST_ID = 76
HEADER_REQUEST_GPIO_CONFIG = 80  # subdevice address should follow
HEADER_SEND_GPIO_CONFIG_UPDATE = 82  # single gpio update to device


list_device_types = ["UNKNOWN", "ATmega328", "ATmega32U4", "ATmega2560"]

list_input_modes = ["INPUT", "OUTPUT", "INPUT_PULLUP"]

list_analog_modes = ["DIGITAL", "ANALOG"]

pro_micro_pin_label = ["A0", "A1", "A2", "A3", "A6", "A7", "A8", "A9", "A10", "D2", "D3", "D5", 
                       "D7", "D14", "D15", "D16"]

pro_micro_pin_idx = [18, 19, 20, 21, 24, 25, 26, 27, 28, 2,  3,  5,
                     7, 14, 15, 16]

list_assigned_input = ["NONE", "XAXIS", "YAXIS", "ZAXIS", "XROTATION", "YROTATION", "ZROTATION", "RUDDER", 
                       "THROTTLE", "ACCELERATOR", "BRAKE", "STEERING", "BUTTON1", "BUTTON2", "BUTTON3", 
                       "BUTTON4", "BUTTON5", "BUTTON6", "BUTTON7", "BUTTON8", "BUTTON9", "BUTTON10", 
                       "BUTTON11", "BUTTON12", "BUTTON13", "BUTTON14", "BUTTON15", "BUTTON16",
                       "BUTTON17", "BUTTON18", "BUTTON19", "BUTTON20", "BUTTON21", "BUTTON22",
                       "BUTTON23", "BUTTON24", "BUTTON25", "BUTTON26", "BUTTON27", "BUTTON28",
                       "BUTTON29", "BUTTON30", "BUTTON31", "BUTTON32"]


def pin_label_to_idx(pin_label):
    for i in range(0, len(pro_micro_pin_label)):
        if pin_label == pro_micro_pin_label[i]:
            return pro_micro_pin_idx[i]
    return -1

def pin_idx_to_label(pin_idx):
    for i in range(0, len(pro_micro_pin_idx)):
        if pin_idx == pro_micro_pin_idx[i]:
            return pro_micro_pin_label[i]
    return -1

def index_of(word, array):
    for i in range(0, len(array)):
        if word == array[i]:
            return i
    return -1

def int_to_2_bytes(x):
    highByte = (x >> 8) & 0xff
    lowByte = x & 0xff
    return [highByte, lowByte]