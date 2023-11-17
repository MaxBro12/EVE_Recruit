from PySide6.QtWidgets import (
    QMainWindow,
    QStackedWidget,
    QWidget,
    QHBoxLayout,
    QPushButton,
    QVBoxLayout,
    QComboBox,
    QLineEdit,
    QTextEdit,
    QPlainTextEdit,
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize, Slot, Signal, QPoint
from datetime import date

from .warning_app import Warning_App
from .mainapp import FullSizedApp, SmallSizedApp 

from core import (
    create_log_file,
    clone_list,
    clone_theme,
    clone_letter,
    pjoin,
    pjoin_r,
    get_files,
    load_file,
    load_file_bytes,
    read_toml,
    write_to_toml,
    get_theme,
    get_letter_way,
    change_letter,
    change_theme,
    get_profiles_names,
    create_prof,
    delete_profile,
    write_to_cb,
)

from settings import (
    FILE_SETTINGS,

    DIR_PROFILE,
    FILE_CSV,

    SMALL_WIDTH,
    SMALL_HEIGHT,

    FULL_MIN_WIDTH,
    FULL_MIN_HEIGHT,

    FILE_APP_ICON,
    FILE_ADD_ICON,
    FILE_HIDE_ICON,
    FILE_EXIT_ICON,
    FILE_LIST_ICON,
    FILE_THEME_ICON,
    FILE_LETTER_ICON,
    FILE_ALWAYS_ON_ICON,
    FILE_SQEEZE_ICON,
    FILE_DELETE_B_ICON,
    FILE_STYLESHEET,
)

from lang import lang


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

        if config != date.today():
            self.conf['last_day'] = date.today()
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


class MyApp(QStackedWidget):
    save_app_signal = Signal(dict)

    close_app_signal = Signal()
    hide_app_signal = Signal()
    alwayson_app_signal = Signal()
    sqeeze_app_signal = Signal()

    def __init__(self, config: dict, profiles: list, parent):
        super().__init__(parent=parent)
        self.config = config
        self.profiles = profiles

        # ? Размеры
        self.resize(self.config['width'], self.config['height'])

        # * Добавляем стаки приложения
        self.full = FullSizedApp(self, config)
        self.small = SmallSizedApp(self, config)
        self.addWidget(self.full)
        self.addWidget(self.small)

        # ! Подключаем кнопки FULL
        if config['use_self_window']:
            self.full.exit_b.clicked.connect(self.exit_app)
            self.full.hide_b.clicked.connect(self.hide_app)

        self.full.sqeeze_b.clicked.connect(self.sqeeze_app)
        self.full.always_on_b.clicked.connect(self.always_on_app)

        self.full.list_b.clicked.connect(self.clone_list_b)
        self.full.list_text.editingFinished.connect(self.list_change)

        self.full.theme_b.clicked.connect(self.clone_theme_b)
        self.full.letter_b.clicked.connect(self.clone_letter_b)

        self.full.theme_text.editingFinished.connect(self.theme_change)
        self.full.letter_text.textChanged.connect(self.letter_change)

        self.full.profile_ch.currentIndexChanged.connect(self.change_profile)

        self.full.add_profile.clicked.connect(self.add_profile)
        self.full.delete_b.clicked.connect(self.delete_profile)

        # ! Подключаем кнопки SMALL
        if config['use_self_window']:
            self.small.exit_b.clicked.connect(self.exit_app)
            self.small.hide_b.clicked.connect(self.hide_app)

        self.small.sqeeze_b.clicked.connect(self.sqeeze_app)
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
    def sqeeze_app(self):
        self.sqeeze_app_signal.emit()

    @Slot()
    def save_config(self, config: dict):
        self.save_app_signal.emit(config)

    @Slot()
    def clone_list_b(self):
        # self.config['todays_letters'] += 1
        # self.save_config(self.config)
        # if self.config['todays_letters'] >= self.config['max_letters_warning']:
        #     warn = Warning_App(lang[self.config['lang']]['max_letter_warning'])
        #     warn.show()

        self.full.list_text.setText(clone_list(
            pjoin(DIR_PROFILE, self.config['lastprofile'], FILE_CSV)
        ))

    @Slot()
    def clone_theme_b(self):
        self.full.theme_text.setText(
            clone_theme(get_theme(self.config['lastprofile']))
        )

    @Slot()
    def clone_letter_b(self):
        self.full.letter_text.setPlainText(
            clone_letter(get_letter_way(self.config['lastprofile']))
        )

    @staticmethod
    def get_txt_file(*paths) -> str:
        return pjoin(
            *paths,
            list(filter(
                lambda x: x.split('.')[1] == 'txt', get_files(pjoin(*paths))
            ))[0]
        )

    def theme_change(self):
        change_theme(
            self.config['lastprofile'], self.full.theme_text.text() + '.txt'
        )

    def letter_change(self):
        change_letter(
            self.config['lastprofile'], self.full.letter_text.toPlainText()
        )

    def list_change(self):
        write_to_cb(self.full.list_text.text())

    def update_full_profile_ch(self):
        for prof in get_profiles_names():
            itms = [
                self.full.profile_ch.itemText(i) for i in range(
                    self.full.profile_ch.count()
                )
            ]
            if prof not in itms:
                self.full.profile_ch.addItem(prof)
        self.full.profile_ch.setCurrentText(self.config['lastprofile'])
        '''
        itms = [
            self.full.profile_ch.itemText(i) for i in range(
                self.full.profile_ch.count()
            )
        ]
        for p in get_profiles_names():
            if p != self.full.profile_ch.currentText() and p not in itms:
                self.full.profile_ch.addItem(p)'''

    def change_profile(self):
        self.config['lastprofile'] = self.full.profile_ch.currentText()
        self.save_config(self.config)
        self.update_app_data()

    def add_profile(self):
        if self.full.new_profile.text() != '':
            create_prof(self.full.new_profile.text())
            self.update_full_profile_ch()
        else:
            create_log_file('Try to create empty profile', levelname='info')

    def delete_profile(self):
        if delete_profile(self.full.profile_ch.currentText()):
            index = self.full.profile_ch.findText(
                self.full.profile_ch.currentText()
            )
            self.full.profile_ch.removeItem(index)
            self.update_full_profile_ch()
            self.update_app_data()

    def update_app_data(self):
        self.full.theme_text.setText(
            get_theme(self.config['lastprofile']).split('.')[0]
        )
        self.full.letter_text.setPlainText(
            load_file_bytes(get_letter_way(self.config['lastprofile']))
        )

