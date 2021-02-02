def __init__(self, port, theme='day', parent=None):
    super().__init__(parent)
    self.setFont(Font().load())
    self.setAcceptRichText(False)
    self.setReadOnly(False)
    self.setObjectName('replpane')
    # open the serial port
    self.serial = QSerialPort(self)
    self.serial.setPortName(port)
    if self.serial.open(QIODevice.ReadWrite):
        self.serial.setBaudRate(115200)
        self.serial.readyRead.connect(self.on_serial_read)
        # clear the text
        self.clear()
        # Send a Control-C
        self.serial.write(b'\x03')
    else:
        raise IOError("Cannot connect to device on port {}".format(port))
    self.set_theme(theme)