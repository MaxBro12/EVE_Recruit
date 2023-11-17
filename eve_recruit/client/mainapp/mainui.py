from PySide6.QtWidgets import (
    QStackedWidget,
)
from PySide6.QtCore import Slot, Signal
from .fullsized import FullSizedApp
from .smallsized import SmallSizedApp
from ..warning_app import Warning_App

from core import (
    create_log_file,
    clone_list,
    clone_theme,
    clone_letter,
    pjoin,
    get_files,
    load_file_bytes,
    get_theme,
    get_letter_way,
    change_letter,
    change_theme,
    get_profiles_names,
    create_prof,
    delete_profile,
    write_to_cb,
)

from lang import lang
from settings import (
    DIR_PROFILE,
    FILE_CSV,
)


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

        # Окна
        self.warning = None
        self.error = None

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

        self.full.new_profile.editingFinished.connect(self.add_profile)
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
        self.config['todays_letters'] += 1
        self.save_config(self.config)
        if self.config['todays_letters'] >= self.config['max_letters_warning']:
            if self.warning is None:
                self.warning = Warning_App(lang[self.config['lang']]['max_letter_warning'])
                self.warning.show()
            
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

