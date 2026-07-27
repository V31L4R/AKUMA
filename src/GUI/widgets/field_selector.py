# Импортируем базовый виджет Qt.
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QFrame
# Импортируем layout с автоматическим переносом чипсов.
from widgets.flow_layout import FlowLayout
# Импортируем механизм сигналов Qt.
from PySide6.QtCore import Signal


# Виджет выбора полей для генерации датасета.
class FieldsSelector(QWidget):

    # Сообщает внешним компонентам, что выбор полей изменился.
    selection_changed = Signal()

    # Создаём экземпляр виджета.
    def __init__(self, available_fields=None):

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

        # Создаём layout, размещающий чипсы слева направо
        # с автоматическим переносом на следующую строку.
        popup_layout = FlowLayout(
            margin=8,
            horizontal_spacing=6,
            vertical_spacing=6
        )

        # Назначаем Layout раскрывающейся панели
        self.popup.setLayout(popup_layout)

        # Сохраняем чипсы по имени поля для дальнейшей обработки.
        self.field_chips = {}

        # Определяем доступные поля для первой версии селектора
        
        # Если список не передан,
        # используем стандартный набор полей.
        if available_fields is None:

            available_fields = [
                "Name",
                "Surname",
                "Age",
                "Email",
             "Phone",
             "City",
             "Country",
            ]

        # Создаём отдельный чип для каждого доступного поля.
        for field_name in available_fields:

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

        # Пока скрываем панель при запуске приложения.
        self.popup.hide()
        
        # Добавляем панель под кнопкой.
        selector_layout.addWidget(self.popup)

    def toggle_popup(self):

        # Определяем новое состояние раскрывающейся панели.
         popup_is_open = not self.popup.isVisible()

            # Показываем или скрываем панель.
         self.popup.setVisible(popup_is_open)

         # После раскрытия заставляем layout заново рассчитать
         # расположение и необходимую высоту панели.
         if popup_is_open:

            self.popup.layout().invalidate()
            self.popup.layout().activate()
            self.popup.updateGeometry()

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

        # Сообщаем внешним компонентам, что набор выбранных полей изменился.
        self.selection_changed.emit()

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

    def set_available_fields(self, available_fields):

        # Полностью удаляем старые чипы.
        while self.popup.layout().count():

            layout_item = self.popup.layout().takeAt(0)

            if layout_item.widget():

                layout_item.widget().deleteLater()

            # Очищаем словарь.
            self.field_chips.clear()

        # Создаём новый набор чипов.
        for field_name in available_fields:

            field_chip = QPushButton(f"{field_name} +")

            field_chip.setFlat(True)
            field_chip.setCheckable(True)

            field_chip.setProperty(
                "field_name",
                field_name
            )

            field_chip.setObjectName("field_chip")

            field_chip.toggled.connect(
                lambda checked, chip=field_chip:
                self.update_chip_state(chip, checked)
            )

            self.field_chips[field_name] = field_chip

            self.popup.layout().addWidget(field_chip)

        # Возвращаем стандартный текст кнопки.
        self.update_button_text()