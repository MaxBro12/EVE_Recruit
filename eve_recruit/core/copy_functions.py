from .clipb import get_from_cp, write_to_cb
from .mybase import Table
from .filemanage import load_file


def clone_list(self, name_csv: str):
    copy_list = ''
    table = Table(name_csv)
    pilots = get_from_cp()
    pilots = pilots.split('\n')

    if len(pilots) > 0:
        for pilot in pilots:
            if table.add(pilot):
                if copy_list != '':
                    copy_list += ', ' + pilot
                else:
                    copy_list = pilot
        write_to_cb(copy_list)


def clone_theme(self, name_txt: str):
    write_to_cb(name_txt.split('.')[0])


def clone_letter(self, name_txt: str):
    write_to_cb(load_file(name_txt))
