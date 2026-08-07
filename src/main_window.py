from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QStackedWidget, QHBoxLayout, QPushButton
)
from PySide6_VerticalQTabWidget import VerticalQTabWidget

from src.config import MONTHS
from src.monthly_page import MonthlyPage
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

    @Slot(str, int)
    def switch_to_input_page(self, user: str, year: int) -> None:
        input_page = self.create_input_page(user, year)
        self.stack.addWidget(input_page)
        self.stack.setCurrentIndex(self.stack.count() - 1)

    def create_input_page(self, user: str, year: int) -> QWidget:
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
            self.tabs.append(MonthlyPage(year, month_name))
            tab_widget.addTab(self.tabs[-1], month_name)

        layout.addWidget(tab_widget)

        w.setLayout(layout)

        return w

    @Slot()
    def switch_user_selector_page(self) -> None:
        self.stack.setCurrentIndex(0)
