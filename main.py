import sys

from PyQt5.QtWidgets import QApplication, QGridLayout, QWidget

from account.model.matchmanagementmodel import MatchManagementModel
from account.view.auth.login import LoginWindow
from account.view.user.profile.userprofile import UserProfile


class Init(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MainView")
        self.setMinimumSize(600, 300)
        grid = QGridLayout()
        grid.addWidget(UserProfile(), 0, 0)

        self.setLayout(grid)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # init = Init()
    # init.show()
    login_window = LoginWindow()
    login_window.show()

    sys.exit(app.exec_())


