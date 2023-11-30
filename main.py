from PyQt5 import uic
import sys
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QMainWindow
import sqlite3


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)

        self.search_product_list = QTableWidget(self.centralwidget)
        self.search_product_list.setObjectName(u"search_product_list")
        self.search_product_list.setGeometry(QRect(30, 40, 720, 271))

        self.connection = sqlite3.connect("coffee.db")
        self.cursor = self.connection.cursor()

        self.load_data()

    def load_data(self):
        query = f'SELECT * FROM sorts'
        self.cursor.execute(query)
        data = self.cursor.fetchall()

        num_rows = len(data)
        num_columns = len(data[0]) if num_rows > 0 else 0

        self.search_product_list.setRowCount(num_rows)
        self.search_product_list.setColumnCount(num_columns)

        for row in range(num_rows):
            for col in range(0, num_columns):
                item = QTableWidgetItem(str(data[row][col]))
                self.search_product_list.setItem(row, col, item)

        column_headers = [description[0] for description in self.cursor.description]
        self.search_product_list.setHorizontalHeaderLabels(column_headers)

    def closeEvent(self, event):
        self.connection.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
