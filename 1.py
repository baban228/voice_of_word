from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QApplication
import time

class WorkerThread(QThread):
    finished = pyqtSignal()

    def __init__(self, main_function):
        super().__init__()
        self.main_function = main_function

    def run(self):
        # Здесь выполняем вашу долгую задачу, например, main.main()
        time.sleep(30)
        self.main_function()

        self.finished.emit()  # Сообщаем, что задача завершена

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Пример")
        self.setGeometry(100, 100, 300, 200)

        # Создаем кнопки
        self.choice_file = QPushButton("Выбрать файл", self)
        self.choice_file.clicked.connect(self.on_file_chosen)
        self.choice_file.move(50, 50)

        self.list_com = QPushButton("Список", self)
        self.list_com.move(50, 100)

        self.exit_button = QPushButton("Выход", self)
        self.exit_button.move(50, 150)

        self.text_panel = QLabel("Текст", self)
        self.text_panel.setVisible(False)  # Скрыто по умолчанию
        self.text_panel.move(50, 50)

    def write_text(self, text):
        self.text_panel.setText(text)

    def on_file_chosen(self):
        # Здесь мы выбираем файл, выводим его название
        file_name = "пример.txt"  # Например, имя файла
        print(f"Выбранный файл: {file_name}")

        # Скрываем старые кнопки
        self.choice_file.setVisible(False)
        self.list_com.setVisible(False)
        self.exit_button.setVisible(False)

        # Показываем текстовое поле и кнопку "Назад"
        self.text_panel.setVisible(True)
        self.write_text("Подождите, идет загрузка....")

        # Создаем и запускаем поток
        self.worker = WorkerThread(main.main)
        self.worker.finished.connect(self.on_task_finished)
        self.worker.start()

    def on_task_finished(self):
        self.write_text("Загрузка завершена")

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
