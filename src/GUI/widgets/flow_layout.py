# Импортируем базовый класс layout.
from PySide6.QtWidgets import QLayout

# Импортируем вспомогательные Qt-классы для расчёта геометрии.
from PySide6.QtCore import QPoint, QRect, QSize, Qt


# Layout, который размещает элементы слева направо
# и переносит их на новую строку при нехватке ширины.
class FlowLayout(QLayout):

    def __init__(self, parent=None, margin=0, horizontal_spacing=6, vertical_spacing=6):

        # Инициализируем родительский QLayout.
        super().__init__(parent)

        # Храним элементы, добавленные в layout.
        self.items = []

        # Сохраняем расстояния между элементами.
        self.horizontal_spacing = horizontal_spacing
        self.vertical_spacing = vertical_spacing

        # Устанавливаем внешние отступы layout.
        self.setContentsMargins(margin, margin, margin, margin)

    def addItem(self, item):

        # Добавляем новый элемент во внутренний список.
        self.items.append(item)

    def count(self):

        # Возвращаем количество элементов в layout.
        return len(self.items)

    def itemAt(self, index):

        # Возвращаем элемент по индексу.
        if 0 <= index < len(self.items):
            return self.items[index]

        return None

    def takeAt(self, index):

        # Извлекаем элемент из layout по индексу.
        if 0 <= index < len(self.items):
            return self.items.pop(index)

        return None

    def expandingDirections(self):

        # Layout не требует обязательного растяжения
        # по горизонтали или вертикали.
        return Qt.Orientation(0)

    def hasHeightForWidth(self):

        # Высота layout зависит от доступной ширины.
        return True

    def heightForWidth(self, width):

        # Рассчитываем высоту layout для заданной ширины,
        # не изменяя реальное положение элементов.
        return self._do_layout(
            QRect(0, 0, width, 0),
            test_only=True
        )

    def setGeometry(self, rectangle):

        # Передаём Qt базовую геометрию layout.
        super().setGeometry(rectangle)

        # Размещаем элементы внутри доступной области.
        self._do_layout(rectangle, test_only=False)

    def sizeHint(self):

        # Возвращаем рекомендуемый размер layout.
        return self.minimumSize()

    def minimumSize(self):

        # Рассчитываем минимальную область,
        # необходимую для всех элементов.
        size = QSize()

        for item in self.items:
            size = size.expandedTo(item.minimumSize())

        margins = self.contentsMargins()

        size += QSize(
            margins.left() + margins.right(),
            margins.top() + margins.bottom()
        )

        return size

    def _do_layout(self, rectangle, test_only):

        # Получаем внешние отступы layout.
        margins = self.contentsMargins()

        # Начальная координата первого элемента.
        x = rectangle.x() + margins.left()
        y = rectangle.y() + margins.top()

        # Высота текущей строки.
        current_row_height = 0

        # Правая граница доступной области.
        available_right = rectangle.right() - margins.right()

        # Последовательно размещаем каждый элемент.
        for item in self.items:

            widget = item.widget()

            # Пропускаем только элементы, которые были скрыты явно.
            # isVisible() возвращает False и тогда, когда скрыт родительский popup.
            # Из-за этого FlowLayout не учитывал чипсы при первом расчёте размера.
            if widget is not None and widget.isHidden():
                continue

            # Получаем рекомендуемый размер текущего элемента.
            item_size = item.sizeHint()

            # Рассчитываем позицию правой границы элемента.
            next_x = (
                x
                + item_size.width()
                + self.horizontal_spacing
            )

            # Если элемент не помещается в текущую строку,
            # переносим его на следующую.
            if (
                next_x - self.horizontal_spacing > available_right
                and current_row_height > 0
            ):
                x = rectangle.x() + margins.left()
                y += current_row_height + self.vertical_spacing

                next_x = (
                    x
                    + item_size.width()
                    + self.horizontal_spacing
                )

                current_row_height = 0

            # При реальном размещении задаём геометрию элемента.
            if not test_only:
                item.setGeometry(
                    QRect(
                        QPoint(x, y),
                        item_size
                    )
                )

            # Передвигаем позицию для следующего элемента.
            x = next_x

            # Обновляем высоту текущей строки.
            current_row_height = max(
                current_row_height,
                item_size.height()
            )

        # Возвращаем итоговую высоту layout.
        return (
            y
            + current_row_height
            - rectangle.y()
            + margins.bottom()
        )