import sys
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QAction, QGroupBox, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton
from PyQt5.QtGui import QIcon


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = "EASier68k - Simulator"
        self.left = 100
        self.top = 100
        self.width = 640
        self.height = 480
        self.mainWidget = QWidget(self)
        self.mainWidget.setSize
        self.horizontalGroupBox = QGroupBox()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.statusBar().showMessage('Status: Okay')
        self.init_grid()
        self.init_menu()

        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.mainWidget.setLayout(windowLayout)


        self.show()

    def init_grid(self):
        layout = QGridLayout()
        layout.setColumnStretch(1, 4)
        layout.setColumnStretch(2, 4)

        layout.addWidget(QPushButton('2'), 0, 1)

        self.horizontalGroupBox.setLayout(layout)

    def init_menu(self):
        main_menu = self.menuBar()
        file_menu = main_menu.addMenu('File')

        exit_button = QAction(QIcon(None), 'Exit', self)
        exit_button.setShortcut('Ctrl+Q')
        exit_button.setStatusTip('Exit application')
        exit_button.triggered.connect(self.close)
        file_menu.addAction(exit_button)

        edit_menu = main_menu.addMenu('Edit')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
