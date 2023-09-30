import socket
import sqlite3
con = sqlite3.connect("tutorial.db")

UDP_IP = "127.0.0.1"
UDP_PORT_R = 65200
UDP_PORT_W = 5005

# print("UDP target IP: %s" % UDP_IP)
# print("UDP target port: %s" % UDP_PORT)
# print("message: %s" % MESSAGE)

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP


import sys

from PyQt5.QtCore import (
    QSize,
    Qt,
    QPoint,
    QRunnable,
    pyqtSlot,
    QThreadPool,
    QObject,
    pyqtSignal,
)

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QTextBrowser,
    QTextEdit,
    QWidget,
    QVBoxLayout,

)

class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)

class Worker(QRunnable):
    '''
    Worker thread
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.signal = WorkerSignals()

    @pyqtSlot()
    def run(self):
        sock.bind((UDP_IP, UDP_PORT_R))
        while True:
            data, addr = sock.recvfrom(1024)
            self.signal.result.emit(data.decode("utf-8"))  # Return the result of the processing

class MyQTextEdit(QTextEdit):
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return and Qt.ShiftModifier == event.modifiers():
            self.send()
        else:
            super().keyPressEvent(event)

    def send(self):
        sock.sendto(self.toPlainText().encode("utf-8"), (UDP_IP, UDP_PORT_W))
        # self.setText("")
        self.clear()
        self.cursorForPosition(QPoint(0,0))

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Chat")

        self.centralwidget = QWidget()
        self.textw = QTextBrowser(parent=self.centralwidget)
        self.texte = MyQTextEdit(parent=self.centralwidget)
        self.button = QPushButton("Send", parent=self.centralwidget)
        self.button.clicked.connect(self.texte.send)
        self.layout = QVBoxLayout()

        self.layout.addWidget(self.textw)
        self.layout.addWidget(self.texte)
        self.layout.addWidget(self.button)

        self.centralwidget.setLayout(self.layout)

        # Set the central widget of the Window.
        self.setCentralWidget(self.centralwidget)

        self.threadpool = QThreadPool()
        self.worker = Worker()
        self.worker.signal.result.connect(self.read)

        self.threadpool.start(self.worker)

    # def send(self):
    #     self.texte.send()

    def read(self, data):
        text = self.textw.toPlainText()
        self.textw.setText(text + data)

    # def closeEvent(self, event):
    #     sock.close()
    #     # self.threadpool.cancel(self.worker)
    #     event.accept()


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()