from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QStackedWidget, QHBoxLayout, QPushButton
)
from PySide6_VerticalQTabWidget import VerticalQTabWidget

from src.config import MONTHS
from src.monthly_page import MonthlyPage, MonthlyIncomeWidget, MonthlyExpanseWidget
from src.summary_page import SummaryPage
from src.user_selection import UserSelection

from src.db import read_db, save_db
from src.utils import create_centered_label


class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.resize(1024, 768)
        self.setWindowTitle("Pénztárkönyv")

        self.summary_page = None
        self.tabs: list[MonthlyPage] = []
        self.current_user: str | None = None

        self.setup_ui()

    def setup_ui(self) -> None:
        main_layout = QVBoxLayout()
        self.stack = QStackedWidget()

        self.db = read_db()
        user_selector_page = self.create_user_selector_page(list(self.db.keys()))

        self.stack.addWidget(user_selector_page)

        main_layout.addWidget(self.stack)
        self.setLayout(main_layout)

    def create_user_selector_page(self, users: list[str]) -> QWidget:
        user_selection_page = UserSelection(users)
        user_selection_page.add_user_to_db.connect(self.add_user_to_db)
        user_selection_page.switch_to_input_page.connect(self.switch_to_input_page)
        return user_selection_page

    @Slot(str)
    def add_user_to_db(self, new_user: str) -> None:
        if new_user in self.db:
            return
        self.db[new_user] = {}
        save_db(self.db)

    @Slot(str, str)
    def switch_to_input_page(self, user: str, year: str) -> None:
        self.current_user = user
        MonthlyIncomeWidget.objects = []
        MonthlyExpanseWidget.objects = []

        if year not in self.db[self.current_user]:
            self.db[self.current_user][year] = {
                "Income": {month: [] for _, month in MONTHS.items()},
                "Expenses": {month: [] for _, month in MONTHS.items()}
            }
            save_db(self.db)

        input_page = self.create_input_page(user, year)
        self.stack.addWidget(input_page)
        self.stack.setCurrentIndex(self.stack.count() - 1)

    @Slot()
    def save_incomes_expenses(self) -> None:
        if self.current_user is None:
            return

        for o in MonthlyIncomeWidget.objects:
            income_data = {
                "serial": o.serial_number,
                "date": o.date_widget.date().toString(),
                "certificate_number": o.certificate_number.value(),
                "title": o.title_input.text(),
                "price": o.price.value(),
                "other": o.other.value(),
                "non-tax": o.non_tax.value(),
                "summary": o.summary.value()
            }

            found_index: int | None = None
            for i, data in enumerate(self.db[self.current_user][o.year]["Income"][o.month]):
                if o.serial_number != data["serial"]:
                    continue
                found_index = i
                break

            if found_index is not None:
                self.db[self.current_user][o.year]["Income"][o.month][found_index] = income_data
            else:
                self.db[self.current_user][o.year]["Income"][o.month].append(income_data)

        for o in MonthlyExpanseWidget.objects:
            expense_data = {
                "serial": o.serial_number,
                "date": o.date_widget.date().toString(),
                "material_price": o.material_price.value(),
                "other": o.other.value(),
                "transmit_price": o.transmit_price.value(),
                "summary": o.summary.value()
            }

            found_index: int | None = None
            for i, data in enumerate(self.db[self.current_user][o.year]["Expenses"][o.month]):
                if o.serial_number != data["serial"]:
                    continue
                found_index = i
                break

            if found_index is not None:
                self.db[self.current_user][o.year]["Expenses"][o.month][found_index] = expense_data
            else:
                self.db[self.current_user][o.year]["Expenses"][o.month].append(expense_data)

        save_db(self.db)

    def create_input_page(self, user: str, year: str) -> QWidget:
        w = QWidget()

        layout = QVBoxLayout()

        header_layout = QHBoxLayout()

        title = create_centered_label("Jelenlegi Felhasználó")
        header_layout.addWidget(title)
        name = create_centered_label(user, set_bold=True)
        header_layout.addWidget(name)
        btn_switch_user_selector_page = QPushButton("Kijelentkezés")
        btn_switch_user_selector_page.pressed.connect(self.switch_user_selector_page)
        header_layout.addWidget(btn_switch_user_selector_page, alignment=Qt.AlignmentFlag.AlignRight)

        layout.addLayout(header_layout)

        tab_widget = VerticalQTabWidget()
        self.summary_page = SummaryPage()
        tab_widget.addTab(self.summary_page, "Összesítés")

        for _, month_name in MONTHS.items():
            monthly_page = MonthlyPage(year, month_name)
            monthly_page.save_db.connect(self.save_incomes_expenses)
            self.tabs.append(monthly_page)
            tab_widget.addTab(self.tabs[-1], month_name)

        layout.addWidget(tab_widget)

        w.setLayout(layout)

        return w

    @Slot()
    def switch_user_selector_page(self) -> None:
        self.stack.setCurrentIndex(0)
