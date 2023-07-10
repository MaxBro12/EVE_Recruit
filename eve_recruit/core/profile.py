from .filemanage import (
    create_file,
    create_folder,
    pjoin
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
    if create_folder(way):
        if create_file(pjoin(way, file_csv)):
            if create_file(pjoin(way, 'THEME.txt')):
                create_log_file(f'PROFILE {name} CREATED', levelname='info')
                return True
    create_log_file(f'CANT CREATE PROFILE {name}', levelname='error')
    return False
