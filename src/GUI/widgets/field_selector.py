# Импортируем базовый виджет Qt.
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QFrame, QCheckBox


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

        # Сохранение чекбоксов по имени поля для дальнейшей обработки
        self.field_checkboxes = {}

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

        # Создаём отдельный чекбокс для каждого доступного поля.
        for field_name in avaliable_fields:

            field_checkbox = QCheckBox(field_name)
            # Обновляем текст кнопки при изменении состояния чекбокса.
            field_checkbox.stateChanged.connect(self.update_button_text)

            # Сохраняем чекбокс, используя имя поля как ключ.
            self.field_checkboxes[field_name] = field_checkbox

            # Добавляем чекбокс в раскрывающуюся панель.
            popup_layout.addWidget(field_checkbox)

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

    # Возвращаем имена всех отмеченных пользователем полей.
        return [
            field_name
            for field_name, checkbox in self.field_checkboxes.items()
            if checkbox.isChecked()
        ]

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