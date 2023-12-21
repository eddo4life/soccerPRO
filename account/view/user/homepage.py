from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTabWidget, QStackedWidget, \
    QGridLayout

from account.model.userprofilemodel import UserProfileModel
from account.view.user.event import Event
from account.view.user.history import HistoryTabs
from account.view.user.profile.userprofile import UserProfile


class UserHomePage(QWidget):
    def __init__(self, login_window=None):
        super().__init__()
        # this instance is required to log out
        self.login_window = login_window
        self.init_ui()
        self.set_username(UserProfileModel().get_username())

    def init_ui(self):
        # Create the event tab
        tab_widget = QTabWidget()
        tab_widget.addTab(Event(), "Events")
        tab_widget.addTab(HistoryTabs(), "Tickets")

        # Main vertical layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.header())
        main_layout.addWidget(tab_widget)

        self.stacked_widget = QStackedWidget(self)

        widget = QWidget(self)
        widget.setLayout(main_layout)
        self.stacked_widget.addWidget(widget)
        self.stacked_widget.addWidget(UserProfile(self))

        grid_layout = QGridLayout()
        grid_layout.addWidget(self.stacked_widget)
        self.setLayout(grid_layout)

    def header(self):
        # Create components
        profile_icon = QLabel()
        profile_icon.setPixmap(QIcon("icon/user.png").pixmap(50, 50))
        self.username_label = QLabel()
        profile_icon.linkActivated.connect(self.open_profile)
        self.username_label.linkActivated.connect(self.open_profile)
        balance_label = QLabel("Balance: $100")

        # Vertical layout for the profile
        profile_layout = QVBoxLayout()
        profile_layout.addWidget(profile_icon)
        profile_layout.addWidget(self.username_label)

        # General horizontal layout

        header = QWidget()
        main_layout = QHBoxLayout(header)
        main_layout.addLayout(profile_layout)
        main_layout.addWidget(balance_label)

        return header

    def set_username(self, username):
        self.username_label.setText(f'<a style="text-decoration:none;color:black;" href="#">{username}</a>')

    def open_profile(self):
        self.stacked_widget.setCurrentIndex(1)

    def back_to_login(self):
        self.login_window.initialize()

    def initialize(self):
        self.stacked_widget.setCurrentIndex(0)
