from write_in_word import *
from voice_to_word import *
from work_with_buffer import *
from path_to_word import *
from application import *
import json
import time

def main():
    time_from_start = time.time()

    # Укажите путь к вашей модели
    path = Path()
    file_path = Path.get_path_file(path)
    model_path = Path.get_model_path(path)
    path_buffer = Path.get_path_buffer(path)

    #работа с док файлом
    recognizer = Voice_recognizer(model_path)
    doc = Write_in_word(file_path)

    #программа отладки док файла
    debug_document = Work_with_buffer(path_buffer, file_path)
    debug_document.compare_and_update()


    application_obj = Application()

    try:
        recognizer.load_model()  # Загружаем модель
        recognizer.start_stream()  # Запускаем поток
        with open("auto.txt", "r", encoding="utf-8") as buf_file:
            recognized_text = buf_file.readlines()  # Список для хранения распознанного текста

        try:
            pause = False
            while True:
                if int(time_from_start) % 60 == 0:
                    with open("auto.txt", "r", encoding="utf-8") as file:
                        file.write('\n'.join(recognized_text))
                        file.close()
                data = recognizer.stream.read(4000, exception_on_overflow=False)
                if recognizer.recognizer.AcceptWaveform(data):
                    result = recognizer.recognizer.Result()
                    result_json = json.loads(result)
                    result_text = result_json.get('text', '')
                    application_obj.write_text(result_text)
                    print(result_text)
                    if result_text == "стоп":
                        pause = True
                    if result_text == "записывай":
                        pause = False
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
    finally:
        recognizer.stop_stream()  # Останавливаем поток после завершения
        doc.save()
        # Открыть файл в режиме записи ('w'), что приведет к его очистке
        with open("auto.txt", "w", encoding="utf-8") as file:
            pass  # Ничего не пишем в файл, это очистит его