import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

import gui_button_matrix

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 860, 100)
        self.setWindowTitle("RealRobots Configurator")
        
        self.button_matrix_page = gui_button_matrix.GUI_ButtonMatrixPage(self)


app = QApplication(sys.argv)
app.setStyle('Breeze')
app.setStyleSheet("QGroupBox {border: none;}")
app.setStyleSheet("QScrollArea {border: none;}")
window = Window()
window.show()
sys.exit(app.exec_())