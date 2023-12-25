from PyQt5.QtWidgets import QStackedWidget, QMainWindow

from account.model.datamodel import DataModel, CustomWidget
from account.view.admin.homepage import AdminHomePage
from account.view.auth.login import LoginWindow, ForgotPasswordStep
from account.view.auth.signup import SignUpForm
from account.view.user.homepage import UserHomePage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.data_model = DataModel()

        self.stack_widget = QStackedWidget(self)
        widget1 = CustomWidget(self.data_model)
        widget2 = CustomWidget(self.data_model)

        self.setCentralWidget(self.stack_widget)

        # Example: Changing data and switching widgets
        self.data_model.set_data("Initial Data")
        self.stack_widget.setCurrentIndex(1)  # Switch to the second widget

    # def center(self):
    #     screen = QDesktopWidget().screenGeometry()
    #
    #     x = (screen.width() - self.width()) // 2
    #     y = (screen.height() - self.height()) // 2
    #     self.move(x, y)
    #
    def init_windows(self):
        self.stacked_widget = QStackedWidget(self)
        self.login_window = LoginWindow()
        # Step 0: Login
        self.stacked_widget.addWidget(self.login_window)

        # Step 1: Forgot Password
        self.forgot_password_step = ForgotPasswordStep(self)
        self.stacked_widget.addWidget(self.forgot_password_step)

        # step 2: Sign up
        self.signup = SignUpForm(self)
        self.stacked_widget.addWidget(self.signup)

        # step 3: user home page
        self.user_home_page = UserHomePage(self)
        self.stacked_widget.addWidget(self.user_home_page)

        # step 4: admin home page
        self.admin_home_page = AdminHomePage(self)
        self.stacked_widget.addWidget(self.admin_home_page)
