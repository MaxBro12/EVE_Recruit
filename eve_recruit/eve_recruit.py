from PySide6.QtWidgets import QApplication
from sys import exit

from core import create_log_file
from client import MyAppMain, Error_App
from start import main_check


def main():
    profiles, conf = main_check()
    app = QApplication([])
    widget = MyAppMain(conf, profiles)
    widget.show()
    exit(app.exec())


if __name__ == '__main__':
    try:
        main()
    except Exception as err:
        create_log_file(err, 'crit')

        if QApplication.instance() is None:
            app = QApplication([])
        widget = Error_App(err)
        widget.show()
        exit(QApplication.exec())
