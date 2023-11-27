# импорт жизненно необходимых приложений
from PyQt5 import QtWidgets
import sys

# Данные коментарии спонсированы никем, здесь могла бы быть ваша реклама
# А сейчас спасибо нашим спонсорам
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QFileDialog, QMessageBox

import untitled

import sqlite3


# здесь мы определяем класс главного окна
class MainWindow(QtWidgets.QMainWindow, untitled.Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        # создадаём переменные которые будут нам нужны дальше
        # в этой я буду хранить текущий магазин
        self.shop = ""
        # в этой я буду хранить текущий товар
        self.product = ""
        # в этой я буду хранить ай ди выбранного в поиске товара
        self.buffer = ""
        # в этой я буду хранить ай ди выбранного в карзине товара
        self.cart_buffer = ""
        # подсоединяем все кнопки к своим функциям
        self.add_1.clicked.connect(self.add_1_func)
        self.lenta.clicked.connect(self.lenta_func)
        self.browser.clicked.connect(self.browser_func)
        self.add_to_list.clicked.connect(self.add_to_list_func)
        self.load_bd.clicked.connect(self.load_bd_func)
        self.magnit.clicked.connect(self.magnit_func)
        self.perekrestok.clicked.connect(self.perekrestok_func)
        self.remove_all.clicked.connect(self.remove_all_func)
        self.remove_one.clicked.connect(self.remove_one_func)
        self.save_as_bd.clicked.connect(self.save_as_bd_func)
        self.save_as_txt.clicked.connect(self.save_as_txt_func)
        self.search.clicked.connect(self.search_func)

        # Делаем статусбар пустым
        self.status_bar.setText("")

        # Создаем виджет для отображения таблицы поиска
        self.search_product_list = QTableWidget(self.centralwidget)
        # задаём имя виджету(не обяательно)
        self.search_product_list.setObjectName(u"search_product_list")
        # задаём размеры виджета
        self.search_product_list.setGeometry(QRect(410, 40, 361, 271))
        # присоединение к виджету вспомогательной функции
        self.search_product_list.cellClicked.connect(self.set_bufer)

        # Создаем виджет для отображения таблицы корзины
        self.list_to_buy = QTableWidget(self.centralwidget)
        # задаём имя виджету(не обяательно)
        self.list_to_buy.setObjectName(u"list_to_buy")
        # задаём размеры виджета
        self.list_to_buy.setGeometry(QRect(15, 40, 376, 271))
        # присоединение к виджету вспомогательной функции
        self.list_to_buy.cellClicked.connect(self.set_cart_buffer)

        # Подключаемся к базе данных SQLite
        self.connection = sqlite3.connect("shop.db")
        self.cursor = self.connection.cursor()

        # Загружаем данные из базы данных и отображаем их в таблицах
        self.load_data()

        # подключаем к виджету-дисплею функцию с вычислением итоговой стоимости
        self.summ_cost.display(self.final_cost_func())

    def add_1_func(self):
        # данная функция по нажатию кнопки увеличивает количество товара в корзине на 1
        if self.cart_buffer == '':
            # проверка выбран ли продукт для операции, если мы попали сюда, то это
            # ошибка пользователя из которой мы красиво выходим и предупреждаем пользователя
            self.status_bar.setText("")
            # делаем соответствующий вывод в статусбар
            self.status_bar.setText("Product hasn't chosen")
        else:
            # если же пользователь молодец, то добавляем продукт ему в корзину
            # делаем запрос товара по ай ди из таблицы поиска чтобы вытащить все данные о нём
            prod_dat = f"SELECT * FROM products WHERE id={self.cart_buffer}"
            self.cursor.execute(prod_dat)
            data = self.cursor.fetchall()
            # узнаём сколько товара было до выполнения функции
            pcs_before = self.cursor.execute(f"SELECT pcs FROM cart WHERE id={self.cart_buffer}").fetchall()
            if pcs_before:
                # очередная защита от дурака, как мне кажется такого не бывает много, а вот дураков бывает
                # создём запрос на обновление данных в таблице
                query = f''' UPDATE cart SET
                name='{data[0][1]}',
                cost={data[0][2]},
                pcs={int(pcs_before[0][0]) + 1}
                WHERE id={data[0][0]}
                '''
                # исполняем его
                self.cursor.execute(query)
                self.status_bar.setText("")
                # отчитываемся пользователю об операции
                self.status_bar.setText("Product added to cart")
                self.load_data()
                self.connection.commit()

    def set_bufer(self):
        a = self.search_product_list.currentRow()
        # задаём переменной значение равное фй ди нужного продукта
        self.buffer = self.search_product_list.item(a, 0).text()

    def set_cart_buffer(self):
        a = self.list_to_buy.currentRow()
        # задаём переменной значение равное ай ди нужного продукта
        self.cart_buffer = self.list_to_buy.item(a, 0).text()

    def lenta_func(self):
        # задаём магазин в соответствующую переменную
        self.shop = "лента"
        # обновляем поисковую таблицу
        self.load_data()
        self.status_bar.setText("")
        # отчитываемся пользователю об операции
        self.status_bar.setText("Now you are searching in shop named Lenta")

    def browser_func(self):
        # создаём всплывающее окно с краткой информацией о продукте
        # В ДАЛЬНЕЙШЕМ ДОРАБОТАТЬ
        msg = QMessageBox()
        # задаём имя таблицы
        msg.setWindowTitle("Описание товара")
        # вставляем картинку товара
        pixmap = QPixmap(QImage("Без названия.png"))
        msg.setIconPixmap(pixmap)
        # задаём текст-описание товара
        msg.setText("Здесь должно быть описание товара с картиночкой, оставленное \n"
                    "производителем/магазином по ссылочке, которую укажет в базе \n"
                    "данных, но нам не рассказали, как такое осуществить, поэтому\n"
                    "здесь находится это сообщение(ходят слухи, что где то здесь \n"
                    "всё равно запрятона картинка),\n"
                    "А ТАК ЖЕ ЗДЕСЬ МОГЛА БЫТЬ ВАША РЕКЛАМА!")
        msg.exec_()

    def add_to_list_func(self):
        # функция добавления нового товара в таблицу
        if self.buffer == '':
            # проверка выбран ли продукт для операции, если мы попали сюда, то это
            # ошибка пользователя из которой мы красиво выходим и предупреждаем пользователя
            self.status_bar.setText("")
            # делаем соответствующий вывод в статусбар
            self.status_bar.setText("Product hasn't chosen")
        else:
            prod_dat = f"SELECT * FROM products WHERE id={self.buffer}"
            self.cursor.execute(prod_dat)
            data = self.cursor.fetchall()
            pcs_before = self.cursor.execute(f"SELECT pcs FROM cart WHERE id={self.buffer}").fetchall()
            if pcs_before:
                # если товар уже есть в карзине, то его количество просто надо увеличить на 1
                # создём запрос на обновление данных в таблице
                query = f''' UPDATE cart SET
                name='{data[0][1]}',
                cost={data[0][2]},
                pcs={int(pcs_before[0][0]) + 1}
                WHERE id={data[0][0]}
                '''
                # исполняем запрос
                self.cursor.execute(query)
                self.status_bar.setText("")
                # отчитываемся пользователю об операции
                self.status_bar.setText("Product added to cart")
                # сохраняем изменения
                self.connection.commit()
            else:
                # если товара ещё нет в карзине, то его надо добавить с нуля
                query = f''' INSERT INTO cart(id,name,cost,pcs) 
                VALUES({data[0][0]},'{data[0][1]}',{data[0][2]},1) '''
                # исполняем запрос
                self.cursor.execute(query)
                self.status_bar.setText("")
                # отчитываемся пользователю об операции
                self.status_bar.setText("Product added to cart")
                # сохраняем изменения
                self.connection.commit()
        # обновляем таблицы
        self.load_data()

    def remove_all_func(self):
        # функция удаляющая все экземпляры товара
        if self.cart_buffer == '':
            # проверка выбран ли продукт для операции, если мы попали сюда, то это
            # ошибка пользователя из которой мы красиво выходим и предупреждаем пользователя
            self.status_bar.setText("")
            # делаем соответствующий вывод в статусбар
            self.status_bar.setText("Product hasn't chosen")
        else:
            prod_dat = f"SELECT * FROM cart WHERE id={self.cart_buffer}"
            self.cursor.execute(prod_dat)
            data = self.cursor.fetchall()
            # пользователь может попытаться удалить товар, которого и так уже нет
            if not data:
                # очередная защита от дурака, как мне кажется такого не бывает много, а вот дураков бывает
                # создём запрос на обновление данных в таблице
                self.status_bar.setText("")
                # делаем соответствующий вывод в статусбар
                self.status_bar.setText("This product isn't in a cart now")
            else:
                # если же товар всё ещё остался в карзине, то его надо удалить
                # создаём запрос для удаления товара
                query = f"DELETE FROM cart WHERE id={self.cart_buffer}"
                # исполняем запрос
                self.cursor.execute(query)
                self.status_bar.setText("")
                # отчитываемся пользователю об операции
                self.status_bar.setText("Product deleted from cart")
                # обновляем таблицы
                self.load_data()
        # сохраняем изменения
        self.connection.commit()

    def remove_one_func(self):
        # функция удаляющая один экземпляр товара
        if self.cart_buffer == '':
            # проверка выбран ли продукт для операции, если мы попали сюда, то это
            # ошибка пользователя из которой мы красиво выходим и предупреждаем пользователя
            self.status_bar.setText("")
            # делаем соответствующий вывод в статусбар
            self.status_bar.setText("Product hasn't chosen")
        else:
            prod_dat = f"SELECT * FROM cart WHERE id={self.cart_buffer}"
            self.cursor.execute(prod_dat)
            data = self.cursor.fetchall()
            if not data:
                # очередная защита от дурака, как мне кажется такого не бывает много, а вот дураков бывает
                # создём запрос на обновление данных в таблице
                self.status_bar.setText("")
                # делаем соответствующий вывод в статусбар
                self.status_bar.setText("This product isn't in a cart now")
            elif data[0][3] == 1:
                # если товар остался в карзине только в единичном экземпляре, то его надо полностью вычеркнуть
                # делаем запрос на удаление
                query = f"DELETE FROM cart WHERE id={self.cart_buffer}"
                # исполняем его
                self.cursor.execute(query)
                self.status_bar.setText("")
                # отчитываемся пользователю об операции
                self.status_bar.setText("Product deleted from cart")
            else:
                # если же товар остался в карзине в множественном экземпляре, то его надо просто изменить
                # делаем запрос на изменение
                pcs_before = self.cursor.execute(f"SELECT pcs FROM cart WHERE id={self.cart_buffer}").fetchall()
                query = f''' UPDATE cart SET
                                name='{data[0][1]}',
                                cost={data[0][2]},
                                pcs={int(pcs_before[0][0]) - 1}
                                WHERE id={data[0][0]}
                                '''
                # исполняем его
                self.cursor.execute(query)
                self.status_bar.setText("")
                # отчитываемся пользователю об операции
                self.status_bar.setText("One product deleted from cart")
        # сохраняем изменения
        self.connection.commit()
        # обновляем таблицы
        self.load_data()

    def load_bd_func(self):
        # в разработке
        pass

    def magnit_func(self):
        # задаём магазин в соответствующую переменную
        self.shop = "магнит"
        # обновляем поисковую таблицу
        self.load_data()
        self.status_bar.setText("")
        # отчитываемся пользователю об операции
        self.status_bar.setText("Now you are searching in shop named Magnit")

    def perekrestok_func(self):
        # задаём магазин в соответствующую переменную
        self.shop = "перекрёсток"
        # обновляем поисковую таблицу
        self.load_data()
        self.status_bar.setText("")
        # отчитываемся пользователю об операции
        self.status_bar.setText("Now you are searching in shop named Perekrestok")

    def save_as_bd_func(self):
        # в разработке
        pass

    def save_as_txt_func(self):
        # это функция делающая текстовый файл со списком продуктов для мужиков
        # делаем запрос
        prod_dat = f"SELECT * FROM cart"
        # исполняем его
        self.cursor.execute(prod_dat)
        # записываем в переменную полученные данные
        data = self.cursor.fetchall()
        # спрашиваем у пользователя, куда сохранить файл
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "Save as", "",
                                                  "All Files (*);;Text Files (*.txt)", options=options)
        self.status_bar.setText("")
        # уведомляем пользователя об операции
        self.status_bar.setText(f"Fale saved")
        # записываем информацию в файл
        with open(fileName, mode="w") as file:
            # делаем удобный заголовок
            file.write("название                    цена    количество\n")
            # делаем переменную в которую запишем итоговую стоимость
            summ = 0
            for i in range(len(data)):
                # добавляем строку с одним товаром
                file.write(str(data[i][1]) +
                           " " * (28 - len(str(data[i][1]))) +
                           str(data[i][2]) + " " * (8 - len(str(data[i][2]))) +
                           str(data[i][3]) + "\n")
                # обновляем итоговую стоимость
                summ += data[i][2] * data[i][3]

            # делаем удобный итог
            file.write(f"итог:                       {summ}")

    def final_cost_func(self):
        # эта функция считает итоговую стоимость
        # делаем запрос
        prod_dat = f"SELECT * FROM cart"
        # исполняем его
        self.cursor.execute(prod_dat)
        # записываем в переменную полученные данные
        data = self.cursor.fetchall()
        # делаем переменную в которую запишем итоговую стоимость
        summ = 0
        for i in range(len(data)):
            # обновляем итоговую стоимость
            summ += data[i][2] * data[i][3]
        # возвращаем итоговую стоимость
        return summ

    def search_func(self):
        # устанавливаем имя искомого продукта
        # записываем его в переменную
        self.product = self.search_enter.toPlainText()
        # обновляем таблицы
        self.load_data()
        self.status_bar.setText("")
        # сообщаем пользователю об операции
        self.status_bar.setText(f"Now you are searching product named {self.product}")

    def load_data(self):
        # в этой функции я обновляю таблицы
        # Делаем запрос для выборки данных
        query = f'SELECT * FROM products WHERE name_of_shop like "%{self.shop}%" AND ' \
                f'name_of_product like "%{self.product}%"'
        # выполняем запрос
        self.cursor.execute(query)
        # записываем его результат в переменную
        data = self.cursor.fetchall()

        # Получаем количество строк и столбцов
        num_rows = len(data)
        num_columns = len(data[0]) if num_rows > 0 else 0

        # Устанавливаем количество строк и столбцов в таблице
        self.search_product_list.setRowCount(num_rows)
        self.search_product_list.setColumnCount(num_columns)

        # Заполняем таблицу данными
        for row in range(num_rows):
            for col in range(0, num_columns):
                item = QTableWidgetItem(str(data[row][col]))
                self.search_product_list.setItem(row, col, item)

        # Опционально: устанавливаем заголовки столбцов
        column_headers = [description[0] for description in self.cursor.description]
        self.search_product_list.setHorizontalHeaderLabels(column_headers)

        # Делаем запрос для выборки данных
        query = f'SELECT * FROM cart'
        # Исполняем его
        self.cursor.execute(query)
        # записываем его результат в переменную
        data = self.cursor.fetchall()

        # Получаем количество строк и столбцов
        num_rows = len(data)
        num_columns = len(data[0]) if num_rows > 0 else 0

        # Устанавливаем количество строк и столбцов в таблице
        self.list_to_buy.setRowCount(num_rows)
        self.list_to_buy.setColumnCount(num_columns)
        # Заполняем таблицу данными
        for row in range(num_rows):
            for col in range(0, num_columns):
                item = QTableWidgetItem(str(data[row][col]))
                self.list_to_buy.setItem(row, col, item)

        # Опционально: устанавливаем заголовки столбцов
        column_headers = [description[0] for description in self.cursor.description]
        self.list_to_buy.setHorizontalHeaderLabels(column_headers)

        # отображение цены
        self.summ_cost.display(self.final_cost_func())

    def closeEvent(self, event):
        # Закрываем соединение с базой данных при закрытии приложения
        self.connection.close()


def except_hook(cls, exception, traceback):
    # отлавливаем ошибки если они будут чтобы пользователь не видел их
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    # запускаем программу
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
