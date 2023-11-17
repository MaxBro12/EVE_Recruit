from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QPushButton,
)
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon

from core import (
    pjoin_r,
)

from lang import lang
from settings import (
    FILE_LIST_ICON,
    FILE_THEME_ICON,
    FILE_THEME_ICON,
    FILE_LETTER_ICON,
    FILE_ALWAYS_ON_ICON,
    FILE_SQEEZE_ICON,
    FILE_HIDE_ICON,
    FILE_EXIT_ICON,
)


class SmallSizedApp(QWidget):
    def __init__(self, parent, conf) -> None:
        super().__init__(parent=parent)

        self.row = QHBoxLayout()
        self.row.setContentsMargins(5, 5, 5, 5)
        self.row.setSpacing(5)
        self.setLayout(self.row)

        self.list_b = QPushButton(self)
        self.list_b.setToolTip(lang[conf['lang']]['list_b'])
        self.list_b.setIcon(QIcon(pjoin_r(FILE_LIST_ICON)))
        self.list_b.setFixedSize(QSize(25, 25))
        self.row.addWidget(self.list_b)

        self.theme_b = QPushButton(self)
        self.theme_b.setToolTip(lang[conf['lang']]['theme_b'])
        self.theme_b.setIcon(QIcon(pjoin_r(FILE_THEME_ICON)))
        self.theme_b.setFixedSize(QSize(25, 25))
        self.row.addWidget(self.theme_b)

        self.letter_b = QPushButton(self)
        self.letter_b.setToolTip(lang[conf['lang']]['letter_b'])
        self.letter_b.setIcon(QIcon(pjoin_r(FILE_LETTER_ICON)))
        self.letter_b.setFixedSize(QSize(25, 25))
        self.row.addWidget(self.letter_b)

        self.always_on_b = QPushButton(self)
        self.always_on_b.setToolTip(lang[conf['lang']]['always_on_b'])
        self.always_on_b.setIcon(QIcon(pjoin_r(FILE_ALWAYS_ON_ICON)))
        self.always_on_b.setFixedSize(QSize(25, 25))
        self.row.addWidget(self.always_on_b)

        self.sqeeze_b = QPushButton(self)
        self.sqeeze_b.setToolTip(lang[conf['lang']]['sqeeze_b'])
        self.sqeeze_b.setIcon(QIcon(pjoin_r(FILE_SQEEZE_ICON)))
        self.sqeeze_b.setFixedSize(QSize(25, 25))
        self.row.addWidget(self.sqeeze_b)

        if conf['use_self_window']:
            self.hide_b = QPushButton(self)
            self.hide_b.setToolTip(lang[conf['lang']]['hide_b'])
            self.hide_b.setIcon(QIcon(pjoin_r(FILE_HIDE_ICON)))
            self.hide_b.setFixedSize(QSize(25, 25))
            self.row.addWidget(self.hide_b)

            self.exit_b = QPushButton(self)
            self.exit_b.setToolTip(lang[conf['lang']]['exit_b'])
            self.exit_b.setIcon(QIcon(pjoin_r(FILE_EXIT_ICON)))
            self.exit_b.setFixedSize(QSize(25, 25))
            self.row.addWidget(self.exit_b)

