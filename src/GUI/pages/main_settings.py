from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QComboBox, QPushButton
from PySide6.QtGui import QIntValidator
from widgets.field_selector import FieldsSelector
from pathlib import Path
from PySide6.QtCore import Qt

class MainSettingsPage(QWidget):
    def __init__(self):
        super().__init__()

        # Назначаем странице имя для обращения к ней из QSS.
        self.setObjectName("main_settings")

        # Формируем путь к файлу стилей страницы.
        stylesheet_path = (
            Path(__file__).parent
            / ".."
            / "styles"
            / "pages"
            / "main_settings.qss"
        ).resolve()

        # Открываем файл стилей страницы.
        with open(stylesheet_path, "r", encoding="utf-8") as stylesheet_file:

            # Считываем содержимое файла.
            stylesheet = stylesheet_file.read()

        # Применяем стили только к данной странице.
        self.setStyleSheet(stylesheet)

        page_layout = QVBoxLayout()
        self.setLayout(page_layout)
        page_title = QLabel("Main Settings")
        page_layout.addWidget(page_title)

        # Создаем горизонтальную строку для настройки количества записей.
        records_row = QHBoxLayout()

        # Создаем подпись, объясняющую назначение поля.
        records_label = QLabel("Number of Records")

        # Создаем пустое текстовое поле для количества генерируемых записей.
        self.records_input = QLineEdit()

        # Показываем допустимый диапазон, пока пользователь ничего не ввел.
        self.records_input.setPlaceholderText("1 to 10'000'000")

        # Создаем валидатор, разрешающий только целые числа в допустимом диапазоне.
        records_validator = QIntValidator(1, 10_000_000, self.records_input)

        # Подключаем валидатор к полю ввода.
        self.records_input.setValidator(records_validator)

        # Ограничиваем ширину поля, чтобы оно не растягивалось на всю страницу.
        self.records_input.setFixedWidth(160)

        # Добавляем подпись в строку настройки.
        records_row.addWidget(records_label)

        # Добавляем пустое поле ввода рядом с подписью.
        records_row.addWidget(self.records_input)

        # Прижимаем элементы строки к левому краю страницы.
        records_row.addStretch()

        # Добавляем готовую строку в основной layout страницы.
        page_layout.addLayout(records_row)

        # Создаем горизонтальную строку для выбора формата файла.
        format_row = QHBoxLayout()

        # Создаем подпись для настройки формата файла.
        format_label = QLabel("File Format")

        # Создаем выпадающий список доступных форматов.
        self.format_input = QComboBox()

        # Добавляем поддерживаемые форматы файлов.
        self.format_input.addItem("CSV")
        self.format_input.addItem("JSON")
        self.format_input.addItem("Parquet")
        self.format_input.addItem("XML")
        self.format_input.addItem("Excel (.xlsx)")

        # Ограничиваем ширину выпадающего списка.
        self.format_input.setFixedWidth(160)

        # Добавляем подпись в строку настройки.
        format_row.addWidget(format_label)

        # Добавляем выпадающий список в строку настройки.
        format_row.addWidget(self.format_input)

        # Прижимаем элементы строки к левому краю.
        format_row.addStretch()

        # Добавляем строку выбора формата в основной layout страницы.
        page_layout.addLayout(format_row)

        # Создаём горизонтальную строку для выбора включённых полей.
        fields_row = QHBoxLayout()
        
        # Создаём подпись для выбора полей.
        fields_label = QLabel("Included Fields")
        
        # Создаём экземпляр кастомного виджета выбора полей.
        self.field_selector = FieldsSelector()
        
        # Добавляем подпись в строку.
        fields_row.addWidget(fields_label, alignment=Qt.AlignmentFlag.AlignTop)
        
        # Добавляем виджет выбора полей.
        fields_row.addWidget(
            self.field_selector,
            alignment=Qt.AlignmentFlag.AlignTop
        )
        
        # Прижимаем содержимое строки к левому краю.
        fields_row.addStretch()
        
        # Добавляем строку в основной layout страницы.
        page_layout.addLayout(fields_row)

         # Заполняем свободное вертикальное пространство между формами и кнопкой.
        page_layout.addStretch()

        # Создаём горизонтальную строку для размещения кнопки генерации.
        generate_row = QHBoxLayout()

        # Добавляем растягиваемое пространство слева от кнопки.
        generate_row.addStretch()

        # Создаём кнопку запуска генерации датасета.
        self.generate_button = QPushButton("Generate")

        # Задаём кнопке имя для дальнейшего обращения из QSS.
        self.generate_button.setObjectName("generate_button")

        # Задаём фиксированный размер кнопки согласно текущему макету.
        self.generate_button.setFixedSize(110, 50)

        # Временно подключаем кнопку к проверке получаемых значений формы.
        # self.generate_button.clicked.connect(self.test_form_values)

        # Добавляем кнопку в правую часть строки.
        generate_row.addWidget(self.generate_button)

        # Добавляем строку с кнопкой в основной layout страницы.
        page_layout.addLayout(generate_row)

    #Тест передачи данных
    # def test_form_values(self):

        # Получаем количество записей из текстового поля.
        records_count = self.records_input.text()

        # Получаем выбранный формат файла.
        file_format = self.format_input.currentText()

        # Получаем список выбранных полей из кастомного селектора.
        selected_fields = self.field_selector.get_selected_fields()

        # Временно выводим полученные значения в консоль.
        print("Number of Records:", records_count)
        print("File Format:", file_format)
        print("Included Fields:", selected_fields)
