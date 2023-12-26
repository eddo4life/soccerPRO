from PyQt5.QtWidgets import QStackedWidget, QMainWindow, QDesktopWidget

from account.view.admin.homepage import AdminHomePage
from account.view.auth.forgotpassword import ForgotPassword
from account.view.auth.login import LoginWindow
from account.view.auth.signup import SignUpForm
from account.view.user.homepage import UserHomePage
from account.view.user.profile.userprofile import UserProfile


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.__stacked_widget)
        self.init_windows()
        self.setGeometry(0, 0, 1000, 800)
        self.center_on_screen()

    def center_on_screen(self):
        # Get the geometry of the screen
        screen_geometry = QDesktopWidget().screenGeometry()

        # Calculate the center point of the screen
        center_point = screen_geometry.center()

        # Move the main window to the center of the screen
        self.move(center_point - self.rect().center())

    def init_windows(self):
        # Step 0: Login
        self.__stacked_widget.addWidget(LoginWindow(self))

        # Step 1: Forgot Password
        self.__stacked_widget.addWidget(ForgotPassword(self))

        # Step 2: Sign up
        self.__stacked_widget.addWidget(SignUpForm(self))

        # Step 3: User home page
        self.__stacked_widget.addWidget(UserHomePage(self))

        # Step 4: Admin home page
        self.__stacked_widget.addWidget(AdminHomePage(self))

    def login(self, telephone, password):
        UserProfile.init_credentials(telephone, password)
        self.revalidate(3, UserHomePage(self))

        self.change_step(3)

    def initialize(self):
        self.change_step(0)

    def change_step(self, index):
        self.__stacked_widget.setCurrentIndex(index)

    def revalidate(self, index, new_widget):
        self.__stacked_widget.insertWidget(index, new_widget)
        # Remove the old widget
        old_widget = self.__stacked_widget.widget(index + 1)
        self.__stacked_widget.removeWidget(old_widget)
        old_widget.deleteLater()
