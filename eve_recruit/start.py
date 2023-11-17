from core import (
    create_prof,
    create_log_file,

    load_file,
    save_file,

    create_folder,

    get_files,

    read_toml,
    write_to_toml,
    toml_type_check,

    wayfinder,
    ProfileCreationError,
)

from settings import (
    MAX_LOG_LEN,

    FILE_SETTINGS,
    FILE_SETTINGS_IN,

    FILE_LOGGER,

    DIR_PROFILE,
    DEFAUT_PROFILE,
)


def main_check() -> tuple:
    conf = check_settings()

    if not wayfinder(DIR_PROFILE):
        create_folder(DIR_PROFILE)
        create_log_file('PROFILE FOLDER CREATED', levelname='info')
        if not create_prof(DEFAUT_PROFILE):
            raise ProfileCreationError
    profiles = get_files(DIR_PROFILE)

    log_file_check()

    return profiles, conf


def create_settings():
    defaut = FILE_SETTINGS_IN
    defaut['lastprofile'] = DEFAUT_PROFILE
    write_to_toml(defaut, FILE_SETTINGS)


def check_settings() -> dict:
    if not wayfinder(FILE_SETTINGS):
        create_settings()
    else:
        conf = read_toml(FILE_SETTINGS)
        if not toml_type_check(FILE_SETTINGS_IN, conf):
            print('WTF')
            create_settings()
    return read_toml(FILE_SETTINGS)


def log_file_check():
    if wayfinder(FILE_LOGGER):
        lens = load_file(FILE_LOGGER).split('\n')
        if len(lens) > MAX_LOG_LEN:
            lens = lens[len(lens) - MAX_LOG_LEN::]
            save_file(FILE_LOGGER, '\n'.join(lens))
            create_log_file('Log file resave', levelname='debug')

