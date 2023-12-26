from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTabWidget, QStackedWidget, \
    QGridLayout, QPushButton

from account.view.user.event import Event
from account.view.user.history import HistoryTabs
from account.view.user.profile.userprofile import UserProfile
from labs.lab import Lab


class UserHomePage(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        # this instance is required to log out
        self.__main_window = main_window
        self.set_title()
        self.username_label = QLabel()
        self.sold_label = QLabel()
        self.user_profile = UserProfile(self)
        self.set_username(self.user_profile.get_user_name())
        self.set_sold(self.user_profile.get_sold())
        self.init_ui()

    def init_ui(self):
        # Create the event tab
        tab_widget = QTabWidget()
        tab_widget.addTab(Event(), Lab.get_icon('event.png'), "Events")
        tab_widget.addTab(HistoryTabs(), Lab.get_icon('history.png'), "History")

        # Main vertical layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.header())
        main_layout.addWidget(tab_widget)

        self.__stacked_widget = QStackedWidget(self)

        widget = QWidget(self)
        widget.setLayout(main_layout)
        self.__stacked_widget.addWidget(widget)
        self.__stacked_widget.addWidget(self.user_profile)

        grid_layout = QGridLayout()
        grid_layout.addWidget(self.__stacked_widget)
        self.setLayout(grid_layout)

    def header(self):
        # Create components
        profile_icon = QLabel()
        profile_icon.setPixmap(Lab.get_icon('user.png').pixmap(50, 50))

        profile_icon.linkActivated.connect(self.open_profile)
        self.username_label.linkActivated.connect(self.open_profile)

        # Vertical layout for the profile
        profile_layout = QVBoxLayout()
        profile_layout.addWidget(profile_icon)
        profile_layout.addWidget(self.username_label)

        # General horizontal layout

        header = QWidget()
        main_layout = QHBoxLayout(header)
        main_layout.addLayout(profile_layout)
        main_layout.addWidget(self.sold_label)

        connect = QPushButton('Se connecter')
        # login
        connect.clicked.connect(lambda: self.__main_window.initialize())
        Lab.set_size_policy_fixed(connect)

        return header if UserProfile.account_id else connect

    def set_username(self, username):
        self.username_label.setText(f'<a style="text-decoration:none;color:black;" href="#">{username}</a>')

    def set_sold(self, sold):
        self.sold_label.setText('Sold : ' + str(sold))

    def open_profile(self):
        self.set_title('User profile')
        self.__stacked_widget.setCurrentIndex(1)

    def logout(self):
        self.set_title('Login')
        self.__main_window.initialize()

    def home(self):
        self.set_title()
        self.__stacked_widget.setCurrentIndex(0)

    # this method is used from the profile window in order to access the main window instance
    # to set the title accordingly
    def set_title(self, title='User home-page'):
        self.__main_window.setWindowTitle(title)
