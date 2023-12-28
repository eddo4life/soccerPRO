from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QComboBox, \
    QStackedWidget, QTreeWidget, QTreeWidgetItem, QTextEdit, QHBoxLayout, QMessageBox

from account.model.userprofilemodel import UserProfileModel
from labs.lab import Lab


class SignUpForm(QWidget):
    def __init__(self, main_window=None):
        """
        Constructor for SignUpForm widget.

        :param main_window: Reference to the main window, usually a MainWindow instance.
        """
        super().__init__()

        self.__main_window = main_window
        self.init_ui()

    def init_ui(self):
        """
        Initialize the user interface components for the sign-up form.
        """
        self.layout = QVBoxLayout()
        # Create a tree widget for the progress indicator
        self.tree_widget = QTreeWidget(self)
        self.tree_widget.setHeaderHidden(True)

        # Add items to the tree widget
        items = ["Personal Information", "Contact Information", "Username and Password"]
        self.tree_items = [QTreeWidgetItem([item]) for item in items]
        self.tree_widget.addTopLevelItems(self.tree_items)

        # Disable the checkboxes
        for item in self.tree_items:
            item.setFlags(item.flags() & ~Qt.ItemIsUserCheckable)

        # Set up the stacked widget for the steps
        self.stacked_widget = QStackedWidget(self)

        # Step 1: Personal Information
        step1_widget = QWidget(self)
        layout1 = QFormLayout(step1_widget)
        self.name_input = QLineEdit()
        self.first_name_input = QLineEdit()
        self.sex_combobox = QComboBox()
        self.sex_combobox.addItems(["M", "F"])

        layout1.addRow("Name:", self.name_input)
        layout1.addRow("First Name:", self.first_name_input)
        layout1.addRow("Sex:", self.sex_combobox)

        self.stacked_widget.addWidget(step1_widget)

        # Step 2: Contact Information
        step2_widget = QWidget(self)
        layout2 = QFormLayout(step2_widget)
        self.telephone_input = QLineEdit()
        self.telephone_input.setValidator(QIntValidator())
        self.address_input = QTextEdit()
        self.nif_cin_input = QLineEdit()
        self.nif_cin_input.setValidator(QIntValidator())

        layout2.addRow("Telephone:", self.telephone_input)
        layout2.addRow("Address:", self.address_input)
        layout2.addRow("NIF/CIN:", self.nif_cin_input)

        self.stacked_widget.addWidget(step2_widget)

        # Step 3: Username and Password
        step3_widget = QWidget(self)
        layout3 = QFormLayout(step3_widget)
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.signup_button = QPushButton("Sign Up", self)
        self.signup_button.clicked.connect(self.sign_up)

        layout3.addRow("Username:", self.username_input)
        layout3.addRow("Password:", self.password_input)
        layout3.addWidget(self.signup_button)

        self.stacked_widget.addWidget(step3_widget)

        # Navigation buttons
        self.prev_button = QPushButton("Previous", self)
        self.next_button = QPushButton("Next", self)
        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.setStyleSheet(
            '''
            QPushButton:hover {
                color: red;
            }
            '''
        )

        self.next_button.clicked.connect(self.next_step)
        self.prev_button.clicked.connect(self.prev_step)
        self.cancel_button.clicked.connect(self.back_to_login)

        self.layout.addWidget(self.tree_widget)
        self.layout.addWidget(self.stacked_widget)
        hbox = QHBoxLayout()
        hbox.addWidget(self.prev_button)
        hbox.addWidget(self.next_button)
        hbox.addWidget(self.cancel_button)
        self.layout.addLayout(hbox)
        self.current_step = 0  # initially
        self.update_tree()
        #     set the layout
        self.setLayout(Lab.get_centered_layout(self.layout, 1000, 700))

    def update_tree(self):
        """
        Update the visual indication of the sign-up progress in the tree widget.
        """
        for i, item in enumerate(self.tree_items):
            if i == self.current_step:
                item.setCheckState(0, 2)  # Checked state
            elif i < self.current_step:
                item.setCheckState(0, 1)  # Checked state
            else:
                item.setCheckState(0, 0)  # Unchecked state

    def next_step(self):
        """
        Move to the next step in the sign-up process.
        """
        if self.current_step < self.stacked_widget.count() - 1:
            self.current_step += 1
            self.stacked_widget.setCurrentIndex(self.current_step)
            self.update_tree()

    def prev_step(self):
        """
        Move to the previous step in the sign-up process.
        """
        if self.current_step > 0:
            self.current_step -= 1
            self.stacked_widget.setCurrentIndex(self.current_step)
            self.update_tree()

    def back_to_login(self):
        """
        Go back to the login screen when the user cancels the sign-up process.
        """
        self.__main_window.initialize()

    def sign_up(self):
        """
        Process the user's sign-up request and save the entered information.

        If the entered information is valid, the user is signed up, and the main window is updated accordingly.
        Otherwise, an error message is displayed.
        """
        # Retrieving and cleaning information:
        name = self.name_input.text().upper().strip()
        first_name = self.first_name_input.text().title().strip()
        sex = self.sex_combobox.currentText().strip()
        telephone = self.telephone_input.text().strip()
        address = self.address_input.toPlainText().strip()
        nif_cin = self.nif_cin_input.text().strip()
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        upm = UserProfileModel(account_id=Lab.generate_id(), username=username, name=name, sex=sex,
                               first_name=first_name,
                               address=address, telephone=telephone, nif_cin=nif_cin, password=password, status='A')

        if upm.valid_data():
            #  proceed and check if any message was not returned
            error_message = upm.save()
            if not error_message:
                # automatically login with telephone and password
                self.__main_window.login(telephone, password)
            else:
                # an error occurs
                if "Duplicate entry" in error_message and "parieur.telephone" in error_message:
                    error_message = "Le numéro de téléphone est déjà en cours d'utilisation."
                elif "Duplicate entry" in error_message and "parieur.nif_cin" in error_message:
                    error_message = "Le NIF/CIN est déjà en cours d'utilisation."
                elif "Duplicate entry" in error_message and "parieur.username" in error_message:
                    error_message = "Le nom d'utilisateur est déjà pris."
                else:
                    error_message = "An unexpected error occurred: " + error_message
                QMessageBox.warning(None, "Denied", error_message, QMessageBox.Ok)
        else:
            QMessageBox.warning(None, "Denied", 'Toutes les informations sont requises!', QMessageBox.Ok)
