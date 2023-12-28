from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QFormLayout, QVBoxLayout, \
    QDialog

from labs.lab import Lab


class AdminDialog(QDialog):
    def __init__(self, parent=None):
        """
        Constructor for the AdminDialog.

        :param parent: Parent widget, if any.
        """
        super().__init__(parent)
        self.setWindowTitle("Login admin")
        self.setFixedSize(400, 250)

        # Labels
        self.id_label = QLabel("ID:")
        self.password_label = QLabel("Password:")
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red")

        # Input fields
        self.id_edit = QLineEdit('admin')
        self.password_edit = QLineEdit('1234')
        self.password_edit.setEchoMode(QLineEdit.Password)

        # Connect button
        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.check_credentials)

        # Set up the layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.id_label)
        layout.addWidget(self.id_edit)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_edit)
        layout.addWidget(self.error_label)
        layout.addWidget(self.connect_button)

    def check_credentials(self):
        """
        Check the entered credentials.

        If the credentials are correct, accept the dialog; otherwise, display an error message.
        """
        entered_id = self.id_edit.text()
        entered_password = self.password_edit.text()

        # Check if ID is 'admin' and password is '1234' (default, can be changed later)
        if entered_id == 'admin' and entered_password == '1234':
            self.accept()  # Accept the dialog (credentials are correct)
        else:
            self.error_label.setText("Incorrect credentials")


class LoginWindow(QWidget):
    def __init__(self, main_window):
        """
        Constructor for the LoginWindow.

        :param main_window: The main window, usually a MainWindow instance.
        """
        super().__init__()
        # get the stack from the main window
        self.__main_window = main_window
        # Set up UI elements for the Login window
        self.init_ui()

    def init_ui(self):
        """
        Initialize the UI elements for the Login window.
        """
        # Create widgets
        self.id_entry = QLineEdit()
        self.password_entry = QLineEdit()
        self.password_entry.setEchoMode(QLineEdit.Password)  # To hide the password input
        self.forgot_password_label = QLabel('<a href="#">Forgot Password?</a>')
        self.forgot_password_label.linkActivated.connect(self.show_forgot_password_step)
        self.admin_connect_label = QLabel('<a style="text-decoration:none;color:black" href="#">Connect as admin?</a>')
        self.admin_connect_label.linkActivated.connect(self.admin_login)
        self.login_button = QPushButton('Login')
        self.login_button.clicked.connect(
            lambda: self.__main_window.login(self.id_entry.text(), self.password_entry.text()))
        self.signup_button = QPushButton('Sign Up')
        self.signup_button.clicked.connect(self.signup)

        # Set up form layout for the Login window
        form_layout = QFormLayout()
        form_layout.addRow(QLabel('ID:'), self.id_entry)
        form_layout.addRow(QLabel('Password:'), self.password_entry)
        form_layout.addRow(self.forgot_password_label, self.admin_connect_label)
        form_layout.addRow(self.login_button)
        form_layout.addRow(self.signup_button)

        # Set the layout for the main window
        self.setLayout(Lab.get_centered_layout(form_layout))

    def show_forgot_password_step(self):
        """
        Show the Forgot Password step.
        """
        # Switch to the Forgot Password step
        self.__main_window.set_title('Forgot password')
        self.__main_window.change_step(1)

    def signup(self):
        """
        Switch to the Sign-up step.
        """
        # Switch to the Sign-up step
        self.__main_window.set_title('Signup')
        self.__main_window.change_step(2)

    def admin_login(self):
        """
        Perform admin login.
        """
        dialog = AdminDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.__main_window.set_title('Admin home page')
            self.__main_window.change_step(4)
