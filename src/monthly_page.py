from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout


class MonthlyPage(QWidget):
    def __init__(self, month: str) -> None:
        super().__init__()
        self.month = month

        self.setup_ui()

    def setup_ui(self) -> None:
        layout = QVBoxLayout()

        title = QLabel(self.month)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = title.font()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        self.setLayout(layout)