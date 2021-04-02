from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication,QGridLayout, QComboBox, QWidget, QScrollArea, QVBoxLayout, QGroupBox, QLabel, QPushButton, QFormLayout
import sys
class Window(QWidget):
    def __init__(self, val):
        super().__init__()
        self.title = "PyQt5 Scroll Bar"
        self.top = 200
        self.left = 500
        self.width = 400
        self.height = 300
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)


        formLayout = QGridLayout()
        groupBox = QGroupBox("This Is Group Box")

        self.columnSpans = [1, 4, 4, 4, 1, 1, 2, 1, 1, 1, 4]
        

        for r in range(0, 10):
            widgets = []
            widget = QLabel(self)
            if r % 2 == 0:
                widget.setText("hi1asdfdasfdasfdasfads there")
            else:
                widget.setText("hi1here")
            widgets.append(widget)
            widget = QComboBox(self)
            widget.addItem("1")
            widget.addItem("2")
            widgets.append(widget)
            widget = QComboBox(self)
            widget.addItem("fasdfdsfd1")
            widget.addItem("2")
            widgets.append(widget)
            widget = QComboBox(self)
            widget.addItem("1")
            widget.addItem("2")
            widgets.append(widget)
            widget = QComboBox(self)
            widget.addItem("1")
            widget.addItem("2")
            widgets.append(widget)
            widget = QComboBox(self)
            widget.addItem("1")
            widget.addItem("2")
            widgets.append(widget)
            widget.addItem("1")
            widget.addItem("2")
            widgets.append(widget)
            widget.addItem("1")
            widget.addItem("2")
            widgets.append(widget)
            widget.addItem("1")
            widget.addItem("2")
            widgets.append(widget)

            for x in range(0, 9):
                formLayout.addWidget(widgets[x], r, x, 1, 1)

          device.widgets[""]
          device.widgets[""]  
          
          device.widgets[""] 
          device.widgets[""]
          device.widgets[""]
          device.widgets[""]
          device.widgets[""]
          device.widgets[""]
          device.widgets[""]
       
        groupBox.setLayout(formLayout)
        scroll = QScrollArea()
        scroll.setWidget(groupBox)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(400)
        layout = QVBoxLayout(self)
        layout.addWidget(scroll)


        self.show()
App = QApplication(sys.argv)
window = Window(30)
sys.exit(App.exec())