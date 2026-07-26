import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QPushButton, QVBoxLayout
from PySide6.QtWidgets import QStackedWidget
from pages.main_settings import MainSettingsPage
from pages.corruption import CorruptionPage
from pages.advanced import AdvancedPage
from pages.options import OptionsPage
from pages.help import HelpPage

# Загружает общие стили приложения.
def load_global_stylesheet():

    # Определяет путь к директории со стилями.
    styles_directory = Path(__file__).parent / "styles"

    # Хранит пути только к глобальным QSS-файлам.
    stylesheet_paths = [

        # Подключает общие стили приложения.
        styles_directory / "general.qss",

        # Подключает стили переиспользуемых элементов управления.
        styles_directory / "controls.qss",
    ]

    # Хранит содержимое прочитанных QSS-файлов.
    stylesheet_parts = []

    # Последовательно перебирает глобальные файлы стилей.
    for stylesheet_path in stylesheet_paths:

        # Открывает текущий QSS-файл в режиме чтения.
        with open(stylesheet_path, "r", encoding="utf-8") as stylesheet_file:

            # Добавляет содержимое файла в общий список.
            stylesheet_parts.append(stylesheet_file.read())

    # Объединяет глобальные стили в одну строку.
    return "\n".join(stylesheet_parts)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AKUMA")
        self.resize(1000, 700)
        central_widget = QWidget()
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        stylesheet_path = (
            Path(__file__).parent
            / "styles"
            / "sidebar.qss"
        )

        with open(stylesheet_path, "r") as stylesheet_file:

            stylesheet = stylesheet_file.read()

        sidebar.setStyleSheet(stylesheet)


        sidebar_layout = QVBoxLayout()
        sidebar.setLayout(sidebar_layout)
        content_area = QStackedWidget()
        main_settings_page = MainSettingsPage()
        corruption_page = CorruptionPage()
        advanced_page = AdvancedPage()
        options_page = OptionsPage()
        help_page = HelpPage()
        content_area.addWidget(main_settings_page)
        content_area.addWidget(corruption_page)
        content_area.addWidget(advanced_page)
        content_area.addWidget(options_page)
        content_area.addWidget(help_page)

        main_layout.addWidget(sidebar,1)
        main_layout.addWidget(content_area,4)
        
       # Задаём имя области контента для точечного обращения из QSS.
        content_area.setObjectName("content_area")

        # Красим только сам QStackedWidget, не затрагивая дочерние элементы.
        content_area.setStyleSheet("""
            QStackedWidget#content_area {
                background-color: #303030;
            }
        """)
        
        self.setCentralWidget(central_widget)

        main_settings_button = QPushButton("Main Settings")
        corruption_button = QPushButton("Corruption")
        advanced_button = QPushButton("Advanced")
        options_button = QPushButton("Options")
        help_button = QPushButton("Help")

        navigation_buttons = [
            main_settings_button,
         corruption_button,
            advanced_button,
            options_button,
            help_button,
        ]

        def set_active_button(selected_button):
            for button in navigation_buttons:
                button.setProperty("active", button is selected_button)
                button.style().unpolish(button)
                button.style().polish(button)
                button.update()
        for button in navigation_buttons:
            button.clicked.connect(
                lambda checked=False, button=button: set_active_button(button)
            )

        set_active_button(main_settings_button)
        sidebar_layout.addWidget(main_settings_button)
        sidebar_layout.addWidget(corruption_button)
        sidebar_layout.addWidget(advanced_button)
        sidebar_layout.addWidget(options_button)
        sidebar_layout.addWidget(help_button)

        main_settings_button.clicked.connect(
            lambda: content_area.setCurrentWidget(main_settings_page)
        )
        corruption_button.clicked.connect(
            lambda: content_area.setCurrentWidget(corruption_page)
        )
        advanced_button.clicked.connect(
            lambda: content_area.setCurrentWidget(advanced_page)
        )
        options_button.clicked.connect(
            lambda: content_area.setCurrentWidget(options_page)
        )
        help_button.clicked.connect(
            lambda: content_area.setCurrentWidget(help_page)
        )
        sidebar_layout.addStretch()



def main():

    app = QApplication(sys.argv)
     # Применяет общие стили ко всему приложению.
    app.setStyleSheet(load_global_stylesheet())
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
