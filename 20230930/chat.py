# pip install pyqt5
# pip install pyqt5-tools
# pyuic5 mainwindow.ui -o MainWindow.py

from PyQt5 import QtWidgets, uic

app = QtWidgets.QApplication([])
ui = uic.loadUi("design.ui")
ui.setWindowTitle("Chat")

ui.show()
app.exec()