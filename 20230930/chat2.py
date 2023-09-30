import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QTextBrowser,
    QTextEdit,
    QWidget,
    QVBoxLayout,
)


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        self.centralwidget = QWidget()
        self.textw = QTextBrowser()
        self.texte = QTextEdit()
        self.button = QPushButton("Send")
        self.button.clicked.connect(self.send)
        self.layout = QVBoxLayout()

        self.layout.addWidget(self.textw)
        self.layout.addWidget(self.texte)
        self.layout.addWidget(self.button)

        self.centralwidget.setLayout(self.layout)

        # Set the central widget of the Window.
        self.setCentralWidget(self.centralwidget)

    def send(self):
        print("send")


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()