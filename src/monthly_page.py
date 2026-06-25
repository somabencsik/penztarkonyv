from datetime import datetime

from PySide6.QtCore import QDate, Qt
from PySide6.QtWidgets import (
    QAbstractSpinBox,
    QDateTimeEdit,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSpinBox,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)


class MonthlyPage(QWidget):

    INCOME_COLUMN_WIDTH = [50, 65, 80, 270, 80, 80, 80, 80]
    EXPENSE_COLUMN_WIDTH = [50, 65, 330, 80, 80, 80]
    INCOME_SERIAL_NUMBER = 0
    EXPENSE_SERIAL_NUMBER = 0

    def __init__(self, month: str) -> None:
        super().__init__()
        self.month = month

        self.setup_ui()

    def setup_ui(self) -> None:
        layout = QVBoxLayout()

        title = QLabel(self.month)
        title.setAlignment(Qt.AlignmentFlag.AlignRight)
        title_font = title.font()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        tabs = QTabWidget()
        tabs.tabBar().setExpanding(True)
        tabs.setStyleSheet("QTabBar::tab { width: 420px }")
        income_tab = self.income_tab_widget()
        expense_tab = self.expense_tab_widget()
        tabs.addTab(income_tab, "Bevétel")
        tabs.addTab(expense_tab, "Kiadás")

        layout.addWidget(tabs)

        self.setLayout(layout)

    def income_tab_widget(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        header_widget = QWidget()
        header_layout = QGridLayout(header_widget)
        header_layout.setSpacing(4)

        header_labels = []
        headers = [
            "Sorszám",
            "Dátum",
            "Bizonylat szám",
            "Név",
            "Értékesítés",
            "Egyéb",
            "Adóalapjába be nem számító bevétel",
            "Összesen",
        ]

        for col, text in enumerate(headers):
            lbl = QLabel(text)
            label_width = self.INCOME_COLUMN_WIDTH[col]
            if col == 3:
                label_width -= 25
            lbl.setFixedWidth(label_width)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setWordWrap(True)
            header_layout.addWidget(lbl, 0, col)
            header_labels.append(lbl)

        layout.addWidget(header_widget)

        horizontal_line = QFrame()
        horizontal_line.setFrameShape(QFrame.Shape.HLine)
        horizontal_line.setFrameShadow(QFrame.Shadow.Plain)
        layout.addWidget(horizontal_line)

        income_widget = QWidget()

        income_scroll_area = QScrollArea()
        income_scroll_area.setWidgetResizable(True)
        income_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        self.income_layout = QGridLayout(income_widget)
        self.income_layout.setSpacing(4)
        self.income_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        income_scroll_area.setWidget(income_widget)
        layout.addWidget(income_scroll_area)

        btn_add = QPushButton("Bevétel Hozzáadás")
        btn_add.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        btn_add.pressed.connect(self.add_income)
        layout.addWidget(btn_add, 0, Qt.AlignmentFlag.AlignCenter)

        self.add_income()

        widget.setLayout(layout)
        return widget

    def expense_tab_widget(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        header_widget = QWidget()
        header_layout = QGridLayout(header_widget)
        header_layout.setSpacing(4)

        header_labels = []
        headers = [
            "Sorszám",
            "Dátum",
            "Anyag árú",
            "Egyéb",
            "Közvetített szolgáltatás",
            "Összesen"
        ]
        for col, text in enumerate(headers):
            lbl = QLabel(text)
            lbl.setFixedWidth(self.EXPENSE_COLUMN_WIDTH[col])
            alignment = Qt.AlignmentFlag.AlignCenter
            if col > 3:
                alignment = Qt.AlignmentFlag.AlignLeft
            lbl.setAlignment(alignment)
            lbl.setWordWrap(True)
            header_layout.addWidget(lbl, 0, col)
            header_labels.append(lbl)

        layout.addWidget(header_widget)

        horizontal_line = QFrame()
        horizontal_line.setFrameShape(QFrame.Shape.HLine)
        horizontal_line.setFrameShadow(QFrame.Shadow.Plain)
        layout.addWidget(horizontal_line)

        expense_widget = QWidget()

        expense_scroll_area = QScrollArea()
        expense_scroll_area.setWidgetResizable(True)
        expense_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        self.expense_layout = QGridLayout(expense_widget)
        self.expense_layout.setSpacing(4)
        self.expense_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        expense_scroll_area.setWidget(expense_widget)
        layout.addWidget(expense_scroll_area)

        btn_add = QPushButton("Kiadás Hozzáadás")
        btn_add.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        btn_add.pressed.connect(self.add_expense)
        layout.addWidget(btn_add, 0, Qt.AlignmentFlag.AlignCenter)
        
        self.add_expense()

        widget.setLayout(layout)
        return widget

    def add_income(self) -> None:
        self.income_layout.addWidget(MonthlyIncomeWidget(
            self.INCOME_SERIAL_NUMBER,
            self.INCOME_COLUMN_WIDTH
        ))
        self.INCOME_SERIAL_NUMBER += 1

    def add_expense(self) -> None:
        self.expense_layout.addWidget(MonthlyExpanseWidget(
            self.EXPENSE_SERIAL_NUMBER,
            self.EXPENSE_COLUMN_WIDTH
        ))
        self.EXPENSE_SERIAL_NUMBER += 1


class MonthlyIncomeWidget(QWidget):

    objects = []

    def __init__(self, serial_number: int, column_width: list[int]) -> None:
        super().__init__()
        self.serial_number = serial_number
        self.column_width = column_width

        self.setup_ui()
        MonthlyIncomeWidget.objects.append(self)

    def setup_ui(self) -> None:
        layout = QHBoxLayout()

        serial_label = QLabel(str(self.serial_number).rjust(3, "0"))
        serial_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        serial_label.setFixedWidth(self.column_width[0])
        layout.addWidget(serial_label)

        today_date = datetime.now()
        today_date = QDate(today_date.year, today_date.month, today_date.day)
        date_widget = QDateTimeEdit(today_date)
        date_widget.setFixedWidth(self.column_width[1])
        layout.addWidget(date_widget)

        layout.addWidget(self.create_spin_box(self.column_width[2]))

        title_input = QLineEdit()
        title_input.setFixedWidth(self.column_width[3])
        layout.addWidget(title_input)

        for i in range(4):
            layout.addWidget(self.create_spin_box(self.column_width[4 + i]))

        self.setLayout(layout)

    def create_spin_box(self, width_size: int = 0) -> QSpinBox:
        spin_box = QSpinBox()
        spin_box.setMinimum(0)
        spin_box.setMaximum(2_000_000_000)
        spin_box.setFixedWidth(width_size)
        spin_box.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        return spin_box


class MonthlyExpanseWidget(QWidget):
    
    objects = []

    def __init__(self, serial_number: int, column_width: list[int]) -> None:
        super().__init__()
        self.serial_number = serial_number
        self.column_width = column_width

        self.setup_ui()
        MonthlyExpanseWidget.objects.append(self)

    def setup_ui(self) -> None:
        layout = QHBoxLayout()

        serial_label = QLabel(str(self.serial_number).rjust(3, "0"))
        serial_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        serial_label.setFixedWidth(self.column_width[0])
        layout.addWidget(serial_label)

        today_date = datetime.now()
        today_date = QDate(today_date.year, today_date.month, today_date.day)
        date_widget = QDateTimeEdit(today_date)
        date_widget.setFixedWidth(self.column_width[1])
        layout.addWidget(date_widget)

        title_input = QLineEdit()
        title_input.setFixedWidth(self.column_width[2])
        layout.addWidget(title_input)

        for i in range(3):
            layout.addWidget(self.create_spin_box(self.column_width[3 + i]))

        self.setLayout(layout)

    def create_spin_box(self, width_size: int = 0) -> QSpinBox:
        spin_box = QSpinBox()
        spin_box.setMinimum(0)
        spin_box.setMaximum(2_000_000_000)
        spin_box.setFixedWidth(width_size)
        spin_box.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        return spin_box
