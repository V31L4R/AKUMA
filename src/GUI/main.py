from pprint import pprint
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

        # Временно собирает и выводит актуальные значения формы
        # в момент нажатия кнопки Generate.
        def print_form_values():

            # Получаем текст Number of Records без преобразования,
            # чтобы увидеть даже значение, которое валидатор не принимает.
            records_text = (
                main_settings_page
                .records_input
                .text()
                .strip()
            )

            # Получаем текст Amount of Corrupt Data без преобразования.
            amount_text = (
                corruption_page
                .corruption_amount_input
                .text()
                .strip()
            )

            # Собираем диагностический снимок текущей формы.
            form_values = {
                "main_settings": {
                    "number_of_records_raw": records_text,
                    "number_of_records_acceptable": (
                        main_settings_page
                        .records_input
                        .hasAcceptableInput()
                    ),
                    "file_format": (
                        main_settings_page
                        .format_input
                        .currentText()
                    ),
                    "included_fields": (
                        main_settings_page
                        .field_selector
                        .get_selected_fields()
                    ),
                },

                "corruption": {
                    "enabled": (
                        corruption_page
                        .corruption_switch
                        .isChecked()
                    ),
                    "mode": (
                        corruption_page
                        .corruption_mode
                        .currentText()
                    ),
                    "amount_raw": amount_text,
                    "amount_acceptable": (
                        corruption_page
                        .corruption_amount_input
                        .hasAcceptableInput()
                    ),
                    "amount_type": (
                        corruption_page
                        .corruption_amount_type
                        .currentText()
                    ),
                    "exclusive": (
                        corruption_page
                        .exclusive_switch
                        .isChecked()
                    ),
                    "corrupted_columns": (
                        corruption_page
                        .corrupted_columns_selector
                        .get_selected_fields()
                    ),
                    "corruption_types": (
                        corruption_page
                        .corruption_type_selector
                        .get_selected_fields()
                    ),
                },
            }

            # Отделяем каждый новый запуск теста.
            print("\n" + "=" * 60)
            print("AKUMA FORM VALUES")
            print("=" * 60)

            # Красиво выводим вложенный словарь.
            pprint(
                form_values,
                sort_dicts=False,
            )

            print("=" * 60)

            # По нажатию Generate на Main Settings
        # выводим актуальные значения всей формы.
        main_settings_page.generate_button.clicked.connect(
            print_form_values
        )

        # По нажатию Generate на Corruption
        # выводим тот же самый снимок формы.
        corruption_page.generate_button.clicked.connect(
            print_form_values
        )

        # Передаёт актуальные параметры Main Settings
        # на страницу Corruption для расчёта доступного количества данных.
        def sync_corruption_limits():

            # Получаем текущее значение количества записей.
            records_text = main_settings_page.records_input.text()

            # Преобразуем заполненное поле в число.
            # Если поле пустое — передаём 0.
            records_count = int(records_text) if records_text else 0

            # Получаем список выбранных полей.
            selected_fields = (
                main_settings_page
                .field_selector
                .get_selected_fields()
            )

            # Передаём количество записей и сами выбранные поля
            # на страницу Corruption.
            corruption_page.update_available_data(
                records_count,
                selected_fields
            )


        # Пересчитываем лимиты при изменении количества записей.
        main_settings_page.records_input.textChanged.connect(
            sync_corruption_limits
        )

        # Пересчитываем лимиты при изменении выбранных полей.
        main_settings_page.field_selector.selection_changed.connect(
            sync_corruption_limits
        )

        # Выполняем первоначальную синхронизацию
        # сразу после создания обеих страниц.
        sync_corruption_limits()

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
