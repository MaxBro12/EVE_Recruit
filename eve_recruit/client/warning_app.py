from PySide6.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout
from PySide6.QtCore import QSize, Qt


class Warning_App(QDialog):
    def __init__(self, msg) -> None:
        super().__init__()

        # ! Разметка
        self.row = QVBoxLayout()
        self.row.setContentsMargins(5, 5, 5, 5)
        self.row.setSpacing(5)
        self.row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.row)

        self.text = QLabel()
        self.text.setText(msg)
        self.row.addWidget(self.text)

        self.button = QPushButton()
        self.button.setFixedSize(QSize(100, 25))
        self.button.setText('OK')
        self.button.clicked.connect(self.close())
        self.row.addWidget(self.button)
