import sys

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QTextBrowser,
    QTextEdit,
    QWidget,
    QVBoxLayout,
    QFileDialog,
    QCheckBox,
    QLabel,
    QListView,
    QHBoxLayout,
)
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor
from PyQt5.QtCore import QModelIndex, Qt

from tools import get_list_names

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Поиск дубликатов")

        self.centralwidget = QWidget()

        self.video_filter = QCheckBox("Видео (avi, mov, mkv)", checked=True)
        self.video_filter.stateChanged.connect(self.checked_video)

        self.book_filter = QCheckBox("Книги (pdf, txt, fb2, djvu)", checked=True)
        self.audio_filter = QCheckBox("Аудиофайлы (mp3)", checked=True)
        self.img_filter = QCheckBox("Изображения (jpg, png)", checked=True)

        self.open_dir = QPushButton("Open Dir")
        self.open_dir.clicked.connect(self.open_dir_dialog)

        self.label_path = QLabel("")
        self.label_index = QLabel("1/50")

        self.listView = QListView()
        self.model = QStandardItemModel()
        self.listView.setModel(self.model)
        self.listView.setObjectName("listView-1")
        self.listView.clicked[QModelIndex].connect(self.on_clicked_list_view)
        self.listView.setFocusPolicy(Qt.NoFocus)

        self.horizontal_layout = QHBoxLayout()
        self.button_next = QPushButton("Next")
        self.button_prev = QPushButton("Prev")

        self.button_apply = QPushButton("Apply")

        self.layout = QVBoxLayout()

        self.layout.addWidget(self.video_filter)
        self.layout.addWidget(self.book_filter)
        self.layout.addWidget(self.audio_filter)
        self.layout.addWidget(self.img_filter)

        self.layout.addWidget(self.open_dir)
        self.layout.addWidget(self.label_path)
        self.layout.addWidget(self.label_index)
        self.layout.addWidget(self.listView)

        self.horizontal_layout.addWidget(self.button_prev)
        self.horizontal_layout.addWidget(self.button_next)

        self.layout.addLayout(self.horizontal_layout)
        self.layout.addWidget(self.button_apply)

        self.centralwidget.setLayout(self.layout)
        self.setCentralWidget(self.centralwidget)

    def checked_video(self, checked):
        print(checked)

    def open_dir_dialog(self):
        self.base_folder = str(QFileDialog.getExistingDirectory(None, "Select Directory"))
        self.label_path.setText(self.base_folder)
        values = ['one', 'two', 'three']
        for i in values:
            self.model.appendRow(QStandardItem(i))

    def on_clicked_list_view(self, index):
        item = self.model.itemFromIndex(index)
        rgb_color = item.background().color().getRgb()
        if rgb_color == (0, 255, 255, 255):
            rgb_color = (0, 0, 0, 0)
            if "remove" in item.text():
                item.setText(" ".join(item.text().split()[:-1]) + " saved")
            else:
                item.setText(item.text() + " saved")
        else:
            rgb_color = (0, 255, 255, 255)
            if "saved" in item.text():
                item.setText(" ".join(item.text().split()[:-1]) + " remove")
            else:
                item.setText(item.text() + " remove")
        item.setBackground(QColor(*rgb_color))

        print(item.text())

    def read(self, data):
        text = self.textw.toPlainText()
        self.textw.setText(text + data)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()