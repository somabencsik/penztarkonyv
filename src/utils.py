from PySide6.QtCore import Qt
from PySide6.QtWidgets import QAbstractSpinBox, QLabel, QLineEdit, QSpinBox


def create_centered_label(
    label: str,
    fixed_width: int | None = None,
    set_bold: bool = False,
    align_center: bool = False
) -> QLabel:
    label = QLabel(label)

    label.setAlignment(Qt.AlignmentFlag.AlignBottom)
    label.setWordWrap(True)

    if fixed_width is not None:
        label.setFixedWidth(fixed_width)
    if set_bold:
        font = label.font()
        font.setBold(True)
        label.setFont(font)
    if align_center:
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    return label


def create_spin_box(width_size: int | None = None, allow_minus: bool = False) -> QSpinBox:
    spin_box = QSpinBox()
    spin_box.setMinimum(0)
    if allow_minus:
        spin_box.setMinimum(-2_000_000_000)
    spin_box.setMaximum(2_000_000_000)
    if width_size is not None:
        spin_box.setFixedWidth(width_size)
    spin_box.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
    return spin_box


def create_line_edit(width_size: int | None) -> QLineEdit:
    line_edit = QLineEdit()
    if width_size is not None:
        line_edit.setFixedWidth(width_size)
    return line_edit