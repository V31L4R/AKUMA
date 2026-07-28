import pytest

from PySide6.QtCore import Qt
from PySide6.QtGui import QIntValidator, QValidator
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication, QLineEdit

from pages.main_settings import MainSettingsPage
from pages.corruption import CorruptionPage


@pytest.fixture(scope="session")
def app():
    """
    Создаёт один QApplication на всю тестовую сессию.

    Без QApplication нельзя создавать QWidget,
    QLineEdit и страницы приложения.
    """
    application = QApplication.instance()

    if application is None:
        application = QApplication([])

    return application


def validator_state_name(state):
    """
    Преобразует состояние Qt-валидатора
    в читаемое название.
    """
    state_names = {
        QValidator.State.Invalid: "Invalid",
        QValidator.State.Intermediate: "Intermediate",
        QValidator.State.Acceptable: "Acceptable",
    }

    return state_names[state]


@pytest.mark.parametrize(
    "value",
    [
        "",
        "0",
        "1",
        "50",
        "100",
        "101",
        "-1",
        "abc",
    ],
)
def test_qintvalidator_diagnostic(value):
    """
    Показывает, как QIntValidator(1, 100)
    классифицирует разные значения.

    Этот тест диагностический:
    он выводит результат для каждого значения.
    """
    validator = QIntValidator(1, 100)

    state, _, _ = validator.validate(value, len(value))

    print(
        f"value={value!r}: "
        f"{validator_state_name(state)}"
    )


def test_zero_is_not_acceptable():
    """
    Ноль не должен считаться полностью валидным
    для диапазона от 1 до 100.
    """
    validator = QIntValidator(1, 100)

    state, _, _ = validator.validate("0", 1)

    assert state != QValidator.State.Acceptable


def test_valid_number_is_acceptable():
    """
    Число внутри диапазона должно быть Acceptable.
    """
    validator = QIntValidator(1, 100)

    state, _, _ = validator.validate("50", 2)

    assert state == QValidator.State.Acceptable


def test_line_edit_can_contain_intermediate_value(app):
    """
    Проверяем критический нюанс Qt:

    QLineEdit может содержать Intermediate-значение,
    хотя оно не является полностью валидным.
    """
    line_edit = QLineEdit()

    validator = QIntValidator(
        1,
        100,
        line_edit,
    )

    line_edit.setValidator(validator)

    line_edit.show()
    line_edit.setFocus()

    QTest.keyClicks(
        line_edit,
        "0",
    )

    assert line_edit.text() == "0"

    assert (
        line_edit.hasAcceptableInput()
        is False
    )


def test_main_settings_validator_range(app):
    """
    Проверяет диапазон Number of Records.
    """
    page = MainSettingsPage()

    validator = page.records_input.validator()

    assert isinstance(
        validator,
        QIntValidator,
    )

    assert validator.bottom() == 1
    assert validator.top() == 10_000_000


def test_main_settings_zero_is_not_acceptable(app):
    """
    Number of Records = 0 не должен
    считаться готовым значением формы.
    """
    page = MainSettingsPage()

    page.records_input.setText("0")

    assert (
        page.records_input.hasAcceptableInput()
        is False
    )


def test_corruption_percent_range(app):
    """
    Для процентов диапазон всегда должен быть 1–100.
    """
    page = CorruptionPage()

    page.update_available_data(
        records_count=10,
        selected_fields=[
            "Name",
            "Email",
            "Phone",
        ],
    )

    page.corruption_amount_type.setCurrentText("%")

    assert (
        page.corruption_amount_validator.bottom()
        == 1
    )

    assert (
        page.corruption_amount_validator.top()
        == 100
    )


def test_corruption_rows_qa_range(app):
    """
    Rows + Qa:

    максимум равен количеству записей.
    """
    page = CorruptionPage()

    page.update_available_data(
        records_count=10,
        selected_fields=[
            "Name",
            "Email",
            "Phone",
        ],
    )

    page.corruption_mode.setCurrentText("Rows")
    page.corruption_amount_type.setCurrentText("Qa")

    assert (
        page.corruption_amount_validator.bottom()
        == 1
    )

    assert (
        page.corruption_amount_validator.top()
        == 10
    )


def test_corruption_cells_qa_range(app):
    """
    Cells + Qa:

    максимум равен:
    records × included fields.
    """
    page = CorruptionPage()

    page.update_available_data(
        records_count=10,
        selected_fields=[
            "Name",
            "Email",
            "Phone",
        ],
    )

    page.corruption_mode.setCurrentText("Cells")
    page.corruption_amount_type.setCurrentText("Qa")

    assert (
        page.corruption_amount_validator.bottom()
        == 1
    )

    assert (
        page.corruption_amount_validator.top()
        == 30
    )


def test_corruption_cells_recalculates_after_fields_change(app):
    """
    Проверяет пересчёт максимума после изменения
    количества Included Fields.
    """
    page = CorruptionPage()

    page.corruption_mode.setCurrentText("Cells")
    page.corruption_amount_type.setCurrentText("Qa")

    page.update_available_data(
        records_count=10,
        selected_fields=[
            "Name",
            "Email",
            "Phone",
        ],
    )

    assert (
        page.corruption_amount_validator.top()
        == 30
    )

    page.update_available_data(
        records_count=10,
        selected_fields=[
            "Name",
            "Email",
        ],
    )

    assert (
        page.corruption_amount_validator.top()
        == 20
    )


def test_corruption_old_value_cleared_after_maximum_reduction(app):
    """
    Если пользователь ввёл значение,
    а затем допустимый максимум уменьшился,
    старое значение должно очищаться.
    """
    page = CorruptionPage()

    page.corruption_mode.setCurrentText("Cells")
    page.corruption_amount_type.setCurrentText("Qa")

    page.update_available_data(
        records_count=10,
        selected_fields=[
            "Name",
            "Email",
            "Phone",
        ],
    )

    page.corruption_amount_input.setText("25")

    assert (
        page.corruption_amount_input.text()
        == "25"
    )

    page.update_available_data(
        records_count=10,
        selected_fields=[
            "Name",
            "Email",
        ],
    )

    assert (
        page.corruption_amount_validator.top()
        == 20
    )

    assert (
        page.corruption_amount_input.text()
        == ""
    )


def test_corruption_qa_disabled_without_main_settings(app):
    """
    Qa должен быть недоступен,
    пока Main Settings не содержит данных.
    """
    page = CorruptionPage()

    page.corruption_amount_type.setCurrentText("Qa")

    page.update_available_data(
        records_count=0,
        selected_fields=[],
    )

    assert (
        page.corruption_amount_input.isEnabled()
        is False
    )

    assert (
        page.corruption_amount_input.placeholderText()
        == "Complete Main Settings"
    )


def test_corruption_zero_is_not_acceptable(app):
    """
    Amount = 0 не должен считаться
    полностью валидным значением.
    """
    page = CorruptionPage()

    page.update_available_data(
        records_count=10,
        selected_fields=[
            "Name",
        ],
    )

    page.corruption_amount_type.setCurrentText("%")
    page.corruption_amount_input.setText("0")

    assert (
        page.corruption_amount_input.hasAcceptableInput()
        is False
    )


def test_corruption_empty_value_is_not_acceptable(app):
    """
    Пустой Amount также не является
    готовым значением формы.
    """
    page = CorruptionPage()

    page.update_available_data(
        records_count=10,
        selected_fields=[
            "Name",
        ],
    )

    page.corruption_amount_input.clear()

    assert (
        page.corruption_amount_input.hasAcceptableInput()
        is False
    )