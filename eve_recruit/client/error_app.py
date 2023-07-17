from PySide6.QtWidgets import QDialog, QLabel, QTextEdit, QVBoxLayout
from PySide6.QtCore import QSize

from settings import error_found


class Error_App(QDialog):
    def __init__(self, msg: str):
        super().__init__()
        # ? Окно
        self.setWindowTitle('ERROR')
        self.setBaseSize(QSize(200, 150))

        # ? Разметка
        self.col = QVBoxLayout()
        self.col.setContentsMargins(5, 5, 5, 5)
        self.col.setSpacing(5)
        self.setLayout(self.col)

        # ? Виджеты
        self.error_found = QLabel()
        self.error_found.setText(error_found)
        self.col.addWidget(self.error_found)

        self.error_log = QTextEdit()
        self.error_log.setText(str(msg))
        self.col.addWidget(self.error_log)
