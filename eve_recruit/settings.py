from typing import Final


# ! Важное
MAX_LOG_LEN: Final = 500

# ! Настройки пилотов
PILOT_PATTERN: Final = r'[\w|-]*[ |.|\w][\w|-]*'

# ! Папки, файлы
DIR_PROFILE: Final = 'profile'
FILE_CSV: Final = 'data.csv'
FILE_SETTINGS: Final = 'settings.toml'
FILE_LOGGER: Final = 'logger.log'
FILE_SETTINGS_IN: Final = {
    'pos_x': 550,
    'pos_y': 350,
    'width': 300,
    'height': 200,
    'opacity': 1,
    'lastprofile': '',
    'lang': 'ru',
    'resizeable': True,
    'alwayson': True,
    'use_self_window': False,
    'letters_warning': True,
    'last_day': '',
    'todays_letters': 0,
    'max_letters_warning': 15,
}

DEFAUT_LETTER: Final = 'defaut.txt'
DEFAUT_PROFILE: Final = 'defaut'

# ! Клиент
FULL_MIN_WIDTH: Final = 400
FULL_MIN_HEIGHT: Final = 600

SMALL_WIDTH: Final = 215
SMALL_HEIGHT: Final = 35


ERROR_FOUND: Final = 'Found error! Please link logger.log to developer\nError log:'


FILE_HIDE_ICON: Final = 'icons/hide_icon.svg'
FILE_EXIT_ICON: Final = 'icons/exit_icon.svg'

FILE_APP_ICON: Final = 'icons/app_icon.svg'
FILE_LIST_ICON: Final = 'icons/list_icon.svg'
FILE_ADD_ICON: Final = 'icons/add_icon.svg'
FILE_THEME_ICON: Final = 'icons/theme_icon.svg'
FILE_LETTER_ICON: Final = 'icons/letter_icon.svg'
FILE_SQEEZE_ICON: Final = 'icons/sqeeze_icon.svg'
FILE_ALWAYS_ON_ICON: Final = 'icons/alwayson_icon.svg'
FILE_DELETE_B_ICON: Final = 'icons/delete_icon.svg'

FILE_STYLESHEET: Final = 'theme.css'

