import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class Car(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 300, 300)
        self.setWindowTitle("Машинка")

        self.pixmap = QPixmap('car1.png')  # Начальное изображение
        self.lbl = QLabel(self)
        self.lbl.setPixmap(self.pixmap)
        self.lbl.setGeometry(0, 0, 50, 50)  # Начальные координаты и размеры машинки

        self.show()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self.change_image()

    def mouseMoveEvent(self, event):
        x = event.x()
        y = event.y()

        # Ограничение движения машинки по границам окна
        x = min(max(x, 0), 250)
        y = min(max(y, 0), 250)

        self.lbl.setGeometry(x, y, 50, 50)

    def change_image(self):
        current_image = int(self.pixmap.fileName()[-5])  # Получаем текущий номер изображения
        next_image = (current_image % 3) + 1  # Переходим к следующему изображению по кругу

        # Обновляем изображение
        self.pixmap.load(f'car{next_image}.png')
        self.lbl.setPixmap(self.pixmap)


def except_hook(cls, exception, traceback):
    # отлавливаем ошибки если они будут чтобы пользователь не видел их
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Car()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
