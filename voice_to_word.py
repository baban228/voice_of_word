import os
import vosk
import pyaudio
import path_to_word

class Voice_recognizer:
    def __init__(self, model_path):
        self.model_path = model_path
        self.model = None
        self.recognizer = None
        self.p = pyaudio.PyAudio()
        self.stream = None
        self.recognized_text = []  # Список для хранения распознанного текста

    def load_model(self):
        """Загружает модель Vosk."""
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Модель не найдена по пути: {self.model_path}")

        try:
            self.model = vosk.Model(self.model_path)
            self.recognizer = vosk.KaldiRecognizer(self.model, 16000)
            print("Модель успешно загружена.")
        except Exception as e:
            raise RuntimeError(f"Ошибка при загрузке модели: {e}")

    def start_stream(self):
        """Запускает поток с микрофона для распознавания речи."""
        self.stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
        self.stream.start_stream()
        print("Скажите что-нибудь...")

    def stop_stream(self):
        """Останавливает поток и завершает работу."""
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.p.terminate()

    def get_recognized_text(self):
        """Возвращает распознанный текст как строку."""
        return ' '.join(self.recognized_text)
