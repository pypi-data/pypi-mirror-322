import sys
import math
from PyQt6.QtCore import Qt, QPropertyAnimation, QPoint, pyqtProperty, QSize
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QGraphicsDropShadowEffect, QFrame, \
    QGraphicsOpacityEffect, QMainWindow, QSizePolicy


class FloatingMenu(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(50, 50)

class MainMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Main Menu")
        self.setStyleSheet("background-color: blue;")
        self.floating_menu = FloatingMenu(self)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        main_menu = MainMenu()
        layout.addWidget(main_menu)
        widget.setLayout(layout)

        self.setCentralWidget(widget)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
