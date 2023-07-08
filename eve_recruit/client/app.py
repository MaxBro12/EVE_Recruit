from typing import Optional
from PySide6.QtWidgets import QMainWindow, QStackedWidget, QWidget
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt

from settings import (
    file_app_icon,
    file_hide_icon,
    file_exit_icon,
)


class MyAppMain(QMainWindow):
    def __init__(self, config: dict, profiles: list) -> None:
        super().__init__()
        self.setCentralWidget(MyApp(config, profiles, self))
        # ? Статус бар
        self.status_bar = self.statusBar()
        # ? Топ панель
        self.setWindowIcon(QIcon(file_app_icon))
        self.setWindowTitle('EVE REQUIT')
        self.setWindowFlags(Qt.FramelessWindowHint)


class MyApp(QStackedWidget):
    def __init__(self, config: dict, profiles: list, parent):
        super().__init__(parent=parent)
        self.config = config
        self.profiles = profiles

        # ? Размеры
        self.resize(self.config['width'], self.config['height'])
        full = FullSizedApp(config, profiles, self)
        small = SmallSizedApp(config, profiles, self)
        self.addWidget(full)
        self.addWidget(small)


class FullSizedApp(QWidget):
    def __init__(self, config, profiles, parent) -> None:
        super().__init__(parent=parent)


class SmallSizedApp(QWidget):
    def __init__(self, config, profiles, parent) -> None:
        super().__init__(parent=parent)

