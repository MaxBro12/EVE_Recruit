from .filemanage import (
    create_file,
    create_folder,
    save_file,
    pjoin,
    rename_file,
    get_files,
    remove_dir_tree,
)
from .debug import (
    create_log_file,
)

from settings import (
    dir_profile,
    file_csv,
)


def create_prof(name: str) -> bool:
    way = pjoin(dir_profile, name)
    print(way)
    if create_folder(way):
        if create_file(pjoin(way, file_csv)):
            if create_file(pjoin(way, 'THEME.txt')):
                create_log_file(f'PROFILE {name} CREATED', levelname='info')
                return True
    create_log_file(f'CANT CREATE PROFILE {name}', levelname='error')
    return False


def get_theme(name_profile: str) -> str:
    return list(filter(
        lambda x: x.split('.')[1] == 'txt', get_files(pjoin(
            dir_profile, name_profile
        ))
    ))[0]


def get_letter_way(name_profile: str) -> str:
    return pjoin(dir_profile, name_profile, get_theme(name_profile))


def change_theme(name_profile: str, new_theme_name: str) -> bool:
    create_log_file(
        f'Theme {pjoin(dir_profile, name_profile, get_theme(name_profile))}' +
        f' was changed to {pjoin(dir_profile, name_profile, new_theme_name)}',
        levelname='info'
    )
    return True if rename_file(
        pjoin(dir_profile, name_profile, get_theme(name_profile)),
        pjoin(dir_profile, name_profile, new_theme_name)
    ) else False


def change_letter(name_profile: str, inner: str) -> bool:
    create_log_file(
        f'Letter {pjoin(dir_profile, name_profile, get_theme(name_profile))}' +
        ' was changed',
        levelname='info'
    )
    return True if save_file(
        pjoin(dir_profile, name_profile, get_theme(name_profile)), inner
    ) else False


def delete_profile(name_profile: str) -> bool:
    create_log_file(
        f'Profile {pjoin(dir_profile, name_profile)} was deleted',
        levelname='info'
    )
    return True if remove_dir_tree(
        pjoin(dir_profile, name_profile)
    ) else False


def get_profiles_names() -> list:
    return get_files(dir_profile)


if __name__ == '__main__':
    print(get_theme('defaut'))
