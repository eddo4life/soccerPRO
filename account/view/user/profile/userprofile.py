from PyQt5.QtWidgets import QWidget, QFormLayout, QLineEdit, QComboBox, QTextEdit, QHBoxLayout, QPushButton, QLabel

from account.model.userprofilemodel import UserProfileModel


class UserProfile(QWidget):
    account_id = None

    def __init__(self, home):
        super().__init__()
        self.home = home
        self.upm = UserProfileModel()
        self.profile()
        self.update_values()

    def profile(self):
        form = QFormLayout()
        form.setSpacing(10)
        main_layout = QHBoxLayout(self)
        main_layout.addLayout(form)
        profile_label = QLabel('')
        main_layout.addWidget(profile_label)
        main_layout.setStretchFactor(form, 2)
        main_layout.setStretchFactor(profile_label, 1)

        self.username_input = QLineEdit()
        self.name_input = QLineEdit()
        self.first_name_input = QLineEdit()
        self.sex_combobox = QComboBox()
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

        self.upm.retrieve_data()
        UserProfile.account_id = self.upm.get_account_id()
        self.username_input.setText(self.upm.get_username())
        self.name_input.setText(self.upm.get_name())
        self.first_name_input.setText(self.upm.get_first_name())

        self.sex_combobox.addItems(["M", "F"])

        # Automatically select the value in the QComboBox that matches the sex from UserProfileModel
        current_sex = self.upm.get_sex()
        if current_sex in ["M", "F"]:
            index = self.sex_combobox.findText(current_sex)
            if index != -1:
                self.sex_combobox.setCurrentIndex(index)
        self.telephone_input.setText(self.upm.get_telephone())
        self.address_input.setText(self.upm.get_address())
        self.nif_cin_input.setText(self.upm.get_nif_cin())

    def get_sold(self):
        return self.upm.get_sold()

    def get_user_name(self):

        return self.upm.get_username()
