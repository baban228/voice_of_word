from write_in_word import *
from voice_to_word import *
from work_with_buffer import *
from path_to_word import *
from application import *
import json
import time


def main(data_queue, on_load_callback, on_error_callback, stop_event):
    time_from_start = time.time()

    # Укажите путь к вашей модели
    path = Path()
    file_path = Path.get_path_file(path)
    model_path = Path.get_model_path(path)
    path_buffer = Path.get_path_buffer(path)

    # Проверка наличия файла
    if not file_path or not os.path.exists(file_path):
        data_queue.put("Ошибка: Файл не найден")
        stop_event.set()
        return

    # работа с док файлом
    recognizer = Voice_recognizer(model_path)
    try:
        doc = Write_in_word(file_path)
    except Exception as e:
        data_queue.put(f"Ошибка при создании документа: {str(e)}")
        stop_event.set()
        return

    # программа отладки док файла
    debug_document = Work_with_buffer(path_buffer, file_path)
    debug_document.compare_and_update()

    try:
        recognizer.load_model()  # Загружаем модель
        recognizer.start_stream()  # Запускаем поток
        on_load_callback()
        recognized_text = []
        try:
            pause = False
            while not stop_event.is_set():
                if int(time_from_start) % 60 == 0:
                    with open("auto.txt", "w", encoding="utf-8") as file:
                        file.write('\n'.join(recognized_text))

                data = recognizer.stream.read(4000, exception_on_overflow=False)
                if recognizer.recognizer.AcceptWaveform(data):
                    result = recognizer.recognizer.Result()
                    result_json = json.loads(result)
                    result_text = result_json.get('text', '')

                    data_queue.put(result_text)  # Put the result into the queue

                    print(result_text)
                    if result_text.lower().strip() == "стоп":
                        pause = True
                    if result_text.lower().strip() == "записывай":
                        pause = False
                    if result_text.lower().strip() == "выход":
                        stop_event.set()
                        break
                    if not pause:
                        recognized_text.append(result_text)  # Добавляем текст в список
        except KeyboardInterrupt:
            print("Программа остановлена пользователем.")

        print("Распознанный текст:", ' '.join(recognized_text))  # Выводим распознанный текст

        state = 0
        for frase in recognized_text:
            if frase == "заголовок":
                state = 1
                continue
            elif frase == "абзац" or frase == "конец заголовка":
                state = 0
                continue

            if state == 0:
                doc.write_paragraph(frase)
            elif state == 1:
                doc.write_title(frase)

    except Exception as e:
        print(f"Ошибка: {e}")
        data_queue.put(f"Ошибка: {str(e)}")
    finally:
        recognizer.stop_stream()  # Останавливаем поток после завершения
        while True:
            try:
                doc.save()
            except:
                on_error_callback()
            else:
                break

        # Открыть файл в режиме записи ('w'), что приведет к его очистке
        with open("auto.txt", "w", encoding="utf-8") as file:
            pass  # Ничего не пишем в файл, это очистит его