from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QFormLayout, QVBoxLayout, \
    QGridLayout, QStackedWidget

from account.view.auth.signup import SignUpForm
from account.view.user.homepage import UserHomePage


class ForgotPasswordStep(QWidget):
    def __init__(self, login_window):
        super().__init__()


        # Reference to the LoginWindow
        self.login_window = login_window

        # Set up UI elements for the Forgot Password step
        self.init_ui()

    def init_ui(self):
        # Create widgets
        self.nif_cin_label = QLabel('NIF/CIN:')
        self.nif_cin_entry = QLineEdit()

        self.telephone_label = QLabel('Telephone:')
        self.telephone_entry = QLineEdit()

        self.new_password_label = QLabel('New Password:')
        self.new_password_entry = QLineEdit()
        self.new_password_entry.setEchoMode(QLineEdit.Password)

        self.confirm_password_label = QLabel('Confirm Password:')
        self.confirm_password_entry = QLineEdit()
        self.confirm_password_entry.setEchoMode(QLineEdit.Password)

        self.reset_password_button = QPushButton('Reset Password')
        self.back_button = QPushButton('Back')
        self.back_button.clicked.connect(self.show_previous_login_step)

        # Set up form layout for the Forgot Password step
        form_layout = QFormLayout()
        form_layout.addRow(self.nif_cin_label, self.nif_cin_entry)
        form_layout.addRow(self.telephone_label, self.telephone_entry)
        form_layout.addRow(self.new_password_label, self.new_password_entry)
        form_layout.addRow(self.confirm_password_label, self.confirm_password_entry)
        form_layout.addRow(self.reset_password_button)
        form_layout.addRow(self.back_button)  # Add the back button

        # Set the layout for the Forgot Password step
        self.setLayout(form_layout)

    def show_previous_login_step(self):
        # Switch to the previous login step in the LoginWindow
        self.login_window.stacked_widget.setCurrentIndex(0)


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set up UI elements for the Login window
        self.init_ui()

    def init_ui(self):
        # Create widgets
        self.id_label = QLabel('ID:')
        self.id_entry = QLineEdit()

        self.password_label = QLabel('Password:')
        self.password_entry = QLineEdit()
        self.password_entry.setEchoMode(QLineEdit.Password)  # To hide the password input

        self.forgot_password_label = QLabel('<a href="#">Forgot Password?</a>')
        self.forgot_password_label.linkActivated.connect(self.show_forgot_password_step)

        self.login_button = QPushButton('Login')
        self.login_button.clicked.connect(self.login)
        self.signup_button = QPushButton('Sign Up')
        self.signup_button.clicked.connect(self.signup)

        # Set up form layout for the Login window
        form_layout = QFormLayout()
        form_layout.addRow(self.id_label, self.id_entry)
        form_layout.addRow(self.password_label, self.password_entry)
        form_layout.addRow(self.forgot_password_label)
        form_layout.addRow(self.login_button)
        form_layout.addRow(self.signup_button)


        # Set up stacked widget for login steps
        self.stacked_widget = QStackedWidget(self)

        # Step 0: Login
        login_step = QWidget(self)
        login_step.setLayout(form_layout)  # Set the layout for login_step
        self.stacked_widget.addWidget(login_step)

        # Step 1: Forgot Password
        forgot_password_step = ForgotPasswordStep(self)
        self.stacked_widget.addWidget(forgot_password_step)

        # step 2: Sign up
        signup = SignUpForm(self)
        self.stacked_widget.addWidget(signup)

        # step 3: log in
        user_home_page = UserHomePage(self)
        self.stacked_widget.addWidget(user_home_page)

        # Set up main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stacked_widget)  # Add the stacked widget to the main layout
        main_layout.setAlignment(self.stacked_widget,Qt.AlignBaseline)


        # Set the layout for the main window
        self.setLayout(main_layout)

        # Set window properties
        self.setWindowTitle('Login Window')
        self.setGeometry(300, 300, 800, 500)

    def show_forgot_password_step(self):
        # Switch to the Forgot Password step
        self.stacked_widget.setCurrentIndex(1)

    def signup(self):
        # Switch to the Sign-up step
        self.stacked_widget.setCurrentIndex(2)

    def login(self):
        # Switch to the user's home page
        self.stacked_widget.setCurrentIndex(3)

    def initialize(self):
        self.stacked_widget.setCurrentIndex(0)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
