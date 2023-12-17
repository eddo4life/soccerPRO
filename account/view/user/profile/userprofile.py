from PyQt5.QtWidgets import QWidget, QFormLayout, QLineEdit, QComboBox, QTextEdit, QHBoxLayout, QPushButton

from account.model.userprofilemodel import UserProfileModel


class UserProfile(QWidget):
    def __init__(self, home):
        super().__init__()
        self.home = home
        self.profile()
        self.update_values()

    def profile(self):
        form = QFormLayout(self)
        self.username_input = QLineEdit()
        self.name_input = QLineEdit()
        self.first_name_input = QLineEdit()
        self.sex_combobox = QComboBox()
        self.sex_combobox.addItems(["M", "F"])
        self.telephone_input = QLineEdit()
        self.address_input = QTextEdit()
        self.nif_cin_input = QLineEdit()
        self.password_input = QLineEdit()
        self.new_password_input = QLineEdit()
        self.confirm_new_password_input = QLineEdit()
        self.new_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_new_password_input.setEchoMode(QLineEdit.Password)

        form.addRow("Username:", self.username_input)
        form.addRow("Name:", self.name_input)
        form.addRow("First Name:", self.first_name_input)
        form.addRow("Sex:", self.sex_combobox)
        form.addRow("Telephone:", self.telephone_input)
        form.addRow("Address:", self.address_input)
        form.addRow("NIF/CIN:", self.nif_cin_input)
        form.addRow("Old Password:", self.password_input)
        form.addRow("new Password:", self.new_password_input)
        form.addRow("Confirm Password:", self.confirm_new_password_input)

        hbox = QHBoxLayout()
        update_button = QPushButton('Update')
        back_button = QPushButton('Back')
        back_button.clicked.connect(self.back_home)
        logout_button = QPushButton('Logout')
        logout_button.clicked.connect(self.logout)
        hbox.addWidget(update_button, 1)
        hbox.addWidget(back_button, 1)
        hbox.addWidget(logout_button, 1)
        form.addRow('Action', hbox)

    def logout(self):
        self.home.back_to_login()

    def back_home(self):
        self.home.initialize()

    def save(self):
        ...

    def update_values(self):
        upm = UserProfileModel()
        self.username_input.setText(upm.username)
        self.name_input.setText(upm.name)
        self.first_name_input.setText(upm.first_name)
        self.sex_combobox = QComboBox()
        self.sex_combobox.addItems(["M", "F"])
        # self.sex_combobox...select the value
        self.telephone_input.setText(upm.telephone)
        self.address_input.setText(upm.adress)
        self.nif_cin_input.setText(upm.nif_cin)
