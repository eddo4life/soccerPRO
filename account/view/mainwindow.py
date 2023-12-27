from PyQt5.QtWidgets import QStackedWidget, QMainWindow, QDesktopWidget, QWidget

from account.view.admin.homepage import AdminHomePage
from account.view.auth.forgotpassword import ForgotPassword
from account.view.auth.login import LoginWindow
from account.view.auth.signup import SignUpForm
from account.view.user.homepage import UserHomePage
from account.view.user.profile.userprofile import UserProfile
from labs.lab import Lab


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the stacked widget as the central widget
        self.__stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.__stacked_widget)

        # Initialize the main window
        self.init_windows()
        self.setGeometry(0, 0, 1000, 800)
        self.center_on_screen()
        self.setWindowIcon(Lab.get_icon('soccer.png'))

        # Set the initial title
        self.set_title('Login')

    def center_on_screen(self):
        # Center the main window on the screen
        screen_geometry = QDesktopWidget().screenGeometry()
        center_point = screen_geometry.center()
        self.move(center_point - self.rect().center())

    def init_windows(self):
        # Initialize and add different windows to the stacked widget
        self.__stacked_widget.addWidget(LoginWindow(self))
        self.__stacked_widget.addWidget(ForgotPassword(self))
        self.__stacked_widget.addWidget(SignUpForm(self))
        self.__stacked_widget.addWidget(QWidget())  # Placeholder for User home page
        self.__stacked_widget.addWidget(AdminHomePage(self))

    def login(self, telephone, password):
        # Log in with provided credentials
        UserProfile.init_credentials(telephone, password)
        self.revalidate(3, UserHomePage(self))
        self.change_step(3)

    def set_title(self, title):
        # Set the title of the main window
        self.setWindowTitle(title)

    def initialize(self):
        # Initialize the main window with the default title and login step
        self.set_title('Login')
        self.change_step(0)

    def change_step(self, index):
        if index == 0:
            # Revalidate the admin data
            self.revalidate(4, AdminHomePage(self))
        # Change the displayed step in the stacked widget
        self.__stacked_widget.setCurrentIndex(index)

    def revalidate(self, index, new_widget):
        # Replace a widget at the specified index in the stacked widget
        self.__stacked_widget.insertWidget(index, new_widget)
        # Remove the old widget
        old_widget = self.__stacked_widget.widget(index + 1)
        self.__stacked_widget.removeWidget(old_widget)
        old_widget.deleteLater()
