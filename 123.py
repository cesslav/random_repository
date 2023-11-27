from random import randint

import sys
from PyQt5.QtGui import QPixmap, QPainter, QColor, QPen
from PyQt5 import uic

from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QFileDialog


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI.ui', self)  # Загружаем дизайн
        canvas = QPixmap(600, 300)
        # painter = QPainter(self.label.pixmap())
        # painter.setBrush(QColor(255, 255, 255))
        # painter.drawRect(-1, -1, 601, 601)
        # painter.end()
        # self.update()

        self.label.setPixmap(canvas)
        self.pushButton.clicked.connect(self.run)

    def run(self):
        def draw():
            x = randint(50, 550)
            y = randint(50, 250)
            w = randint(10, 100)
            painter.setBrush(QColor(randint(0, 255), 255, 0))
            painter.drawEllipse(x, y, w, w)
        # создаем экземпляр QPainter, передавая холст (self.label.pixmap())
        painter = QPainter(self.label.pixmap())
        # pen = QPen()
        # pen.setWidth(3)
        painter.setBrush(QColor(255, 255, 255))
        painter.drawRect(-1, -1, 601, 601)

        # pen.setColor(QColor(*[randint(0, 255) for i in range(3)]))
        # painter.setPen(pen)
        for i in range(randint(3, 5000)):
            draw()
        painter.end()
        self.update()


def except_hook(cls, exception, traceback):
    # отлавливаем ошибки если они будут чтобы пользователь не видел их
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())