from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QPushButton, QTabWidget, QWidget

from account.view.admin.match import Matches
from account.view.admin.rechargement import Reload
from labs.lab import Lab


class AdminHomePage(QMainWindow):
    def __init__(self, main_window=None):
        """
        AdminHomePage constructor.

        Args:
            main_window (MainWindow): The main window instance.
        """
        super().__init__()
        self.main_window = main_window

        # Set up the central widget and layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Top Label
        self.label_admin_account = QLabel("<h1>Admin Account</h1>", self)
        self.layout.addWidget(self.label_admin_account)

        # Middle Tabs
        self.tab_widget = QTabWidget(self)
        self.tab2 = QWidget(self)
        self.tab3 = QWidget(self)

        # Add tabs to the tab widget
        self.tab_widget.addTab(Reload(), "Renflouement")
        self.tab_widget.addTab(Matches(), "Gestion match")
        self.layout.addWidget(self.tab_widget)

        # Bottom Disconnect Button
        self.disconnect_button = QPushButton("Disconnect", self)
        self.disconnect_button.clicked.connect(self.disconnect)
        self.layout.addWidget(self.disconnect_button)  # Bottom-right alignment
        Lab.set_size_policy_fixed(self.disconnect_button)

        # Set styles for the Disconnect button
        self.disconnect_button.setStyleSheet(
            '''
            QPushButton:hover {
                color: red;
            }
             QPushButton {
                border: none; 
            }
            '''
        )

    def disconnect(self):
        """
        Disconnect button click event handler. Returns to the main login window.
        """
        self.main_window.initialize()
