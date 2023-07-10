from PySide6.QtWidgets import (
    QMainWindow, QStackedWidget, QWidget, QHBoxLayout, QPushButton,
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize, Slot, Signal

from core import create_log_file, clone_list, clone_theme, clone_letter, pjoin, get_files

from settings import (
    dir_profile,
    file_csv,

    file_app_icon,
    file_hide_icon,
    file_exit_icon,
    file_list_icon,
    file_theme_icon,
    file_letter_icon,
    file_always_on_icon,
)


class MyAppMain(QMainWindow):
    def __init__(self, config: dict, profiles: list) -> None:
        super().__init__()
        self.app = MyApp(config, profiles, self)
        self.setCentralWidget(self.app)

        # ? Допы
        self.always_on_bool = False

        # ? Статус бар
        self.status_bar = self.statusBar()

        # ? Топ панель
        self.setWindowIcon(QIcon(file_app_icon))
        self.setWindowTitle('EVE RECRUIT')
        self.setWindowFlags(Qt.FramelessWindowHint)

        # ? Соединияем кнопки
        self.app.close_app_signal.connect(self.close_app)
        self.app.hide_app_signal.connect(self.hide_app)
        self.app.alwayson_app_signal.connect(self.always_on)

        create_log_file('Application launched successfully', levelname='info')

    def resizeEvent(self, event):
            print("resize")
            self.resizeEvent(self, event)

    def close_app(self):
        self.close()

    def hide_app(self):
        self.showMinimized()

    def always_on(self):
        self.always_on_bool = not self.always_on_bool
        if self.always_on_bool:
            self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        else:
            self.setWindowFlag(Qt.WindowStaysOnTopHint, False)


class MyApp(QStackedWidget):
    close_app_signal = Signal()
    hide_app_signal = Signal()
    alwayson_app_signal = Signal()
    def __init__(self, config: dict, profiles: list, parent):
        super().__init__(parent=parent)
        self.config = config
        self.profiles = profiles

        # ? Размеры
        self.resize(self.config['width'], self.config['height'])

        self.full = FullSizedApp(config, profiles, self)
        self.small = SmallSizedApp(config, profiles, self)
        self.addWidget(self.full)
        self.addWidget(self.small)
        self.setCurrentIndex(1)

        # ! Подключаем кнопки SMALL
        self.small.exit_b.clicked.connect(self.exit_app)
        self.small.hide_b.clicked.connect(self.hide_app)
        self.small.always_on_b.clicked.connect(self.always_on_app)
        self.small.list_b.clicked.connect(self.clone_list_b)
        self.small.theme_b.clicked.connect(self.clone_theme_b)
        self.small.letter_b.clicked.connect(self.clone_letter_b)

    @Slot()
    def exit_app(self):
        self.close_app_signal.emit()

    @Slot()
    def hide_app(self):
        self.hide_app_signal.emit()

    @Slot()
    def always_on_app(self):
        self.alwayson_app_signal.emit()

    @Slot()
    def clone_list_b(self):
        clone_list(pjoin(dir_profile, self.config['lastprofile'], file_csv))

    @Slot()
    def clone_theme_b(self):
        clone_theme(pjoin(dir_profile, self.config['lastprofile']))

    @Slot()
    def clone_letter_b(self):
        clone_letter(pjoin(dir_profile, self.config['lastprofile']))

    @staticmethod
    def get_txt_file(*paths) -> str:
        return pjoin(
            *paths,
            list(filter(lambda x: x.split('.')[1] == 'txt', get_files(pjoin(*paths))))[0]
        )


class FullSizedApp(QWidget):
    def __init__(self, config, profiles, parent) -> None:
        super().__init__(parent=parent)


class SmallSizedApp(QWidget):
    def __init__(self, config, profiles, parent) -> None:
        super().__init__(parent=parent)
        self.row = QHBoxLayout()
        self.row.setContentsMargins(0, 0, 0, 0)
        self.row.setSpacing(0)
        self.setLayout(self.row)

        self.exit_b = QPushButton(self)
        self.exit_b.setIcon(QIcon(file_exit_icon))
        self.exit_b.setMinimumSize(QSize(15, 15))
        self.row.addWidget(self.exit_b)

        self.hide_b = QPushButton(self)
        self.hide_b.setIcon(QIcon(file_hide_icon))
        self.hide_b.setMinimumSize(QSize(15, 15))
        self.row.addWidget(self.hide_b)

        self.always_on_b = QPushButton(self)
        self.always_on_b.setIcon(QIcon(file_always_on_icon))
        self.always_on_b.setMinimumSize(QSize(15, 15))
        self.row.addWidget(self.always_on_b)

        self.list_b = QPushButton(self)
        self.list_b.setIcon(QIcon(file_list_icon))
        self.list_b.setMinimumSize(QSize(15, 15))
        self.row.addWidget(self.list_b)

        self.theme_b = QPushButton(self)
        self.theme_b.setIcon(QIcon(file_theme_icon))
        self.theme_b.setMinimumSize(QSize(15, 15))
        self.row.addWidget(self.theme_b)

        self.letter_b = QPushButton(self)
        self.letter_b.setIcon(QIcon(file_letter_icon))
        self.letter_b.setMinimumSize(QSize(15, 15))
        self.row.addWidget(self.letter_b)
