from os.path import exists, join
from os import mkdir

from mybase import (
    create_csv,
)

from settings import (
    dir_profile,
)


def main_cheack():
    if not exists(dir_profile):
        mkdir(dir_profile)
    if not exists(csv_file):
        create_csv(csv_file, csv_data)


def create_prof(name: str):
    create_csv(name, csv_data)
