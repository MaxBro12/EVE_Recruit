from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QComboBox,
    QLineEdit,
    QPlainTextEdit,
)
from PySide6.QtCore import Qt, QSize
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
    FILE_DELETE_B_ICON,
    FILE_HIDE_ICON,
    FILE_EXIT_ICON,
)


class FullSizedApp(QWidget):
    def __init__(self, parent, conf) -> None:
        super().__init__(parent=parent)

        # ? Верхняя панель ====================================================
        self.row_top = QHBoxLayout()
        self.row_top.setContentsMargins(0, 0, 0, 0)
        self.row_top.setSpacing(5)
        # self.row_top.setAlignment(
        #     Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop
        # )

        self.profile_ch = QComboBox(self)
        self.profile_ch.setPlaceholderText(lang[conf['lang']]['profile_ch'])
        self.profile_ch.setFixedHeight(25)
        self.row_top.addWidget(self.profile_ch, 0)

        self.delete_b = QPushButton(self)
        self.delete_b.setToolTip(lang[conf['lang']]['delete_b'])
        self.delete_b.setIcon(QIcon(pjoin_r(FILE_DELETE_B_ICON)))
        self.delete_b.setFixedSize(QSize(25, 25))
        self.row_top.addWidget(self.delete_b, 0)

        self.row_top.addSpacing(10)

        self.new_profile = QLineEdit(self)
        self.new_profile.setToolTip(lang[conf['lang']]['new_profile'])
        self.new_profile.setMaximumHeight(25)
        self.row_top.addWidget(self.new_profile)

        # self.add_profile = QPushButton(self)
        # self.add_profile.setToolTip(lang[conf['lang']]['add_profile'])
        # self.add_profile.setIcon(QIcon(pjoin_r(FILE_ADD_ICON)))
        # self.add_profile.setFixedSize(QSize(25, 25))
        # self.row_top.addWidget(self.add_profile, 0)

        self.row_top.addSpacing(10)

        self.always_on_b = QPushButton(self)
        self.always_on_b.setToolTip(lang[conf['lang']]['always_on_b'])
        self.always_on_b.setIcon(QIcon(pjoin_r(FILE_ALWAYS_ON_ICON)))
        self.always_on_b.setFixedSize(QSize(25, 25))
        self.row_top.addWidget(self.always_on_b, 0)

        self.sqeeze_b = QPushButton(self)
        self.sqeeze_b.setToolTip(lang[conf['lang']]['sqeeze_b'])
        self.sqeeze_b.setIcon(QIcon(pjoin_r(FILE_SQEEZE_ICON)))
        self.sqeeze_b.setFixedSize(QSize(25, 25))
        self.row_top.addWidget(self.sqeeze_b, 0)

        if conf['use_self_window']:
            self.hide_b = QPushButton(self)
            self.hide_b.setToolTip(lang[conf['lang']]['hide_b'])
            self.hide_b.setIcon(QIcon(pjoin_r(FILE_HIDE_ICON)))
            self.hide_b.setFixedSize(QSize(25, 25))
            self.row_top.addWidget(self.hide_b, 0)

        if conf['use_self_window']:
            self.exit_b = QPushButton(self)
            self.exit_b.setToolTip(lang[conf['lang']]['exit_b'])
            self.exit_b.setIcon(QIcon(pjoin_r(FILE_EXIT_ICON)))
            self.exit_b.setFixedSize(QSize(25, 25))
            self.row_top.addWidget(self.exit_b, 0)

        # ? Панель списка пилотов =============================================
        self.row_list = QHBoxLayout()
        self.row_list.setContentsMargins(0, 0, 0, 0)
        self.row_list.setSpacing(5)

        self.list_b = QPushButton(self)
        self.list_b.setToolTip(lang[conf['lang']]['list_b'])
        self.list_b.setIcon(QIcon(pjoin_r(FILE_LIST_ICON)))
        self.list_b.setFixedSize(QSize(25, 25))
        self.row_list.addWidget(self.list_b)

        self.list_text = QLineEdit(self)
        self.list_text.setToolTip(lang[conf['lang']]['list_text'])
        self.list_text.setMaximumHeight(25)
        self.row_list.addWidget(self.list_text)

        # ? Панель темы письма ================================================
        self.row_theme = QHBoxLayout()
        self.row_theme.setContentsMargins(0, 0, 0, 0)
        self.row_theme.setSpacing(5)

        self.theme_b = QPushButton(self)
        self.theme_b.setToolTip(lang[conf['lang']]['theme_b'])
        self.theme_b.setIcon(QIcon(pjoin_r(FILE_THEME_ICON)))
        self.theme_b.setFixedSize(QSize(25, 25))
        self.row_theme.addWidget(self.theme_b)

        self.theme_text = QLineEdit(self)
        self.theme_text.setToolTip(lang[conf['lang']]['theme_text'])
        self.theme_text.setMaximumHeight(25)
        self.row_theme.addWidget(self.theme_text)

        # ? Панель письма =====================================================
        self.row_letter = QHBoxLayout()
        self.row_letter.setContentsMargins(0, 0, 0, 0)
        self.row_letter.setSpacing(5)
        self.row_letter.setAlignment(Qt.AlignmentFlag.AlignBottom)

        self.letter_b = QPushButton(self)
        self.letter_b.setToolTip(lang[conf['lang']]['letter_b'])
        self.letter_b.setIcon(QIcon(pjoin_r(FILE_LETTER_ICON)))
        self.letter_b.setFixedSize(QSize(25, 25))
        self.row_letter.addWidget(self.letter_b, 1, Qt.AlignmentFlag.AlignTop)

        self.letter_text = QPlainTextEdit(self)
        self.letter_text.setMinimumSize(QSize(100, 30))
        self.letter_text.setToolTip(lang[conf['lang']]['letter_text'])
        self.row_letter.addWidget(self.letter_text, 0)

        # ! Главная разметка ==================================================
        self.main_l = QVBoxLayout()
        self.main_l.setContentsMargins(3, 3, 3, 3)
        self.main_l.setSpacing(5)

        self.main_l.addLayout(self.row_top, 0)
        self.main_l.addLayout(self.row_list, 0)
        self.main_l.addLayout(self.row_theme, 0)
        self.main_l.addLayout(self.row_letter, 1)
        self.main_l.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.setLayout(self.main_l)

