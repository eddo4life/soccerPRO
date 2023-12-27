from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QFormLayout, QLineEdit, QComboBox, QTextEdit, QHBoxLayout, QPushButton, QLabel, \
    QVBoxLayout, QFrame, QCheckBox, QMessageBox

from account.model.userprofilemodel import UserProfileModel
from account.view.dialog import ConfirmDialog
from labs.lab import Lab


class UserProfile(QWidget):
    # some important credentials
    user_fund = None
    account_id = None
    user_name = None
    user_password = None
    user_status = None

    @classmethod
    def init_credentials(cls, telephone, password):
        UserProfile.user_name = telephone
        UserProfile.user_password = password

    def __init__(self, home):
        super().__init__()
        self.upm = None
        self.home = home
        self.profile()
        self.update_values()

    def profile(self):

        main_layout = QVBoxLayout(self)

        h_separator = QFrame()
        h_separator.setFrameShape(QFrame.HLine)
        h_separator.setFrameShadow(QFrame.Sunken)

        header_layout = QVBoxLayout()
        main_layout.addLayout(header_layout)
        header_layout.addWidget(QLabel('<h2>Informations personelles</h2>'))
        header_layout.addWidget(h_separator)

        content_layout = QHBoxLayout()
        main_layout.addLayout(content_layout)

        pic_layout = QVBoxLayout()
        pic_layout.setAlignment(Qt.AlignTop)
        self.profile_pic = QLabel()

        pic_layout.addWidget(self.profile_pic)

        self.name_label = QLabel()

        pic_layout.addWidget(self.name_label)

        # add delete or closed account
        dc = QFormLayout()
        self.account_status_box = QComboBox()
        self.account_status_box.currentIndexChanged.connect(self.update_status)
        self.account_status_box.addItems(['Actif', 'Fermer', 'Supprimer'])
        dc.addRow('Mon compte :', self.account_status_box)
        pic_layout.addLayout(dc)

        background = QWidget()
        background.setStyleSheet("""
        background-color: rgba(255, 255, 255, 0.5);
        """
                                 )

        # Add vertical separator
        v_separator = QFrame()
        v_separator.setFrameShape(QFrame.VLine)
        v_separator.setFrameShadow(QFrame.Sunken)

        background.setLayout(pic_layout)

        content_layout.addWidget(background)
        content_layout.addWidget(v_separator)
        # form to show the user's information
        form = QFormLayout()
        form.setSpacing(10)
        form.setAlignment(Qt.AlignTop)

        content_layout.addLayout(form)

        content_layout.setStretchFactor(background, 1)
        content_layout.setStretchFactor(form, 4)

        self.username_input = QLineEdit()
        self.name_input = QLineEdit()
        self.first_name_input = QLineEdit()
        self.sex_combobox = QComboBox()
        self.telephone_input = QLineEdit()
        self.address_input = QTextEdit()
        self.address_input.setFixedHeight(200)
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
        update_button.clicked.connect(self.retrieve_values)
        back_button = QPushButton('Back')
        back_button.clicked.connect(self.back_home)
        logout_button = QPushButton('Logout')
        logout_button.clicked.connect(lambda: self.home.logout())
        hbox.addWidget(update_button, 1)
        hbox.addWidget(back_button, 1)
        hbox.addWidget(logout_button, 1)
        self.password_check_box = QCheckBox('Update password')
        self.password_check_box.clicked.connect(lambda: self.password_enablings(self.password_check_box.isChecked()))
        form.addRow(self.password_check_box, hbox)
        self.feed_back_label = QLabel('feed back')
        self.feed_back_label.setFixedHeight(25)
        # form.addRow(self.feed_back_label)

        self.setStyleSheet("""
        QLineEdit { height: 30px; }
        """)

        #     disable passwords fields by default
        self.password_enablings(False)

    def password_enablings(self, is_enabled):
        self.password_input.setEnabled(is_enabled)
        self.new_password_input.setEnabled(is_enabled)
        self.confirm_new_password_input.setEnabled(is_enabled)

    def back_home(self):
        self.home.home()

    def retrieve_values(self):
        username = self.username_input.text().strip()
        name = self.name_input.text().upper().strip()
        first_name = self.first_name_input.text().title().strip()
        sex = self.sex_combobox.currentText()
        telephone = self.telephone_input.text()
        address = self.address_input.toPlainText().strip()
        nif_cin = self.nif_cin_input.text().strip()
        password = self.password_input.text()
        new_password = self.new_password_input.text()
        confirm_new_password = self.confirm_new_password_input.text()

        tests_passed = True

        if self.password_check_box.isChecked():
            # test if the old password is actually the same:
            if UserProfile.user_password == password:
                # test if the password is well confirmed
                if new_password == confirm_new_password:
                    # assign the new password
                    UserProfile.user_password = new_password
                    # clear fields
                    self.confirm_new_password_input.setText('')
                    self.new_password_input.setText('')
                    self.password_input.setText('')
                    self.password_check_box.setChecked(False)
                    self.password_enablings(False)
                else:
                    tests_passed = False
                    QMessageBox.warning(None, "Denied", 'Veuillez saisir deux mots de passe identiques!',
                                        QMessageBox.Ok)
            else:
                tests_passed = False
                self.feed_back_label.setText('Mot de passe incorrecte')
                QMessageBox.warning(None, "Denied", 'Mot de passe incorrecte!', QMessageBox.Ok)

        if tests_passed:
            # if ever the user name was changed
            UserProfile.user_name = username
            # set up the model
            upm = UserProfileModel(account_id=UserProfile.account_id, username=UserProfile.user_name, name=name,
                                   sex=sex,
                                   first_name=first_name,
                                   address=address, telephone=telephone, nif_cin=nif_cin,
                                   password=UserProfile.user_password,
                                   status=UserProfile.user_status[0].upper())
            upm.update()
            # reload
            self.update_values()

    def save(self):
        self.retrieve_values()

    def update_values(self):
        self.upm = UserProfileModel()
        self.upm.retrieve_data(UserProfile.user_name, UserProfile.user_password)
        # store the account id
        UserProfile.account_id = self.upm.get_account_id()

        self.username_input.setText(self.upm.get_username())
        # update the username at user home window
        self.home.set_username(self.upm.get_username())

        # set the full name (username)
        self.name_label.setText('<h3>' +
                                str(self.upm.get_name()) + ' ' + str(self.upm.get_first_name()) + ' (' + str(
            self.upm.get_username()) + ')</h3>')

        self.name_input.setText(self.upm.get_name())
        self.first_name_input.setText(self.upm.get_first_name())

        self.sex_combobox.addItems(["M", "F"])
        # Automatically select the value in the QComboBox that matches the sex from UserProfileModel
        current_sex = self.upm.get_sex()
        if current_sex in ["M", "F"]:
            index = self.sex_combobox.findText(current_sex)
            if index != -1:
                self.sex_combobox.setCurrentIndex(index)
                if index == 0:
                    self.profile_pic.setPixmap(Lab.get_icon('man.png').pixmap(255, 250))
                else:
                    self.profile_pic.setPixmap(Lab.get_icon('woman.png').pixmap(255, 250))

        # retrieve the current status
        UserProfile.user_status = self.find_status(self.upm.get_status())
        # set the current state of the account to the combobox
        index = self.account_status_box.findText(UserProfile.user_status)
        if index != -1:
            self.account_status_box.setCurrentIndex(index)

        self.telephone_input.setText(self.upm.get_telephone())
        self.address_input.setText(self.upm.get_address())
        self.nif_cin_input.setText(self.upm.get_nif_cin())
        UserProfile.user_fund = self.upm.get_sold()

    def find_status(self, stat):
        if stat:
            stat = stat.lower()
            if stat == 'a':
                return 'Actif'
            elif stat == 'f':
                return 'Fermer'

    def update_status(self):
        if UserProfile.user_status:
            # retrieve the initial index
            index = self.account_status_box.findText(UserProfile.user_status)
            # keep track of the selected status
            UserProfile.user_status = self.account_status_box.currentText()

            if UserProfile.user_status[0].upper() == 'S':
                if ConfirmDialog.confirmed('Suprression du compte est definitive, voulez-vous continuer? '):
                    # dete the account
                    UserProfileModel.delete_account(UserProfile.account_id)
                    # loging out
                    self.home.logout()
                else:
                    # set it to the initial state
                    self.account_status_box.setCurrentIndex(index)

    def get_sold(self):
        return self.upm.get_sold()

    def get_user_name(self):
        return self.upm.get_username()
