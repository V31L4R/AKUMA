from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QComboBox, QPushButton
from pathlib import Path
from PySide6.QtCore import Signal

class OptionsPage(QWidget):

    # Сообщаем MainWindow об изменении режима отображения.
    screen_layout_changed = Signal(str)
    # Сообщаем MainWindow об изменении Remember Settings.
    remember_settings_changed = Signal(bool)

    def __init__(self):
        super().__init__()
        self.setObjectName("options")
        
        # Формируем путь к файлу стилей страницы.
        stylesheet_path = (
            Path(__file__).parent
            / ".."
            / "styles"
            / "pages"
            / "options.qss"
        ).resolve()

        # Открываем файл стилей страницы.
        with open(stylesheet_path, "r", encoding="utf-8") as stylesheet_file:

            # Считываем содержимое файла.

            stylesheet = stylesheet_file.read()
        # Применяем стили страницы Options.
        self.setStyleSheet(stylesheet)
        page_layout = QVBoxLayout()
        self.setLayout(page_layout)
        page_title = QLabel("Options")
        page_layout.addWidget(page_title)
        # Создаём строку настройки языка приложения.
        language_row = QHBoxLayout()

        # Создаём подпись настройки.
        language_label = QLabel("Language")

        # Создаём выпадающий список доступных языков.
        self.language_input = QComboBox()

        # Пока в MVP доступен только английский язык.
        self.language_input.addItem("EN")

        # Задаём имя для стилизации через QSS.
        self.language_input.setObjectName("options_combo")

        # Ограничиваем ширину элемента.
        self.language_input.setFixedWidth(120)

        # Добавляем элементы в строку.
        language_row.addWidget(language_label)
        language_row.addWidget(self.language_input)

        # Не даём строке растягивать контрол на всю страницу.
        language_row.addStretch()

        # Добавляем строку на страницу.
        page_layout.addLayout(language_row)

        # Создаём строку настройки режима окна.
        screen_layout_row = QHBoxLayout()

        # Создаём подпись настройки.
        screen_layout_label = QLabel("Screen Layout")

        # Создаём выпадающий список режимов окна.
        self.screen_layout_input = QComboBox()

        # Добавляем режимы отображения приложения.
        self.screen_layout_input.addItems([
            "Windowed",
            "Fullscreen",
        ])

        # Передаём выбранный режим окна наружу.
        self.screen_layout_input.currentTextChanged.connect(
            self.screen_layout_changed.emit
        )

        # Задаём имя для стилизации через QSS.
        self.screen_layout_input.setObjectName("options_combo")

        # Используем ту же ширину, что и у Language.
        self.screen_layout_input.setFixedWidth(120)

        # Добавляем элементы в строку.
        screen_layout_row.addWidget(screen_layout_label)
        screen_layout_row.addWidget(self.screen_layout_input)
        screen_layout_row.addStretch()

        # Добавляем строку на страницу.
        page_layout.addLayout(screen_layout_row)
        # Создаём строку настройки сохранения предыдущих параметров.
        remember_settings_row = QHBoxLayout()

        # Создаём подпись настройки.
        remember_settings_label = QLabel("Remember Settings")

        # Создаём переключатель.
        self.remember_settings_switch = QPushButton("OFF")

        # Позволяем кнопке хранить состояние ON/OFF.
        self.remember_settings_switch.setCheckable(True)

        # Задаём имя для стилизации.
        self.remember_settings_switch.setObjectName("options_switch")

        # Устанавливаем фиксированную ширину.
        self.remember_settings_switch.setFixedWidth(120)

        # При изменении состояния обновляем переключатель
        # и выполняем связанную с ним логику.
        self.remember_settings_switch.toggled.connect(
            self.update_remember_settings_state
        )

        # Добавляем элементы в строку.
        remember_settings_row.addWidget(remember_settings_label)
        remember_settings_row.addWidget(self.remember_settings_switch)
        remember_settings_row.addStretch()

        # Добавляем строку на страницу.
        page_layout.addLayout(remember_settings_row)
        # Создаём строку настройки проверки обновлений.
        check_updates_row = QHBoxLayout()

        # Создаём подпись настройки.
        check_updates_label = QLabel("Check for Updates")

        # Создаём переключатель.
        self.check_updates_switch = QPushButton("OFF")

        # Позволяем кнопке хранить состояние ON/OFF.
        self.check_updates_switch.setCheckable(True)

        # Задаём имя для стилизации.
        self.check_updates_switch.setObjectName("options_switch")

        # Устанавливаем фиксированную ширину.
        self.check_updates_switch.setFixedWidth(120)

        # При изменении состояния обновляем переключатель
        # и выполняем связанную с ним логику.
        self.check_updates_switch.toggled.connect(
            self.update_check_updates_state
        )

        # Добавляем элементы в строку.
        check_updates_row.addWidget(check_updates_label)
        check_updates_row.addWidget(self.check_updates_switch)
        check_updates_row.addStretch()

        # Добавляем строку на страницу.
        page_layout.addLayout(check_updates_row)
        page_layout.addStretch()

    def update_remember_settings_state(self, enabled):

        # Отображаем текущее состояние переключателя.
        if enabled:

            self.remember_settings_switch.setText("ON")

        else:

            self.remember_settings_switch.setText("OFF")

        self.remember_settings_changed.emit(enabled)


    def update_check_updates_state(self, enabled):

        # Отображаем текущее состояние переключателя.
        if enabled:

            self.check_updates_switch.setText("ON")

        else:

            self.check_updates_switch.setText("OFF")