import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QComboBox, \
    QStackedWidget, QTreeWidget, QTreeWidgetItem, QTextEdit


class SignUpForm(QWidget):
    def __init__(self, login_window=None):
        super().__init__()

        self.setWindowTitle("Sign Up Form")
        self.setGeometry(100, 100, 800, 500)
        # Reference to the LoginWindow
        self.login_window = login_window
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
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
        self.address_input = QTextEdit()
        self.nif_cin_input = QLineEdit()

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
        self.next_button = QPushButton("Next", self)
        self.prev_button = QPushButton("Previous", self)
        self.back_button = QPushButton("Back", self)

        self.next_button.clicked.connect(self.next_step)
        self.prev_button.clicked.connect(self.prev_step)
        self.back_button.clicked.connect(self.back_to_login)

        self.layout.addWidget(self.tree_widget)
        self.layout.addWidget(self.stacked_widget)
        self.layout.addWidget(self.next_button)
        self.layout.addWidget(self.prev_button)
        self.layout.addWidget(self.back_button)

        self.current_step = 0
        self.update_tree()

    def update_tree(self):
        for i, item in enumerate(self.tree_items):
            if i == self.current_step:
                item.setCheckState(0, 2)  # Checked state
            elif i < self.current_step:
                item.setCheckState(0, 1)  # Checked state
            else:
                item.setCheckState(0, 0)  # Unchecked state

    def next_step(self):
        if self.current_step < self.stacked_widget.count() - 1:
            self.current_step += 1
            self.stacked_widget.setCurrentIndex(self.current_step)
            self.update_tree()

    def prev_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.stacked_widget.setCurrentIndex(self.current_step)
            self.update_tree()

    def back_to_login(self):
        self.login_window.stacked_widget.setCurrentIndex(0)

    def sign_up(self):
        # Add your sign-up logic here
        print("Signing up...")
        # You can retrieve the entered information using:
        # name = self.name_input.text()
        # first_name = self.first_name_input.text()
        # sex = self.sex_combobox.currentText()
        # telephone = self.telephone_input.text()
        # address = self.address_input.text()
        # nif_cin = self.nif_cin_input.text()
        # username = self.username_input.text()
        # password = self.password_input.text()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SignUpForm()
    window.show()
    sys.exit(app.exec_())
