# Импортируем базовый виджет Qt.
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QFrame


# Виджет выбора полей для генерации датасета.
class FieldsSelector(QWidget):

    # Создаём экземпляр виджета.
    def __init__(self):

        # Инициализируем родительский класс QWidget.
        super().__init__()

        # Создаём основной вертикальный layout компонента.
        selector_layout = QVBoxLayout()
        
        # Убираем внешние отступы, чтобы виджет не добавлял лишнее пространство.
        selector_layout.setContentsMargins(0, 0, 0, 0)
        
        # Устанавливаем layout для текущего виджета.
        self.setLayout(selector_layout)
        
        # Создаём кнопку, которая открывает и закрывает список полей.
        self.trigger_button = QPushButton("Select Fields ▼")
        
        # Задаём имя для обращения к кнопке из QSS.
        self.trigger_button.setObjectName("fields_selector_trigger")
        
        # Устанавливаем минимальную ширину элемента.
        self.trigger_button.setMinimumWidth(240)
        
        # Подключаем нажатие кнопки к переключению видимости панели.
        self.trigger_button.clicked.connect(self.toggle_popup)
        
        # Добавляем кнопку в layout виджета.
        selector_layout.addWidget(self.trigger_button)
        
        # Создаём панель, в которой позже будут размещены доступные поля.
        self.popup = QFrame()
        
        # Задаём имя панели для обращения из QSS.
        self.popup.setObjectName("fields_selector_popup")

        # Создаем вертикальный Layout для содержимого раскрывающейся панели
        popup_layout = QVBoxLayout()

        # Устанавливаем внутренние отступы панели
        popup_layout.setContentsMargins(8, 8, 8, 8)

        # Назначаем Layout раскрывающейся панели
        self.popup.setLayout(popup_layout)

        # Сохраняем чипсы по имени поля для дальнейшей обработки.
        self.field_chips = {}

        # Определяем доступные поля для первой версии селектора
        
        avaliable_fields = [
            "Name", 
            "Surname",
            "Age",
            "Email",
            "Phone",
            "City",
            "Country",
        ]

        # Создаём отдельный чип для каждого доступного поля.
        for field_name in avaliable_fields:

            # Создаём кнопку с названием поля и символом добавления.
            field_chip = QPushButton(f"{field_name} +")

            # Отключаем нативный рамочный стиль кнопки,
            # чтобы QSS полностью управлял её фоном.
            field_chip.setFlat(True)

            # Разрешаем кнопке хранить два состояния:
            # выбрана и не выбрана.
            field_chip.setCheckable(True)

            # Сохраняем исходное имя поля внутри самого чипа.
            field_chip.setProperty("field_name", field_name)

            # Задаём общее имя для стилизации всех чипсов через QSS.
            field_chip.setObjectName("field_chip")

            # При клике обновляем внешний вид чипса
            # и текст основной кнопки селектора.
            field_chip.toggled.connect(
                lambda checked, chip=field_chip: self.update_chip_state(chip, checked)
            )

            # Сохраняем чип, используя имя поля как ключ.
            self.field_chips[field_name] = field_chip

            # Добавляем чип в раскрывающуюся панель.
            popup_layout.addWidget(field_chip)

        # Задаём временную минимальную высоту, пока панель ещё не содержит полей.
        self.popup.setMinimumHeight(80)
        
        # Пока скрываем панель при запуске приложения.
        self.popup.hide()
        
        # Добавляем панель под кнопкой.
        selector_layout.addWidget(self.popup)

    def toggle_popup(self):

        # Переключаем видимость панели выбора полей.
        self.popup.setVisible(not self.popup.isVisible())

    def get_selected_fields(self):

        # Возвращаем имена всех выбранных пользователем полей.
        return [
            field_name
            for field_name, chip in self.field_chips.items()
            if chip.isChecked()
        ]

    def update_chip_state(self, chip, checked):

        # Получаем исходное имя поля из свойства чипса.
        field_name = chip.property("field_name")

        # Если чип выбран — убираем символ добавления.
        if checked:

            chip.setText(field_name)

        # Если выбор снят — возвращаем символ добавления.
        else:

            chip.setText(f"{field_name} +")

        # Обновляем текст основной кнопки селектора.
        self.update_button_text()

    def update_button_text(self):

        # Получаем список выбранных пользователем полей.
        selected_fields = self.get_selected_fields()

        # Если ничего не выбрано — возвращаем исходный текст.
        if not selected_fields:

            self.trigger_button.setText("Select Fields ▼")

            return

        # Если выбрано не больше двух полей — показываем их названия.
        if len(selected_fields) <= 2:

            text = ", ".join(selected_fields)

        # Если полей больше двух — показываем первые два и количество остальных.
        else:

            text = (
                f"{selected_fields[0]}, "
                f"{selected_fields[1]} "
                f"+{len(selected_fields) - 2}"
            )

        # Обновляем текст кнопки.
        self.trigger_button.setText(f"{text} ▼")