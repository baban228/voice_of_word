import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import queue
import main  # Import the main script containing the main() function
from path_to_word import Path
from PIL import Image, ImageTk

class WorkerThread(threading.Thread):
    def __init__(self, main_function, callback_start, on_error_callback, callback_finish, data_queue, stop_event):
        super().__init__()
        self.main_function = main_function
        self.callback = callback_finish
        self.data_queue = data_queue
        self.stop_event = stop_event
        self.callback_start = callback_start
        self.on_error_callback = on_error_callback

    def run(self):
        self.main_function(self.data_queue, self.callback_start, self.on_error_callback, self.stop_event)
        if not self.stop_event.is_set():
            self.callback()

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("WordEditor")
        self.geometry("1019x699")

        # Загрузка фонового изображения
        self.background_image = Image.open("image.jpg")  # Укажите путь к вашему изображению
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.background_label = tk.Label(self, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Кнопка выбора файла
        self.choice_file = tk.Button(self, text="Выбрать файл", command=self.open_file_dialog, bg="green", fg="black",
                                     font=("bold"))
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
        self.back_button = tk.Button(self.text_panel, text="Назад", command=self.show_main_buttons, bg="green",
                                     fg="black", font=("bold"))
        self.back_button.place(x=350, y=320, width=100, height=50)
        self.stop_button = tk.Button(self.text_panel, text="Завершить", command=self.stop_and_quit, bg="red", fg="black",
                                     font=("bold"))
        self.stop_button.place(x=600, y=320, width=100, height=50)
        self.data_queue = queue.Queue()
        self.stop_event = threading.Event()
        self.worker = None
        self.after(100, self.process_queue)  # Start processing the queue every 100ms

    def open_file_dialog(self):
        file_name = filedialog.askopenfilename(title="Выберите файл")
        if file_name:
            print(f"Выбранный файл: {file_name}")
            Path.set_path_file(Path, file_name)  # Set the file path in the Path class
            # Скрыть старые кнопки
            self.choice_file.place_forget()
            self.list_com.place_forget()
            self.exit_button.place_forget()
            # Показать текстовое поле и кнопку "Назад"
            self.text_panel.place(x=200, y=150, width=800, height=400)
            self.write_text("подождите идет загрузка....")
            self.worker = WorkerThread(main.main, self.on_load_finished, self.on_error_callback, self.on_task_finished, self.data_queue, self.stop_event)
            self.worker.start()

    def on_task_finished(self):
        self.write_text("Загрузка завершена")

    def on_load_finished(self):
        self.write_text("Загрузка завершена")

    def on_error_callback(self):
        self.write_text("Нет доступа к файлу; закройте или создайте его", tag="red_bold")
    def write_text(self, text):
        self.text_edit.insert(tk.END, text + "\n")

    def show_main_buttons(self):
        # Скрыть панель с текстом и кнопкой "Назад"
        self.text_panel.place_forget()
        # Показать старые кнопки
        self.choice_file.place(x=20, y=210, width=171, height=61)
        self.list_com.place(x=20, y=290, width=171, height=61)
        self.exit_button.place(x=20, y=370, width=171, height=61)

    def process_queue(self):
        try:
            while True:
                text = self.data_queue.get_nowait()
                self.write_text(text)
                if text.strip().lower() == "выход":
                    self.stop_and_quit()
        except queue.Empty:
            pass
        finally:
            self.after(100, self.process_queue)

    def stop_and_quit(self):
        if self.worker is not None and self.worker.is_alive():
            self.stop_event.set()
            self.worker.join(timeout=5)  # Wait for the thread to finish with a timeout
            self.write_text("Работа завершена.")
        self.quit()  # Exit the application

if __name__ == "__main__":
    app = Application()
    app.mainloop()