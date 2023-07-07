from core import (
    create_prof,
    create_log_file,

    create_file,
    create_folder,

    get_files,

    read,
    write,

    wayfinder,
    pjoin
)

from settings import (
    file_settings,
    file_settings_in,

    dir_profile,
    file_csv,
    defaut_profile,
    defaut_letter,
)


def main_check() -> tuple:
    if not wayfinder(file_settings):
        write(file_settings_in, file_settings)
    
    conf = read(file_settings)

    if not wayfinder(dir_profile):
        create_folder(dir_profile)
        create_log_file('PROFILE FOLDER CREATED', levelname='info')
        if not create_prof(defaut_profile):
            pass # TODO: Сделать окно ошибки
    profiles = get_files(dir_profile)

    return profiles, conf
