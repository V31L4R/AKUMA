from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QFrame, QLineEdit, QComboBox, QMessageBox
from PySide6.QtGui import QIntValidator
from pathlib import Path
from widgets.field_selector import FieldsSelector

class CorruptionPage(QWidget):
    def __init__(self):
        super().__init__()
        # Назначаем имя страницы для обращения из QSS.
        self.setObjectName("corruption")

        # Формируем путь к файлу стилей страницы Corruption.
        stylesheet_path = (
            Path(__file__).parent
            / ".."
            / "styles"
            / "pages"
            / "corruption.qss"
        ).resolve()

        # Открываем файл стилей страницы.
        with open(stylesheet_path, "r", encoding="utf-8") as stylesheet_file:

            # Считываем содержимое файла.
            stylesheet = stylesheet_file.read()

        # Применяем стили только к странице Corruption.
        self.setStyleSheet(stylesheet)

        page_layout = QVBoxLayout()
        self.setLayout(page_layout)
        page_title = QLabel("Corruption")
        page_layout.addWidget(page_title)
        # Создаём строку главного переключателя корруптора.
        corruption_switch_row = QHBoxLayout()

        # Создаём подпись переключателя.
        corruption_switch_label = QLabel("Corrupt Data")

        # Создаём кнопку с двумя состояниями: Off и On.
        self.corruption_switch = QPushButton("OFF")

        # Разрешаем кнопке хранить состояние переключателя.
        self.corruption_switch.setCheckable(True)

        # Назначаем имя для стилизации переключателя через QSS.
        self.corruption_switch.setObjectName("corruption_switch")

        # Ограничиваем размер кнопки переключателя.
        self.corruption_switch.setFixedSize(50, 28)

        # По умолчанию корруптор выключен.
        self.corruption_switch.setChecked(False)

        # Подключаем изменение состояния переключателя.
        self.corruption_switch.toggled.connect(
            self.update_corruption_state
        )

        # Добавляем подпись и переключатель в строку.
        corruption_switch_row.addWidget(corruption_switch_label)
        corruption_switch_row.addWidget(self.corruption_switch)

        # Прижимаем строку к левому краю.
        corruption_switch_row.addStretch()

        # Добавляем строку переключателя на страницу.
        page_layout.addLayout(corruption_switch_row)

        # Создаём контейнер для всех настроек корруптора.
        # Позже внутрь него войдут:
        # Amount of Corrupt Data,
        # Exclusive Corruption,
        # Corrupted Columns,
        # Corruption Type.
        self.corruption_controls = QFrame()

        # Назначаем имя контейнера для обращения из QSS.
        self.corruption_controls.setObjectName("corruption_controls")

        # Создаём вертикальный layout настроек корруптора.
        self.corruption_controls_layout = QVBoxLayout()

        # Убираем внешние отступы контейнера.
        self.corruption_controls_layout.setContentsMargins(0, 0, 0, 0)

        # Назначаем layout контейнеру.
        self.corruption_controls.setLayout(
            self.corruption_controls_layout
        )

        # Создаём строку настройки количества повреждаемых записей.
        amount_row = QHBoxLayout()

        # Создаём подпись для количества повреждаемых данных.
        amount_label = QLabel("Amount of Corrupt Data")

        # Создаём поле ввода количества.
        self.corruption_amount_input = QLineEdit()

        # Показываем допустимое значение, пока поле пустое.
        self.corruption_amount_input.setPlaceholderText("1 to 100")

        # Создаём валидатор количества повреждаемых данных.
        # Сохраняем его как атрибут класса, потому что верхняя граница
        # будет меняться в зависимости от данных Main Settings.
        self.corruption_amount_validator = QIntValidator(
            1,
            100,
            self.corruption_amount_input
        )

        # Подключаем валидатор к полю ввода.
        self.corruption_amount_input.setValidator(
            self.corruption_amount_validator
        )
        # Ограничиваем ширину числового поля.
        self.corruption_amount_input.setFixedWidth(180)

        # Создаём выпадающий список единиц измерения.
        self.corruption_amount_type = QComboBox()

        # Добавляем процентное значение.
        self.corruption_amount_type.addItem("%")

        # Добавляем абсолютное количество записей.
        self.corruption_amount_type.addItem("Qa")

        # При переключении единицы измерения
        # пересчитываем допустимый диапазон поля Amount.
        self.corruption_amount_type.currentTextChanged.connect(
           self.update_amount_validator
        )

        # Ограничиваем ширину выпадающего списка.
        self.corruption_amount_type.setFixedWidth(60)

        # Добавляем элементы в строку.
        amount_row.addWidget(amount_label)
        amount_row.addWidget(self.corruption_amount_input)
        amount_row.addWidget(self.corruption_amount_type)

        # Прижимаем содержимое строки к левому краю.
        amount_row.addStretch()

        # Добавляем строку в контейнер настроек корруптора.
        self.corruption_controls_layout.addLayout(amount_row)

        # Создаём строку режима коррупции.
        mode_row = QHBoxLayout()

        # Создаём подпись режима.
        mode_label = QLabel("Corruption Mode")

        # Создаём выпадающий список.
        self.corruption_mode = QComboBox()

        # Добавляем режимы.
        self.corruption_mode.addItem("Rows")
        self.corruption_mode.addItem("Cells")

        # Ограничиваем ширину списка.
        self.corruption_mode.setFixedWidth(120)

        # При смене режима пересчитываем допустимый максимум.
        self.corruption_mode.currentTextChanged.connect(
            self.update_amount_validator
        )

        # Добавляем элементы строки.
        mode_row.addWidget(mode_label)
        mode_row.addWidget(self.corruption_mode)

        # Прижимаем содержимое влево.
        mode_row.addStretch()

        # Добавляем строку на страницу.
        self.corruption_controls_layout.addLayout(mode_row)

        # Создаём строку переключателя Exclusive Corruption.
        exclusive_row = QHBoxLayout()

        # Создаём подпись переключателя.
        exclusive_label = QLabel("Exclusive Corruption")

        # Создаём кнопку с двумя состояниями: OFF и ON.
        self.exclusive_switch = QPushButton("OFF")

        # Разрешаем кнопке хранить состояние переключателя.
        self.exclusive_switch.setCheckable(True)

        # Назначаем имя для стилизации через QSS.
        self.exclusive_switch.setObjectName("exclusive_switch")

        # Ограничиваем размер переключателя.
        self.exclusive_switch.setFixedSize(50, 28)

        # По умолчанию Exclusive Corruption выключен.
        self.exclusive_switch.setChecked(False)

        # Подключаем изменение состояния переключателя.
        self.exclusive_switch.toggled.connect(
        self.update_exclusive_state
        )

        # Добавляем подпись и переключатель в строку.
        exclusive_row.addWidget(exclusive_label)
        exclusive_row.addWidget(self.exclusive_switch)

        # Прижимаем строку к левому краю.
        exclusive_row.addStretch()

        # Добавляем строку в контейнер настроек корруптора.
        self.corruption_controls_layout.addLayout(exclusive_row)

        # По умолчанию все настройки видимы, но недоступны.
        self.corruption_controls.setEnabled(False)

        #Добавляем контейнер настроек на страницу.
        page_layout.addWidget(self.corruption_controls)

        # Храним актуальное количество записей,
        # полученное со страницы Main Settings.
        self.available_records_count = 0

        # Храним актуальный список полей,
        # выбранных на странице Main Settings.
        self.available_fields = []

        page_layout.addStretch()

        # Создаём строку выбора повреждаемых колонок.
        corrupted_columns_row = QHBoxLayout()

        # Создаём подпись.
        corrupted_columns_label = QLabel("Corrupted Columns")

        # Создаём селектор.
        self.corrupted_columns_selector = FieldsSelector([])

        # Пока Exclusive выключен —
        # ручной выбор колонок запрещён.
        self.corrupted_columns_selector.setEnabled(False)

        corrupted_columns_row.addWidget(
            corrupted_columns_label
        )

        corrupted_columns_row.addWidget(
            self.corrupted_columns_selector
        )

        corrupted_columns_row.addStretch()

        self.corruption_controls_layout.addLayout(
        corrupted_columns_row
        )

    def update_corruption_state(self, enabled):

        # Если пользователь выключает корруптор,
        # отключаем его настройки и возвращаем текст OFF.
        if not enabled:

            self.corruption_controls.setEnabled(False)
            self.corruption_switch.setText("OFF")

            return

        # Получаем количество выбранных полей.
        selected_fields_count = len(self.available_fields)

        # По умолчанию предупреждение отсутствует.
        warning_message = None

        # Не указаны ни количество записей, ни поля.
        if (
            self.available_records_count <= 0
            and selected_fields_count <= 0
        ):

            warning_message = (
                "Please specify Number of Records and Included Fields "
                "on the Main Settings page."
            )

        # Не указано только количество записей.
        elif self.available_records_count <= 0:

            warning_message = (
                "Please specify Number of Records "
                "on the Main Settings page."
            )

        # Не выбраны только поля.
        elif selected_fields_count <= 0:

            warning_message = (
                "Please specify Included Fields "
                "on the Main Settings page."
            )

        # Если обязательные значения отсутствуют.
        if warning_message is not None:

            # Блокируем сигнал, чтобы программный возврат в OFF
            # не вызвал этот же метод повторно.
            self.corruption_switch.blockSignals(True)

            # Возвращаем кнопку в выключенное состояние.
            self.corruption_switch.setChecked(False)
            self.corruption_switch.setText("OFF")

            # Возвращаем обработку сигналов.
            self.corruption_switch.blockSignals(False)

            # Настройки остаются выключенными.
            self.corruption_controls.setEnabled(False)

            # Показываем предупреждение.
            QMessageBox.warning(
                self,
                "Main Settings Required",
                warning_message,
            )

            return

        # Все обязательные значения заполнены:
        # разрешаем включить корруптор.
        self.corruption_controls.setEnabled(True)
        self.corruption_switch.setText("ON")

    def update_available_data(self, records_count, selected_fields):

        # Сохраняем актуальное количество записей
        # со страницы Main Settings.
        self.available_records_count = records_count

        # Сохраняем копию списка выбранных полей.
        #
        # Копия нужна, чтобы CorruptionPage хранила собственное
        # текущее состояние, а не зависела от внешнего списка.
        self.available_fields = list(selected_fields)

        # Полностью пересоздаём список
        # доступных колонок.
        self.corrupted_columns_selector.set_available_fields(
            self.available_fields
        )

        # После получения новых данных
        # пересчитываем допустимый диапазон Amount.
        self.update_amount_validator()

        # Если корруптор уже включён,
        # но обязательные настройки Main Settings стали невалидными,
        # автоматически возвращаем переключатель в OFF.
        if (
            self.corruption_switch.isChecked()
            and (
                self.available_records_count <= 0
                or len(self.available_fields) <= 0
            )
        ):

            # Блокируем сигнал, чтобы программное переключение
            # не вызвало обработчик повторно.
            self.corruption_switch.blockSignals(True)

            # Возвращаем переключатель в выключенное состояние.
            self.corruption_switch.setChecked(False)
            self.corruption_switch.setText("OFF")

            # Возвращаем обработку сигналов.
            self.corruption_switch.blockSignals(False)

            # Отключаем все настройки корруптора.
            self.corruption_controls.setEnabled(False)

    def update_amount_validator(self):

        # Получаем выбранную единицу измерения:
        # "%" или "Qa".
        amount_unit = self.corruption_amount_type.currentText()

        # Получаем выбранный режим коррупции.
        corruption_mode = self.corruption_mode.currentText()

        # В процентном режиме диапазон всегда остаётся от 1 до 100.
        if amount_unit == "%":

            maximum_value = 100

            # Показываем пользователю текущий допустимый диапазон.
            self.corruption_amount_input.setPlaceholderText(
                "1 to 100"
            )

            # Поле доступно для ввода.
            self.corruption_amount_input.setEnabled(True)

        # В режиме Qa считаем абсолютное количество доступных ячеек.
        else:

            # Количество доступных ячеек:
            #
            # количество строк × количество выбранных колонок.
            if corruption_mode == "Rows":

                maximum_value = self.available_records_count

            else:

                maximum_value = (
                    self.available_records_count
                    * len(self.available_fields)
                )
            # Если количество строк не введено
            # или не выбрано ни одного поля.
            if maximum_value < 1:

                # Временно оставляем технический диапазон 1–1.
                self.corruption_amount_validator.setRange(1, 1)

                # Удаляем значение, которое больше нельзя проверить.
                self.corruption_amount_input.clear()

                # Объясняем, почему поле недоступно.
                self.corruption_amount_input.setPlaceholderText(
                    "Complete Main Settings"
                )

                # Запрещаем ввод до заполнения Main Settings.
                self.corruption_amount_input.setEnabled(False)

                return

            # Показываем рассчитанный максимум.
            #
            # Например:
            # 10'000
            # вместо:
            # 10000
        
            self.corruption_amount_input.setPlaceholderText(
                f"1 to {maximum_value}"
            )

            # Разрешаем ввод после успешного расчёта.
            self.corruption_amount_input.setEnabled(True)

        # Устанавливаем новый допустимый диапазон.
        self.corruption_amount_validator.setRange(
        1,
            maximum_value
        )

        # Получаем уже введённое значение.
        current_text = self.corruption_amount_input.text()

        # Если поле не пустое — проверяем старое значение
        # относительно нового максимума.
        if current_text:

            current_value = int(current_text)

            # Если старое значение больше нового максимума,
            # очищаем поле.
            if current_value > maximum_value:

                self.corruption_amount_input.clear()

    def update_exclusive_state(self, enabled):
    
                # Обновляем текст переключателя.
                if enabled:
    
                    self.exclusive_switch.setText("ON")
    
                else:
    
                    self.exclusive_switch.setText("OFF")
                self.corrupted_columns_selector.setEnabled(
                    enabled
                )


    