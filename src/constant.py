INPUT = 0               # 1  ESP32 Values
OUTPUT = 1              # 2
INPUT_PULLUP = 2        # 5
RESERVED = 3            # reserved for button matrix or other special function
UNKNOWN = 4

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
BUTTON_MATRIX_CONFIG_LENGTH = 288

# Incoming serial leading bytes
HEADER_INPUT_VALUES = 84
HEADER_HANDSHAKE_RESPONSE = 73
HEADER_ID_RESPONSE = 77
HEADER_REQUEST_GPIO_CONFIG_RESPONSE = 81
HEADER_SEND_GPIO_CONFIG_UPDATE_RESPONSE = 83
HEADER_SEND_MATRIX_CONFIG_UPDATE_RESPONSE = 93
HEADER_RECEIVE_TEXT_MESSAGE = 86

# Outgoing serial leading bytes
HEADER_HANDSHAKE = 74
HEADER_REQUEST_ID = 76
HEADER_REQUEST_GPIO_CONFIG = 80  # subdevice address should follow
HEADER_SEND_GPIO_CONFIG_UPDATE = 82  # single gpio update to device
HEADER_SEND_BUTTON_MATRIX_CONFIG_UPDATE = 92  # full button matrix config
HEADER_COMMIT_TO_EEPROM = 85
HEADER_RESET_TO_DEFAULTS = 72
HEADER_SELECT_SUB_DEVICE = 87
HEADER_UPDATE_DEVICE_NAME = 89
HEADER_UPDATE_DEVICE_ADDRESS = 91


list_device_types = ["UNKNOWN", "ATmega328", "ATmega32U4", "ATmega2560", "ESP32", "RP2040"]

list_input_modes = ["INPUT", "OUTPUT", "INPUT_PULLUP", "RESERVED"]#, "ENCODER0_A", "ENCODER0_B"]

list_analog_modes = ["DIGITAL", "ANALOG"]

pro_micro_pin_label = ["A0", "A1", "A2", "A3", "D4", "D6", "D8", "D9", "D10", "D2", "D3", "D5", 
                       "D7", "D14", "D15", "D16"]

pro_micro_pin_idx = [18, 19, 20, 21, 4, 6, 8, 9, 10, 2,  3,  5,
                     7, 14, 15, 16]

esp32_pin_label = ["4", "5", "13", "14", "15", "16", "17", "18", "19", "23", "25", "26", "27", "32", "33", "34"]
esp32_pin_idx = [4, 5, 13, 14, 15, 16, 17, 18, 19, 23, 25, 26, 27, 32, 33, 34]

rp2040_pin_label = ["2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","26","27","28"]
rp2040_pin_idx = [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,26,27,28]

mega2560_pin_label = ["A0","A1","A2","A3","A4","A5","A6","A7","A8","A9","A10","A11","A12","A13","A14","A15","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","48","49","50","51","52","53"]
mega2560_pin_idx   = [54,55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53]

atmega328p_pin_label = ["A0","A1","A2","A3","A4","A5", "2","3","4","5","6","7","8","9","10","11","12","13"]
atmega328p_pin_idx =   [14, 15, 16, 17, 18, 19, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

list_assigned_input = ["NONE", "XAXIS", "YAXIS", "ZAXIS", "XROTATION", "YROTATION", "ZROTATION", "SLIDER0", 
                       "SLIDER1", "!RESERVED!", "!RESERVED!", "!RESERVED!",
                       "HAT1_N", "HAT1_NE", "HAT1_E", "HAT1_SE", "HAT1_S", "HAT1_SW", "HAT1_W", "HAT1_NW",
                       "HAT2_N", "HAT2_NE", "HAT2_E", "HAT2_SE", "HAT2_S", "HAT2_SW", "HAT2_W", "HAT2_NW",
                       "HAT3_N", "HAT3_NE", "HAT3_E", "HAT3_SE", "HAT3_S", "HAT3_SW", "HAT3_W", "HAT3_NW",
                       "HAT4_N", "HAT4_NE", "HAT4_E", "HAT4_SE", "HAT4_S", "HAT4_SW", "HAT4_W", "HAT4_NW"]

list_assigned_input_short = ["NONE", "XAXIS", "YAXIS", "ZAXIS", "XROT", "YROT", "ZROT", "SLDR0", 
                       "SLDR1", "!RSVD!", "!RSVD!", "!RSVD!",
                       "H1_N", "H1_NE", "H1_E", "H1_SE", "H1_S", "H1_SW", "H1_W", "H1_NW",
                       "H2_N", "H2_NE", "H2_E", "H2_SE", "H2_S", "H2_SW", "H2_W", "H2_NW",
                       "H3_N", "H3_NE", "H3_E", "H3_SE", "H3_S", "H3_SW", "H3_W", "H3_NW",
                       "H4_N", "H4_NE", "H4_E", "H4_SE", "H4_S", "H4_SW", "H4_W", "H4_NW"]


def get_pin_label_count(microcontroller):
    if microcontroller == 0:
        return 0
    elif microcontroller == 1:
        return len(atmega328p_pin_idx)
    elif microcontroller == 2:
        return len(pro_micro_pin_idx)
    elif microcontroller == 3:
        return len(mega2560_pin_idx)
    elif microcontroller == 4:
        return len(esp32_pin_idx)
    elif microcontroller == 5:
        return len(rp2040_pin_idx)

# Add BUTTON1..128 to list_assigned_input
for i in range(1, 129):
    list_assigned_input.append("BUTTON" + str(i))
    list_assigned_input_short.append("BTN" + str(i))


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