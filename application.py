import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import main

class WorkerThread(threading.Thread):
    def __init__(self, main_function, callback):
        super().__init__()
        self.main_function = main_function
        self.callback = callback

    def run(self):
        self.main_function()
        self.callback()

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("WordEditor")
        self.geometry("1019x699")
        self.configure(bg="lightblue")

        # Кнопка выбора файла
        self.choice_file = tk.Button(self, text="Выбрать файл", command=self.open_file_dialog, bg="green", fg="black", font=("bold"))
        self.choice_file.place(x=20, y=210, width=171, height=61)

        # Другие кнопки
        self.list_com = tk.Button(self, text="Список COM-портов", bg="green", fg="black", font=("bold"))
        self.list_com.place(x=20, y=290, width=171, height=61)

        self.exit_button = tk.Button(self, text="Выход", command=self.quit, bg="green", fg="black", font=("bold"))
        self.exit_button.place(x=20, y=370, width=171, height=61)

        # Панель с QTextEdit и кнопкой "Назад"
        self.text_panel = tk.Frame(self, bg="lightblue")
        self.text_panel.place(x=200, y=150, width=800, height=400)
        self.text_panel.place_forget()  # Изначально скрыто

        self.text_edit = tk.Text(self.text_panel, bg="white")
        self.text_edit.place(x=50, y=50, width=700, height=250)

        self.back_button = tk.Button(self.text_panel, text="Назад", command=self.show_main_buttons, bg="green", fg="black", font=("bold"))
        self.back_button.place(x=350, y=320, width=100, height=50)

    def open_file_dialog(self):
        file_name = filedialog.askopenfilename(title="Выберите файл")

        if file_name:
            print(f"Выбранный файл: {file_name}")

            # Скрыть старые кнопки
            self.choice_file.place_forget()
            self.list_com.place_forget()
            self.exit_button.place_forget()

            # Показать текстовое поле и кнопку "Назад"
            self.text_panel.place(x=200, y=150, width=800, height=400)
            self.write_text("подождите идет загрузка....")
            self.worker = WorkerThread(main.main, self.on_task_finished)
            self.worker.start()

    def on_task_finished(self):
        self.write_text("Загрузка завершена")

    def write_text(self, text):
        self.text_edit.insert(tk.END, text + "\n")

    def show_main_buttons(self):
        # Скрыть панель с текстом и кнопкой "Назад"
        self.text_panel.place_forget()

        # Показать старые кнопки
        self.choice_file.place(x=20, y=210, width=171, height=61)
        self.list_com.place(x=20, y=290, width=171, height=61)
        self.exit_button.place(x=20, y=370, width=171, height=61)

if __name__ == "__main__":
    app = Application()
    app.mainloop()
