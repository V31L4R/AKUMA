from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from pathlib import Path

class AdvancedPage(QWidget):
    def __init__(self):
        super().__init__()
        # Назначаем имя страницы для обращения из QSS.
        self.setObjectName("advanced")
        # Формируем путь к файлу стилей страницы.
        stylesheet_path = (
            Path(__file__).parent
            / ".."
            / "styles"
            / "pages"
            / "advanced.qss"
        ).resolve()

        # Открываем файл стилей страницы.
        with open(stylesheet_path, "r", encoding="utf-8") as stylesheet_file:

            # Считываем содержимое файла.
            stylesheet = stylesheet_file.read()

        # Применяем стили страницы Advanced.
        self.setStyleSheet(stylesheet)
        
        page_layout = QVBoxLayout()
        self.setLayout(page_layout)
        # Создаём заголовок страницы.
        page_title = QLabel("Advanced")

        # Добавляем заголовок первым элементом страницы.
        page_layout.addWidget(page_title)

        # Создаём плашку-заглушку для будущего функционала.
        coming_soon_label = QLabel("Coming Soon")

        # Назначаем имя для стилизации через QSS.
        coming_soon_label.setObjectName("coming_soon_label")

        # Центрируем текст внутри плашки.
        coming_soon_label.setAlignment(Qt.AlignCenter)

        # Ограничиваем плашку по высоте.
        coming_soon_label.setFixedHeight(30)
        # Растягиваем плашку по доступной ширине страницы.
        coming_soon_label.setMinimumWidth(400)

        # Добавляем плашку под заголовком.
        page_layout.addWidget(coming_soon_label)

        # Всё оставшееся место оставляем пустым.
        page_layout.addStretch()