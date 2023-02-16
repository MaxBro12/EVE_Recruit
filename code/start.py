from os.path import exists, join
from os import mkdir

from settings import (
    profile_dir,

    csv_file,
    csv_data,
)
from mybase import (
    create_csv,
)


def main_cheack():
    if not exists(profile_dir):
        mkdir(profile_dir)
    if not exists(csv_file):
        create_csv(csv_file, csv_data)


def create_prof(name: str):
    create_csv(join(profile_dir, name), csv_data)
