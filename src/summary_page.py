from PySide6.QtWidgets import QWidget, QLabel


class SummaryPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setup_ui()

    def setup_ui(self) -> None:
        ...