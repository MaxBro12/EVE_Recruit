from pyperclip import (
    copy,
    paste,
)


def write_to_cb(data: str) -> str:
    copy(data)
    paste()
    return data
