import sys
from PyQt5.QtWidgets import QApplication, QAbstractItemView, QVBoxLayout, QFrame, QWidget, QLabel, QGridLayout, QPushButton, QComboBox
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import pyqtSlot
from functools import partial
import constant

class GUI_ButtonMatrixPage():
    def __init__(self, win):
        self.win = win
        self.frame = QFrame()
        # self.grid.show()

        self.selected_input_assignment = 0

    def init_matrix_gui(self):
        self.grid = QGridLayout()

        device = self.win.current_device


        self.grid.addWidget(QLabel("R"), 4, 0, 1, 1)
        self.grid.addWidget(QLabel("O"), 5, 0, 1, 1)
        self.grid.addWidget(QLabel("W"), 6, 0, 1, 1)
        self.grid.addWidget(QLabel("S"), 7, 0, 1, 1)

        self.grid.addWidget(QLabel("C"), 0, 6, 1, 1)
        self.grid.addWidget(QLabel("O"), 0, 7, 1, 1)
        self.grid.addWidget(QLabel("L"), 0, 8, 1, 1)
        self.grid.addWidget(QLabel("U"), 0, 9, 1, 1)
        self.grid.addWidget(QLabel("M"), 0, 10, 1, 1)
        self.grid.addWidget(QLabel("N"), 0, 11, 1, 1)
        self.grid.addWidget(QLabel("S"), 0, 12, 1, 1)

        self.input_assignment_combo_box = QComboBox()
  
        # setting geometry of combo box
        self.input_assignment_combo_box.setGeometry(200, 150, 120, 30)
        self.input_assignment_combo_box.activated[str].connect(self.on_assigned_input_combo_change)

    
        # adding list of items to combo box
        self.input_assignment_combo_box.addItems(constant.list_assigned_input)


        for y in range(0, 17):
            for x in range(0, 17):
                if (x == 0 and y == 0):
                    #self.grid.addWidget(widget, y, x*2)
                    pass

                elif x == 0 and y >= 0:
                    widget = QComboBox()
                    self.grid.addWidget(widget, y+2, x*2+1, 1, 3)
                    device.widgets["matrix_row_label_" + str(y-1)] = widget
                    widget.addItem("N/A")
                    for m in range(0, len(device.get_pin_label_list())):
                        widget.addItem(device.get_pin_label_list()[m])
                    
                    widget.activated[str].connect(partial(self.on_row_pin_assignment_combo_change, y, "matrix_row_label_" + str(y-1)))

                    

                elif x >= 0 and y == 0:
                    widget = QComboBox()
                    self.grid.addWidget(widget, 1, x*2+2, 1, 2)
                    device.widgets["matrix_col_label_" + str(x-1)] = widget
                    widget.addItem("N/A")
                    for m in range(0, len(device.get_pin_label_list())):
                        widget.addItem(device.get_pin_label_list()[m])

                    widget.activated[str].connect(partial(self.on_col_pin_assignment_combo_change, x, "matrix_col_label_" + str(x-1)))

                else:
                    widget = QLabel("0")
                    self.grid.addWidget(widget, y+2, x*2+2)
                    # device.widgets["matrix_val_" + str(x-1) + "," + str(y-1)] = widget
                    device.matrix_state_widgets.append(widget)

                    widget = QPushButton("Button 1")
                    #widget.setFont(QFont('Condensed', 6.5))
                    self.grid.addWidget(widget, y+2, x*2+3)
                    # device.widgets["matrix_assignment_" + str(x-1) + "," + str(y-1)] = widget
                    device.matrix_assignment_widgets.append(widget)
                    widget.pressed.connect(partial(self.open_select_input_combo, x, y))


        #self.grid.parent = self.layout
        self.frame.setFixedHeight(444)
        self.frame.setFixedWidth(900)
        self.frame.setLayout(self.grid)

    def open_select_input_combo(self, x, y):
        x = x-1
        y = y-1
        self.selected_input_assignment = y*16+x    

        self.input_assignment_combo_box.setCurrentIndex(self.win.current_device.get_matrix_assignment(y*16+x))    
        # showing the pop up
        self.input_assignment_combo_box.showPopup()

    
    def on_assigned_input_combo_change(self):
        idx = self.selected_input_assignment
        assignment = self.input_assignment_combo_box.currentIndex()
        
        self.win.current_device.set_matrix_assignment(idx, assignment)   
        self.UpdateMatrixGUIValues()


        print("setting matrix: " + str(idx) + " to " + str(assignment))
        self.win.send_button_matrix_config_update([])

    def on_row_pin_assignment_combo_change(self, row, widget_name):
        print("row: " + str(row) + ", " + widget_name)

        row -= 1
        pinIdx = self.win.current_device.widgets[widget_name].currentIndex()-1
        # pinIdx -= 1
        if pinIdx < 0: 
            pinIdx = 254

        old_pin = self.win.current_device.get_matrix_row_pin(row)
        self.win.current_device.set_matrix_row_pin(row, pinIdx)

        if (not self.pin_is_in_matrix(old_pin)):
            self.win.current_device.gpios[old_pin].pin_mode = constant.INPUT

        self.win.current_device.set_reserved_pin(pinIdx)   
        self.win.device_page.update_gpio_controls()    

        

        self.win.send_button_matrix_config_update([old_pin, pinIdx])

    def on_col_pin_assignment_combo_change(self, col, widget_name):
        print("col: " + str(col) + ", " + widget_name)

        col -= 1
        pinIdx = self.win.current_device.widgets[widget_name].currentIndex()-1
        # pinIdx -= 1
        if pinIdx < 0: 
            pinIdx = 254

        old_pin = self.win.current_device.get_matrix_col_pin(col)
        self.win.current_device.set_matrix_col_pin(col, pinIdx)

        if (not self.pin_is_in_matrix(old_pin)):
            self.win.current_device.gpios[old_pin].pin_mode = constant.INPUT
        
        self.win.current_device.set_reserved_pin(pinIdx)
        self.win.device_page.update_gpio_controls()    

        
        self.win.send_button_matrix_config_update([old_pin, pinIdx])

    def pin_is_in_matrix(self, pin):
        for i in range(0, 16):
            if self.win.current_device.get_matrix_row_pin(i) == pin:
                return True
            if self.win.current_device.get_matrix_col_pin(i) == pin:
                return True
        return False

    def UpdateMatrixGUIValues(self):
        print("GUI UPDATE")
        device = self.win.current_device
        for row in range(0, 16):       
            if device.get_matrix_row_pin(row) > 32:
                device.widgets["matrix_row_label_" + str(row)].setCurrentIndex(0)
            else:     
                device.widgets["matrix_row_label_" + str(row)].setCurrentIndex(device.get_matrix_row_pin(row)+1)

        for col in range(0, 16):    
            #print(str(device.get_matrix_col_pin(col)+1))        
            if device.get_matrix_col_pin(col) > 32:
                #print(">32")
                device.widgets["matrix_col_label_" + str(col)].setCurrentIndex(0)
            else:     
                #print("else")
                device.widgets["matrix_col_label_" + str(col)].setCurrentIndex(device.get_matrix_col_pin(col)+1)
           
        for x in range(0, 256):
            device.matrix_state_widgets[x].setText(str(0))
            device.matrix_assignment_widgets[x].setText(constant.list_assigned_input_short[device.get_matrix_assignment(x)])
        

    def hide(self):
        self.frame.hide()

    def show(self):
        self.frame.show()
