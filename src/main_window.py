from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel
)
from PySide6_VerticalQTabWidget import VerticalQTabWidget

from src.config import MONTHS
from src.monthly_page import MonthlyPage
from src.summary_page import SummaryPage


class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.resize(1024, 768)
        self.setWindowTitle("Pénztárkönyv")

        self.summary_page = None
        self.tabs: list[MonthlyPage] = []

        self.setup_ui()

    def setup_ui(self) -> None:
        layout = QVBoxLayout()

        title = QLabel("Bencsik")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        title_font = title.font()
        title_font.setPixelSize(36)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        tab_widget = VerticalQTabWidget()
        self.summary_page = SummaryPage()
        tab_widget.addTab(self.summary_page, "Összesítés")

        for _, month_name in MONTHS.items():
            self.tabs.append(MonthlyPage(month_name))
            tab_widget.addTab(self.tabs[-1], month_name)

        layout.addWidget(tab_widget)

        self.setLayout(layout)
