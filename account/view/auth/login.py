from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QFormLayout, QVBoxLayout, \
    QStackedWidget, QDialog, QDesktopWidget, QGridLayout, QHBoxLayout

from account.view.admin.homepage import AdminHomePage
from account.view.auth.signup import SignUpForm
from account.view.user.homepage import UserHomePage


class AdminDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Login")
        self.setFixedSize(400, 250)

        self.id_label = QLabel("ID:")
        self.password_label = QLabel("Password:")
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red")

        self.id_edit = QLineEdit()
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)

        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.check_credentials)

        layout = QVBoxLayout(self)
        layout.addWidget(self.id_label)
        layout.addWidget(self.id_edit)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_edit)
        layout.addWidget(self.error_label)
        layout.addWidget(self.connect_button)

    def check_credentials(self):
        entered_id = self.id_edit.text()
        entered_password = self.password_edit.text()

        # Check if ID is 'admin' and password is '1234'
        if entered_id == 'admin' and entered_password == '1234':
            self.accept()  # Accept the dialog (credentials are correct)
        else:
            self.error_label.setText("Incorrect credentials")

        self.accept()  # to be removed later


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
        # Set window properties
        self.setWindowTitle('Login Window')
        self.setGeometry(0, 0, 1000, 400)
        self.center()

    def center(self):
        screen = QDesktopWidget().screenGeometry()

        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    #     self.setMaximumSize(round(screen.width()//1.4), round(screen.height()//1.6))

    def init_ui(self):
        # Create widgets
        self.id_entry = QLineEdit()
        self.password_entry = QLineEdit()
        self.password_entry.setEchoMode(QLineEdit.Password)  # To hide the password input
        self.forgot_password_label = QLabel('<a href="#">Forgot Password?</a>')
        self.forgot_password_label.linkActivated.connect(self.show_forgot_password_step)
        self.admin_connect_label = QLabel('<a style="text-decoration:none;color:black" href="#">Connect as admin?</a>')
        self.admin_connect_label.linkActivated.connect(self.admin_login)
        self.login_button = QPushButton('Login')
        self.login_button.clicked.connect(self.login)
        self.signup_button = QPushButton('Sign Up')
        self.signup_button.clicked.connect(self.signup)

        # Set up form layout for the Login window
        form_layout = QFormLayout()
        form_layout.addRow(QLabel('ID:'), self.id_entry)
        form_layout.addRow(QLabel('Password:'), self.password_entry)
        form_layout.addRow(self.forgot_password_label, self.admin_connect_label)
        form_layout.addRow(self.login_button)
        form_layout.addRow(self.signup_button)
        form_layout.setSpacing(20)

        # Centered Container Widget
        container_widget = QWidget()
        container_widget.setStyleSheet("background-color: rgb(245,245,245);")
        container_widget.setLayout(form_layout)
        container_widget.setFixedSize(500, 250)



        # Centered Layout
        center_layout = QHBoxLayout()
        center_layout.addWidget(container_widget, alignment=Qt.AlignmentFlag.AlignCenter)

        # Set up stacked widget for login steps
        self.stacked_widget = QStackedWidget(self)

        # Step 0: Login
        login_step = QWidget(self)
        login_step.setLayout(center_layout)  # Set the layout for login_step

        # Set a fixed size for the login widget
        # login_step.setFixedSize(300, 200)  # Adjust the size as needed

        self.stacked_widget.addWidget(login_step)

        # Step 1: Forgot Password
        forgot_password_step = ForgotPasswordStep(self)
        self.stacked_widget.addWidget(forgot_password_step)

        # step 2: Sign up
        signup = SignUpForm(self)
        self.stacked_widget.addWidget(signup)

        # step 3: user home page
        user_home_page = UserHomePage(self)
        self.stacked_widget.addWidget(user_home_page)

        # step 4: admin home page
        admin_home_page = AdminHomePage(self)
        self.stacked_widget.addWidget(admin_home_page)

        # Set up main layout
        main_layout = QGridLayout()
        main_layout.addWidget(self.stacked_widget)  # Add the stacked widget to the main layout
        # main_layout.setAlignment(self.stacked_widget, Qt.AlignCenter)

        # Set the layout for the main window
        self.setLayout(main_layout)

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

    def admin_login(self):
        dialog = AdminDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.stacked_widget.setCurrentIndex(4)
        else:
            print("Login canceled")
