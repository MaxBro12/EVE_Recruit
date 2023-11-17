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
        write(config, FILE_SETTINGS)
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

        self.add_profile = QPushButton(self)
        self.add_profile.setToolTip(lang[conf['lang']]['add_profile'])
        self.add_profile.setIcon(QIcon(pjoin_r(FILE_ADD_ICON)))
        self.add_profile.setFixedSize(QSize(25, 25))
        self.row_top.addWidget(self.add_profile, 0)

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

        if conf['use_self_window']:
            self.exit_b = QPushButton(self)
            self.exit_b.setToolTip(lang[conf['lang']]['exit_b'])
            self.exit_b.setIcon(QIcon(pjoin_r(FILE_EXIT_ICON)))
            self.exit_b.setFixedSize(QSize(25, 25))
            self.row.addWidget(self.exit_b)
