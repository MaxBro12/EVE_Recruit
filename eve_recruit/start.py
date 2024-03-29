from core import (
    create_prof,
    create_log_file,

    load_file,
    load_file_bytes,
    save_file,

    create_file,
    create_folder,

    get_files,

    read,
    write,

    wayfinder,
    pjoin,
    ProfileNotLoaded,
    ProfileCreationError,
)

from settings import (
    max_log_len,

    file_settings,
    file_settings_in,

    file_logger,

    dir_profile,
    file_csv,
    defaut_profile,
    defaut_letter,
)


def main_check() -> tuple:
    if not wayfinder(file_settings):
        defaut = file_settings_in
        defaut['lastprofile'] = defaut_profile
        write(defaut, file_settings)

    conf = read(file_settings)

    if not wayfinder(dir_profile):
        create_folder(dir_profile)
        create_log_file('PROFILE FOLDER CREATED', levelname='info')
        if not create_prof(defaut_profile):
            raise ProfileCreationError
    profiles = get_files(dir_profile)

    log_file_check()

    return profiles, conf


def log_file_check():
    if wayfinder(file_logger):
        lens = load_file(file_logger).split('\n')
        if len(lens) > max_log_len:
            lens = lens[len(lens) - max_log_len::]
            save_file(file_logger, '\n'.join(lens))
            create_log_file('Log file resave', levelname='debug')
