from PySide6.QtWidgets import (
    QMainWindow,
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize, QPoint
from datetime import date

from .warning_app import Warning_App
from .mainapp import MyApp 

from core import (
    create_log_file,
    pjoin_r,
    write_to_toml,
)

from settings import (
    FILE_SETTINGS,

    SMALL_WIDTH,
    SMALL_HEIGHT,

    FULL_MIN_WIDTH,
    FULL_MIN_HEIGHT,

    FILE_APP_ICON,
    FILE_STYLESHEET,
)


class MyAppMain(QMainWindow):
    def __init__(self, config: dict, profiles: list) -> None:
        super().__init__()
        self.app = MyApp(config, profiles, self)
        self.setCentralWidget(self.app)

        # * Темы
        with open(pjoin_r(FILE_STYLESHEET), 'r') as f:
            self.setStyleSheet(f.read())
        self.setWindowOpacity(config['opacity'])

        # ? Конфиг
        self.conf = config

        self.warning_app = None
        self.error_app = None

        if config != date.today():
            self.conf['last_day'] = str(date.today())
            self.conf['todays_letters'] = 0
            self.save_config(self.conf)

        self.oldPosition = QPoint()

        # ? Статус бар
        # self.status_bar = self.statusBar()

        # ? Топ панель
        self.setWindowIcon(QIcon(pjoin_r(FILE_APP_ICON)))
        self.setWindowTitle('EVE RECRUIT')
        self.setWindowFlag(Qt.FramelessWindowHint, self.conf['use_self_window'])
        self.setWindowFlag(Qt.WindowStaysOnTopHint, self.conf['alwayson'])

        # ? Соединияем кнопки
        self.app.save_app_signal.connect(self.save_config)
        self.app.close_app_signal.connect(self.close_app)
        self.app.hide_app_signal.connect(self.hide_app)
        self.app.alwayson_app_signal.connect(self.always_on_app)
        self.app.sqeeze_app_signal.connect(self.sqeeze_app)

        # ! Изначально запускается режим?
        self.app.update_full_profile_ch()
        self.change_to_full()

        create_log_file(
            f'Application launched successfully!\nProfiles: {len(profiles)}' +
            f'\nLast profile: {config["lastprofile"]}' +
            f'\nUse Self Window: {config["use_self_window"]}',
            levelname='info'
        )

    def sqeeze_app(self):
        if self.app.currentIndex() == 1:
            # ! Переключаемся на полноразмерную прогу
            create_log_file('Change to full-size app', levelname='info')
            self.change_to_full()
        else:
            # ! Переключаемся на малоразмерную прогу
            create_log_file('Change to small app', levelname='info')
            self.change_to_small()

    def mousePressEvent(self, event):
        if self.conf['use_self_window']:
            self.oldPosition = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.conf['use_self_window']:
            self.move(
                self.pos() +
                event.globalPosition().toPoint() -
                self.oldPosition
            )
            self.oldPosition = event.globalPosition().toPoint()
            event.accept()

    def close_app(self):
        self.close()

    def hide_app(self):
        self.showMinimized()

    def always_on_app(self):
        self.conf['alwayson'] = not self.conf['alwayson']
        create_log_file(
            f'Always on is now {self.conf["alwayson"]}', levelname='info'
        )
        self.save_config(self.conf)

    def change_to_small(self):
        self.app.setCurrentIndex(1)
        self.setMinimumSize(QSize(SMALL_WIDTH, SMALL_HEIGHT))
        self.resize(QSize(SMALL_WIDTH, SMALL_HEIGHT))

    def change_to_full(self):
        self.app.setCurrentIndex(0)
        self.resize(QSize(FULL_MIN_WIDTH, FULL_MIN_HEIGHT))

    def save_config(self, config):
        self.conf = config
        write_to_toml(config, FILE_SETTINGS)
        create_log_file('Config was saved', levelname='info')

