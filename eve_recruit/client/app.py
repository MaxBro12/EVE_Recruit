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
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize, Slot, Signal, QPoint

from core import (
    create_log_file,
    clone_list,
    clone_theme,
    clone_letter,
    pjoin,
    get_files,
    load_file,
    read,
    write,
    get_theme,
    get_letter_way,
    change_letter,
    change_theme,
    get_profiles_names,
    create_prof,
    delete_profile,
)

from settings import (
    file_settings,

    dir_profile,
    file_csv,

    small_width,
    small_height,

    full_min_width,
    full_min_height,

    file_app_icon,
    file_add_icon,
    file_hide_icon,
    file_exit_icon,
    file_list_icon,
    file_theme_icon,
    file_letter_icon,
    file_always_on_icon,
    file_sqeeze_icon,
)
from lang import lang


class MyAppMain(QMainWindow):
    def __init__(self, config: dict, profiles: list) -> None:
        super().__init__()
        self.app = MyApp(config, profiles, self)
        self.setCentralWidget(self.app)

        # ? Допы
        self.conf = config
        self.oldPosition = QPoint()

        # ? Статус бар
        # self.status_bar = self.statusBar()

        # ? Топ панель
        self.setWindowIcon(QIcon(file_app_icon))
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

        create_log_file('Application launched successfully', levelname='info')

    def sqeeze_app(self):
        if self.app.currentIndex() == 1:
            # ! Переключаемся на полноразмерную прогу
            self.change_to_full()
        else:
            # ! Переключаемся на малоразмерную прогу
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
        self.save_config()

    def change_to_small(self):
        self.app.setCurrentIndex(1)
        self.setMinimumSize(QSize(small_width, small_height))
        self.resize(QSize(small_width, small_height))

    def change_to_full(self):
        self.app.setCurrentIndex(0)
        self.resize(QSize(full_min_width, full_min_height))

    def save_config(self, config):
        self.conf = config
        write(config, file_settings)


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
        self.full.theme_b.clicked.connect(self.clone_theme_b)
        self.full.letter_b.clicked.connect(self.clone_letter_b)

        self.full.theme_text.editingFinished.connect(self.theme_change)
        self.full.letter_text.textChanged.connect(self.letter_change)

        self.full.profile_ch.currentIndexChanged.connect(self.change_profile)

        self.full.add_profile.clicked.connect(self.add_profile)

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
        self.full.list_text.setText(clone_list(
            pjoin(dir_profile, self.config['lastprofile'], file_csv)
        ))

    @Slot()
    def clone_theme_b(self):
        self.full.theme_text.setText(
            clone_theme(get_theme(self.config['lastprofile']))
        )

    @Slot()
    def clone_letter_b(self):
        self.full.letter_text.setText(
            clone_letter(get_letter_way(self.config['lastprofile']))
        )

    @staticmethod
    def get_txt_file(*paths) -> str:
        return pjoin(
            *paths,
            list(filter(lambda x: x.split('.')[1] == 'txt', get_files(pjoin(*paths))))[0]
        )

    def theme_change(self):
        change_theme(
            self.config['lastprofile'], self.full.theme_text.text() + '.txt'
        )

    def letter_change(self):
        change_letter(
            self.config['lastprofile'], self.full.letter_text.toPlainText()
        )

    def update_full_profile_ch(self):
        # self.full.profile_ch.setCurrentText(self.config['lastprofile'])
        itms = [
            self.full.profile_ch.itemText(i) for i in range(
                self.full.profile_ch.count()
            )
        ]
        for p in get_profiles_names():
            if p != self.full.profile_ch.currentText() and p not in itms:
                self.full.profile_ch.addItem(p)

    def change_profile(self):
        print("WTF")
        self.config['lastprofile'] = self.full.profile_ch.currentText()
        self.save_config(self.config)
        self.update_app_data()

    def add_profile(self):
        create_prof(self.full.new_profile.text())
        self.update_full_profile_ch()

    def update_app_data(self):
        self.full.theme_text.setText(
            get_theme(self.config['lastprofile']).split('.')[0]
        )
        self.full.letter_text.setText(
            load_file(get_letter_way(self.config['lastprofile']))
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

        self.row_top.addSpacing(10)

        self.new_profile = QLineEdit(self)
        self.new_profile.setToolTip(lang[conf['lang']]['new_profile'])
        self.new_profile.setMaximumHeight(25)
        self.row_top.addWidget(self.new_profile)

        self.add_profile = QPushButton(self)
        self.add_profile.setToolTip(lang[conf['lang']]['add_profile'])
        self.add_profile.setIcon(QIcon(file_add_icon))
        self.add_profile.setFixedSize(QSize(25, 25))
        self.row_top.addWidget(self.add_profile, 0)

        self.row_top.addSpacing(10)

        self.always_on_b = QPushButton(self)
        self.always_on_b.setToolTip(lang[conf['lang']]['always_on_b'])
        self.always_on_b.setIcon(QIcon(file_always_on_icon))
        self.always_on_b.setFixedSize(QSize(25, 25))
        self.row_top.addWidget(self.always_on_b, 0)

        self.sqeeze_b = QPushButton(self)
        self.sqeeze_b.setToolTip(lang[conf['lang']]['sqeeze_b'])
        self.sqeeze_b.setIcon(QIcon(file_sqeeze_icon))
        self.sqeeze_b.setFixedSize(QSize(25, 25))
        self.row_top.addWidget(self.sqeeze_b, 0)

        if conf['use_self_window']:
            self.hide_b = QPushButton(self)
            self.hide_b.setToolTip(lang[conf['lang']]['hide_b'])
            self.hide_b.setIcon(QIcon(file_hide_icon))
            self.hide_b.setFixedSize(QSize(25, 25))
            self.row_top.addWidget(self.hide_b, 0)

        if conf['use_self_window']:
            self.exit_b = QPushButton(self)
            self.exit_b.setToolTip(lang[conf['lang']]['exit_b'])
            self.exit_b.setIcon(QIcon(file_exit_icon))
            self.exit_b.setFixedSize(QSize(25, 25))
            self.row_top.addWidget(self.exit_b, 0)

        # ? Панель списка пилотов =============================================
        self.row_list = QHBoxLayout()
        self.row_list.setContentsMargins(0, 0, 0, 0)
        self.row_list.setSpacing(5)

        self.list_b = QPushButton(self)
        self.list_b.setToolTip(lang[conf['lang']]['list_b'])
        self.list_b.setIcon(QIcon(file_list_icon))
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
        self.theme_b.setIcon(QIcon(file_theme_icon))
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

        self.letter_b = QPushButton(self)
        self.letter_b.setToolTip(lang[conf['lang']]['letter_b'])
        self.letter_b.setIcon(QIcon(file_letter_icon))
        self.letter_b.setFixedWidth(25)
        self.row_letter.addWidget(self.letter_b)

        self.letter_text = QTextEdit(self)
        self.letter_text.setToolTip(lang[conf['lang']]['letter_text'])
        self.row_letter.addWidget(self.letter_text)

        # ! Главная разметка ==================================================
        self.main_l = QVBoxLayout()
        self.main_l.setContentsMargins(3, 3, 3, 3)
        self.main_l.setSpacing(5)

        self.main_l.addLayout(self.row_top)
        self.main_l.addLayout(self.row_list)
        self.main_l.addLayout(self.row_theme)
        self.main_l.addLayout(self.row_letter)

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
        self.list_b.setIcon(QIcon(file_list_icon))
        self.list_b.setFixedSize(QSize(25, 25))
        self.row.addWidget(self.list_b)

        self.theme_b = QPushButton(self)
        self.theme_b.setToolTip(lang[conf['lang']]['theme_b'])
        self.theme_b.setIcon(QIcon(file_theme_icon))
        self.theme_b.setFixedSize(QSize(25, 25))
        self.row.addWidget(self.theme_b)

        self.letter_b = QPushButton(self)
        self.letter_b.setToolTip(lang[conf['lang']]['letter_b'])
        self.letter_b.setIcon(QIcon(file_letter_icon))
        self.letter_b.setFixedSize(QSize(25, 25))
        self.row.addWidget(self.letter_b)

        self.always_on_b = QPushButton(self)
        self.always_on_b.setToolTip(lang[conf['lang']]['always_on_b'])
        self.always_on_b.setIcon(QIcon(file_always_on_icon))
        self.always_on_b.setFixedSize(QSize(25, 25))
        self.row.addWidget(self.always_on_b)

        self.sqeeze_b = QPushButton(self)
        self.sqeeze_b.setToolTip(lang[conf['lang']]['sqeeze_b'])
        self.sqeeze_b.setIcon(QIcon(file_sqeeze_icon))
        self.sqeeze_b.setFixedSize(QSize(25, 25))
        self.row.addWidget(self.sqeeze_b)

        if conf['use_self_window']:
            self.hide_b = QPushButton(self)
            self.hide_b.setToolTip(lang[conf['lang']]['hide_b'])
            self.hide_b.setIcon(QIcon(file_hide_icon))
            self.hide_b.setFixedSize(QSize(25, 25))
            self.row.addWidget(self.hide_b)

        if conf['use_self_window']:
            self.exit_b = QPushButton(self)
            self.exit_b.setToolTip(lang[conf['lang']]['exit_b'])
            self.exit_b.setIcon(QIcon(file_exit_icon))
            self.exit_b.setFixedSize(QSize(25, 25))
            self.row.addWidget(self.exit_b)
