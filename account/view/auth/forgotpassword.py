from PyQt5.QtWidgets import QFormLayout, QPushButton, QLineEdit, QLabel, QWidget, QMessageBox

from account.model.userprofilemodel import UserProfileModel
from labs.lab import Lab


class ForgotPassword(QWidget):
    def __init__(self, main_window):
        """
        Constructor for SignUpForm widget.

        :param main_window: Reference to the main window, usually a MainWindow instance.
        """

        super().__init__()

        self.__main_window = main_window

        # Set up UI elements for the Forgot Password step
        self.init_ui()

    def init_ui(self):
        """
        Initialize the UI elements for the Forgot Password step.
        """
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
        self.reset_password_button.clicked.connect(self.reset_password)
        self.back_button = QPushButton('Back')
        self.back_button.clicked.connect(self.show_previous_login_step)
        self.back_button.setStyleSheet(Lab.get_logout_btn_style())

        # Set up form layout for the Forgot Password step
        form_layout = QFormLayout()
        form_layout.addRow(self.nif_cin_label, self.nif_cin_entry)
        form_layout.addRow(self.telephone_label, self.telephone_entry)
        form_layout.addRow(self.new_password_label, self.new_password_entry)
        form_layout.addRow(self.confirm_password_label, self.confirm_password_entry)
        form_layout.addRow(self.back_button, self.reset_password_button)

        # Set the layout for the Forgot Password step
        self.setLayout(Lab.get_centered_layout(form_layout, 700, 300))

    def reset_password(self):
        """
        Reset the password based on user input.
        """
        nif_cin = self.nif_cin_entry.text().strip()
        telephone = self.telephone_entry.text().strip()
        password1 = self.new_password_entry.text()
        password2 = self.confirm_password_entry.text()
        if password1 == password2:
            if UserProfileModel.reset_password(password1, nif_cin, telephone):
                # Automatically login with telephone and password
                self.__main_window.login(telephone, password2)
            else:
                QMessageBox.warning(None, "Denied", 'Informations incorrectes!', QMessageBox.Ok)
        else:
            QMessageBox.warning(None, "Denied", 'Veuillez saisir deux mots de passe identiques!', QMessageBox.Ok)

    def show_previous_login_step(self):
        """
        Show the previous login step.
        """
        self.__main_window.initialize()
