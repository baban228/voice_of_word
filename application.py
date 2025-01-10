import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QTextEdit, QVBoxLayout, QWidget
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
import main


class WorkerThread(QThread):
    finished = pyqtSignal()

    def __init__(self, main_function):
        super().__init__()
        self.main_function = main_function

    def run(self):
        # Здесь выполняем вашу долгую задачу, например, main.main()
        self.main_function()
        self.finished.emit()  # Сообщаем, что задача завершена

# Ваш UI-класс, как указано
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1019, 699)

        # Центральный виджет
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Устанавливаем фон бледно-голубым
        self.centralwidget.setStyleSheet("background-color: lightblue;")

        # Кнопка выбора файла
        self.choice_file = QtWidgets.QPushButton(self.centralwidget)
        self.choice_file.setGeometry(QtCore.QRect(20, 210, 171, 61))
        self.choice_file.setObjectName("choice_file")
        # Устанавливаем стиль кнопки (зеленый фон, черный жирный текст)
        self.choice_file.setStyleSheet("background-color: green; color: black; font-weight: bold;")

        # Другие кнопки
        self.list_com = QtWidgets.QPushButton(self.centralwidget)
        self.list_com.setGeometry(QtCore.QRect(20, 290, 171, 61))
        self.list_com.setObjectName("list_com")
        self.list_com.setStyleSheet("background-color: green; color: black; font-weight: bold;")

        self.exit_button = QtWidgets.QPushButton(self.centralwidget)
        self.exit_button.setGeometry(QtCore.QRect(20, 370, 171, 61))
        self.exit_button.setObjectName("exit_button")
        self.exit_button.setStyleSheet("background-color: green; color: black; font-weight: bold;")

        # Устанавливаем центральный виджет
        MainWindow.setCentralWidget(self.centralwidget)

        # Меню
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1019, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        # Строка состояния
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # Переводим текст
        self.retranslateUi(MainWindow)

        # Подключаем слоты
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "WordEditor"))
        self.choice_file.setText(_translate("MainWindow", "Выбрать файл"))
        self.list_com.setText(_translate("MainWindow", "Список COM-портов"))
        self.exit_button.setText(_translate("MainWindow", "Выход"))


# Основное окно, которое наследует от QMainWindow и использует UI
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Панель с QTextEdit и кнопкой "Назад"
        self.text_panel = QWidget(self.centralwidget)
        self.text_panel.setGeometry(QtCore.QRect(200, 150, 800, 400))
        self.text_panel.setVisible(False)  # Изначально скрыто

        self.text_edit = QTextEdit(self.text_panel)
        self.text_edit.setGeometry(50, 50, 700, 250)
        self.text_edit.setStyleSheet("background-color: white")
        self.text_edit.setPlaceholderText("Здесь будет выводиться текст...")

        self.back_button = QPushButton('Назад', self.text_panel)
        self.back_button.setGeometry(350, 320, 100, 50)
        self.back_button.setStyleSheet("background-color: green; color: black; font-weight: bold;")
        self.back_button.clicked.connect(self.show_main_buttons)


        # Привязываем обработчики к кнопкам
        self.choice_file.clicked.connect(self.open_file_dialog)
        self.exit_button.clicked.connect(self.close)

    def open_file_dialog(self):
        # Открытие диалога выбора файла
        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите файл")

        if file_name:
            print(f"Выбранный файл: {file_name}")

            # Скрыть старые кнопки
            self.choice_file.setVisible(False)
            self.list_com.setVisible(False)
            self.exit_button.setVisible(False)

            # Показать текстовое поле и кнопку "Назад"
            self.text_panel.setVisible(True)
            self.write_text("подождите идет загрузка....")
            self.worker = WorkerThread(main.main)
            self.worker.finished.connect(self.on_task_finished)
            self.worker.start()

    def on_task_finished(self):
        self.write_text("Загрузка завершена")

    def write_text(self, text):
        self.text_edit.append(text)

    def show_main_buttons(self):
        # Скрыть панель с текстом и кнопкой "Назад"
        self.text_panel.setVisible(False)

        # Показать старые кнопки
        self.choice_file.setVisible(True)
        self.list_com.setVisible(True)
        self.exit_button.setVisible(True)
