from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QPushButton, QTabWidget, QWidget, QTableWidget, \
    QAbstractItemView

from account.view.admin.match import Matches
from account.view.admin.rechargement import Reload


class AdminHomePage(QMainWindow):
    def __init__(self, login_window=None):
        super().__init__()
        self.login_window = login_window

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
        self.tab_widget.addTab(self.tab3, "Tab 3")

        self.layout.addWidget(self.tab_widget)

        # Bottom Disconnect Button
        self.disconnect_button = QPushButton("Disconnect", self)
        self.disconnect_button.clicked.connect(self.disconnect)
        self.layout.addWidget(self.disconnect_button)  # Bottom-right alignment


    def disconnect(self):
        self.login_window.initialize()
