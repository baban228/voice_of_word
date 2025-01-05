from write_in_word import Write_in_word
from voice_to_word import Voice_recognizer
from docx import Document
import path_to_word
import json
def main():
    file_path = path_to_word.path_file()
    model_path = path_to_word.model_path()  # Укажите путь к вашей модели

    recognizer = Voice_recognizer(model_path)
    doc = Write_in_word(file_path)

    try:
        recognizer.load_model()  # Загружаем модель
        recognizer.start_stream()  # Запускаем поток

        recognized_text = []  # Список для хранения распознанного текста

        try:
            while True:
                data = recognizer.stream.read(4000)
                if recognizer.recognizer.AcceptWaveform(data):
                    result = recognizer.recognizer.Result()
                    result_json = json.loads(result)
                    result_text = result_json.get('text', '')
                    print(result_text)
                    recognized_text.append(result_text)# Добавляем текст в список
                    if result_text == "стоп":
                        return
                    elif result_text == "заголовок":
                        doc.write_paragraph(recognizer.get_recognized_text())
                    elif result_text == "абзац":
                        doc.write_title(recognizer.get_recognized_text())

        except KeyboardInterrupt:
            print("Программа остановлена пользователем.")

        print("Распознанный текст:", ' '.join(recognized_text))  # Выводим распознанный текст
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        recognizer.stop_stream()  # Останавливаем поток после завершения
        doc.save()
if __name__ == "__main__":
    main()