from write_in_word import *
from voice_to_word import *
import path_to_word
import json
import time

def main():
    time_from_start = time.time()
    file_path = path_to_word.path_file()
    model_path = path_to_word.model_path()  # Укажите путь к вашей модели

    recognizer = Voice_recognizer(model_path)
    doc = Write_in_word(file_path)

    try:
        recognizer.load_model()  # Загружаем модель
        recognizer.start_stream()  # Запускаем поток

        recognized_text = []  # Список для хранения распознанного текста

        try:
            pause = False
            while True:
                if int(time_from_start) % 60 == 0:
                    file = open("auto.save", 'w')
                    file.write('\n'.join(recognized_text))
                    file.close()
                data = recognizer.stream.read(4000, exception_on_overflow=False)
                if recognizer.recognizer.AcceptWaveform(data):
                    result = recognizer.recognizer.Result()
                    result_json = json.loads(result)
                    result_text = result_json.get('text', '')
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

if __name__ == "__main__":
    main()
