import sys

from PyQt5.QtWidgets import QApplication

from account.view.mainwindow import MainWindow


def start_application():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    start_application()
