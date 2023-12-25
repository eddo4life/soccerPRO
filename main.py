import sys

from PyQt5.QtWidgets import QApplication

from account.view.auth.login import LoginWindow
from account.view.mainwindow import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # init = Init()
    # init.show()
    login_window = LoginWindow()
    login_window.show()
    # main_window = MainWindow()
    # main_window.show()
    sys.exit(app.exec_())
