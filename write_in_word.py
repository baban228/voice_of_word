from docx import Document
from docx.shared import Pt, RGBColor
import path_to_word
class Write_in_word:
    def __init__(self, filename=""):
        self.filename = filename
        self.doc = Document(filename)

    def write_paragraph(self, string):
        self.doc.add_paragraph(string)

    def write_title(self, text, font_name='Times New Roman', font_size=24, font_color=RGBColor(0, 0, 0), heading_style='Heading 1'):
        # Создаем параграф для заголовка
        heading = self.doc.add_paragraph()

        # Добавляем текст с настройкой стилей
        run = heading.add_run(text)

        # Настройка шрифта
        run.font.name = font_name
        run.font.size = Pt(font_size)
        run.font.color.rgb = font_color

        # Устанавливаем стиль заголовка
        heading.style = heading_style

    def save(self):
        self.doc.save(path_to_word.path_file())