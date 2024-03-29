from .filemanage import (
    create_file,
    create_folder,
    save_file,
    pjoin,
    rename_file,
    get_files,
    remove_dir_tree,
)
from .mybase import create_csv
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
        create_csv(pjoin(way, file_csv))
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
    way1 = pjoin(dir_profile, name_profile, get_theme(name_profile))
    way2 = pjoin(dir_profile, name_profile, new_theme_name)
    if rename_file(way1, way2):
        create_log_file(
            f'Theme {way1} was changed to {way2}', levelname='info'
        )
        return True
    else:
        create_log_file(f'CANT change {way1} to {way2}', levelname='info')
        return False


def change_letter(name_profile: str, inner: str) -> bool:
    way = pjoin(dir_profile, name_profile, get_theme(name_profile))
    if save_file(way, inner):
        create_log_file(f'Letter {way} was changed', levelname='info')
        return True
    else:
        create_log_file(f'Error in {way} cannot be change', levelname='error')
        return False


def delete_profile(name_profile: str) -> bool:
    way = pjoin(dir_profile, name_profile)
    if remove_dir_tree(way):
        create_log_file(f'Profile {way} was deleted', levelname='info')
        return True
    else:
        create_log_file(f'CANT DELETE Profile {way}', levelname='error')
        return False


def get_profiles_names() -> list:
    return get_files(dir_profile)


if __name__ == '__main__':
    pass
