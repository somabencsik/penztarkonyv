from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QSpinBox, QAbstractSpinBox


def create_centered_label(label: str, fixed_width: Optional[int] = None, set_bold: bool = False) -> QLabel:
    label = QLabel(label)

    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label.setWordWrap(True)
    if fixed_width is not None:
        label.setFixedWidth(fixed_width)
    if set_bold:
        font = label.font()
        font.setBold(True)
        label.setFont(font)

    return label


def create_spin_box(width_size: Optional[int] = None) -> QSpinBox:
    spin_box = QSpinBox()
    spin_box.setMinimum(0)
    spin_box.setMaximum(2_000_000_000)
    if width_size is not None:
        spin_box.setFixedWidth(width_size)
    spin_box.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
    return spin_box