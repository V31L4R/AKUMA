from pprint import pprint
import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QPushButton, QVBoxLayout
from PySide6.QtWidgets import QStackedWidget
from PySide6.QtCore import QSettings
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
        # Создаём постоянное хранилище настроек AKUMA.
        self.settings = QSettings(
            "AKUMA",
            "AKUMA"
        )

        # Получаем сохранённое состояние функции Remember Settings.
        # Если приложение запускается впервые — используем OFF.
        self.remember_settings_enabled = self.settings.value(
            "remember_settings",
            False,
            type=bool
        )

        saved_form = self.settings.value("saved_form")

        #Тест записи сохранения состояния
        print()
        print("RESTORED FROM SETTINGS")
        pprint(saved_form)
        print()

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
        self.main_settings_page = MainSettingsPage()
        self.corruption_page = CorruptionPage()
        self.advanced_page = AdvancedPage()
        self.options_page = OptionsPage()
        self.help_page = HelpPage()

        # Временно сохраняем старые локальные имена страниц,
        # чтобы существующий код __init__ продолжил работать без изменений.
        main_settings_page = self.main_settings_page
        corruption_page = self.corruption_page
        advanced_page = self.advanced_page
        options_page = self.options_page
        help_page = self.help_page

        # Подключаем изменение режима отображения окна.
        options_page.screen_layout_changed.connect(
            self.update_screen_layout
        )

        # Подключаем изменение Remember Settings
        # к MainWindow.
        self.options_page.remember_settings_changed.connect(
            self.update_remember_settings
        )

        # Восстанавливаем сохранённое состояние переключателя.
        self.options_page.remember_settings_switch.blockSignals(True)

        self.options_page.remember_settings_switch.setChecked(
            self.remember_settings_enabled
        )

        self.options_page.remember_settings_switch.setText(
            "ON"
            if self.remember_settings_enabled
            else "OFF"
        )

        self.options_page.remember_settings_switch.blockSignals(False)

        # Временно собирает и выводит актуальные значения формы
        # в момент нажатия кнопки Generate.
        def print_form_values():

            # Получаем единый снимок текущего состояния формы.
            form_values = self.build_form_state()


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

        # Если Remember Settings включён —
        # восстанавливаем сохранённое состояние всей формы.
        if self.remember_settings_enabled:

            self.restore_form_state()

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

    def build_form_state(self):

        # Получаем Number of Records как исходный текст.
        records_text = (
            self.main_settings_page
            .records_input
            .text()
            .strip()
        )

        # Получаем Amount of Corrupt Data как исходный текст.
        amount_text = (
            self.corruption_page
            .corruption_amount_input
            .text()
            .strip()
        )

        # Возвращаем полный снимок текущего состояния формы.
        return {
            "main_settings": {
                "number_of_records_raw": records_text,
                "number_of_records_acceptable": (
                    self.main_settings_page
                    .records_input
                    .hasAcceptableInput()
                ),
                "file_format": (
                    self.main_settings_page
                    .format_input
                    .currentText()
                ),
                "included_fields": (
                    self.main_settings_page
                    .field_selector
                    .get_selected_fields()
                ),
            },

            "corruption": {
                "enabled": (
                    self.corruption_page
                    .corruption_switch
                    .isChecked()
                ),
                "mode": (
                    self.corruption_page
                    .corruption_mode
                    .currentText()
                ),
                "amount_raw": amount_text,
                "amount_acceptable": (
                    self.corruption_page
                    .corruption_amount_input
                    .hasAcceptableInput()
                ),
                "amount_type": (
                    self.corruption_page
                    .corruption_amount_type
                    .currentText()
                ),
                "exclusive": (
                    self.corruption_page
                    .exclusive_switch
                    .isChecked()
                ),
                "corrupted_columns": (
                    self.corruption_page
                    .corrupted_columns_selector
                    .get_selected_fields()
                ),
                "corruption_types": (
                    self.corruption_page
                    .corruption_type_selector
                    .get_selected_fields()
                ),
            },
        }

    def restore_form_state(self):

        # Получаем ранее сохранённое состояние формы.
        saved_form = self.settings.value(
            "saved_form",
            None
        )

        # Если сохранённого состояния нет —
        # восстанавливать нечего.
        if not saved_form:

            return

        # Получаем сохранённые секции формы.
        main_settings = saved_form.get(
            "main_settings",
            {}
        )

        corruption = saved_form.get(
            "corruption",
            {}
        )

        # -------------------------------------------------
        # MAIN SETTINGS
        # -------------------------------------------------

        # Восстанавливаем Number of Records.
        self.main_settings_page.records_input.setText(
            main_settings.get(
                "number_of_records_raw",
                ""
            )
        )

        # Восстанавливаем File Format.
        saved_format = main_settings.get(
            "file_format",
            "CSV"
        )

        format_index = (
            self.main_settings_page
            .format_input
            .findText(saved_format)
        )

        if format_index >= 0:

            self.main_settings_page.format_input.setCurrentIndex(
                format_index
            )

        # Восстанавливаем Included Fields.
        self.main_settings_page.field_selector.set_selected_fields(
            main_settings.get(
                "included_fields",
                []
            )
        )

        # -------------------------------------------------
        # SYNCHRONIZATION MAIN SETTINGS -> CORRUPTION
        # -------------------------------------------------

        # Получаем восстановленное количество записей.
        records_text = (
            self.main_settings_page
            .records_input
            .text()
        )

        records_count = (
            int(records_text)
            if records_text
            else 0
        )

        # Получаем восстановленный список полей.
        selected_fields = (
            self.main_settings_page
            .field_selector
            .get_selected_fields()
        )

        # Передаём восстановленные данные на Corruption.
        #
        # Это важно сделать ДО восстановления
        # Corrupted Columns и Amount Qa,
        # потому что они зависят от Main Settings.
        self.corruption_page.update_available_data(
            records_count,
            selected_fields
        )

        # -------------------------------------------------
        # CORRUPTION
        # -------------------------------------------------

        # Восстанавливаем Corruption Mode.
        saved_mode = corruption.get(
            "mode",
            "Rows"
        )

        mode_index = (
            self.corruption_page
            .corruption_mode
            .findText(saved_mode)
        )

        if mode_index >= 0:

            self.corruption_page.corruption_mode.setCurrentIndex(
                mode_index
            )

        # Восстанавливаем единицу Amount:
        # "%" или "Qa".
        saved_amount_type = corruption.get(
            "amount_type",
            "%"
        )

        amount_type_index = (
            self.corruption_page
            .corruption_amount_type
            .findText(saved_amount_type)
        )

        if amount_type_index >= 0:

            self.corruption_page.corruption_amount_type.setCurrentIndex(
                amount_type_index
            )

        # Восстанавливаем Amount только после Mode и Unit,
        # чтобы валидатор уже имел правильный диапазон.
        self.corruption_page.corruption_amount_input.setText(
            corruption.get(
                "amount_raw",
                ""
            )
        )

        # Восстанавливаем главный переключатель Corrupt Data.
        self.corruption_page.corruption_switch.setChecked(
            corruption.get(
                "enabled",
                False
            )
        )

        # Восстанавливаем Exclusive Corruption.
        self.corruption_page.exclusive_switch.setChecked(
            corruption.get(
                "exclusive",
                False
            )
        )

        # Восстанавливаем выбранные Corrupted Columns.
        #
        # К этому моменту update_available_data()
        # уже пересоздал список доступных колонок.
        self.corruption_page.corrupted_columns_selector.set_selected_fields(
            corruption.get(
                "corrupted_columns",
                []
            )
        )

        # Восстанавливаем выбранные Corruption Types.
        self.corruption_page.corruption_type_selector.set_selected_fields(
            corruption.get(
                "corruption_types",
                []
            )
        )

    def save_form_state(self):

        # Если функция отключена —
        # ничего не сохраняем.
        if not self.remember_settings_enabled:

            return

        # Получаем текущее состояние формы.
        form_state = self.build_form_state()

        # Сохраняем его в постоянное хранилище.
        self.settings.setValue(
            "saved_form",
            form_state
        )

        print()

        print("FORM SAVED")

        pprint(form_state)

        print()


    def update_screen_layout(self, layout_mode):

        # Переключаем приложение в полноэкранный режим.
        if layout_mode == "Fullscreen":

            self.showFullScreen()

        # Возвращаем приложение в обычный оконный режим.
        else:

            self.showNormal()

    def update_remember_settings(self, enabled):

        # Сохраняем состояние функции в памяти текущего запуска.
        self.remember_settings_enabled = enabled

        # Сохраняем состояние между запусками приложения.
        self.settings.setValue(
            "remember_settings",
            enabled
        )

        # Если Remember Settings выключен,
        # старое сохранённое состояние формы больше не нужно.
        if not enabled:

            self.settings.remove("saved_form")


    def closeEvent(self, event):

        # Сохраняем состояние формы
        # перед закрытием приложения.
        self.save_form_state()

        # Передаём обработку Qt.
        super().closeEvent(event)

def main():

    app = QApplication(sys.argv)
     # Применяет общие стили ко всему приложению.
    app.setStyleSheet(load_global_stylesheet())
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
