from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTabWidget, QStackedWidget, \
    QGridLayout, QPushButton

from account.view.user.event import Event
from account.view.user.history import HistoryTabs
from account.view.user.profile.userprofile import UserProfile
from labs.lab import Lab


class UserHomePage(QWidget):
    def __init__(self, main_window=None):
        super().__init__()

        # Reference to the main window for logout functionality
        self.__main_window = main_window

        # Initialize UI components
        self.set_title()
        self.username_label = QLabel()
        self.sold_label = QLabel()
        self.user_profile = UserProfile(self)
        self.set_username(self.user_profile.get_user_name())
        self.set_sold(self.user_profile.get_sold())
        self.init_ui()

    def init_ui(self):
        # Create the event and history tabs
        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(Event(self), Lab.get_icon('event.png'), "Events")
        self.tab_widget.addTab(HistoryTabs(), Lab.get_icon('history.png'), "History")

        # Main vertical layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.header())
        main_layout.addWidget(self.tab_widget)

        # Stacked widget for switching between main content and user profile
        self.__stacked_widget = QStackedWidget(self)
        widget = QWidget(self)
        widget.setLayout(main_layout)
        self.__stacked_widget.addWidget(widget)
        self.__stacked_widget.addWidget(self.user_profile)

        # Grid layout to arrange the stacked widget
        grid_layout = QGridLayout()
        grid_layout.addWidget(self.__stacked_widget)
        self.setLayout(grid_layout)

    def revalidate_history_tab(self):
        # Refresh the history tab
        self.tab_widget.removeTab(1)
        self.tab_widget.addTab(HistoryTabs(), Lab.get_icon('history.png'), "History")

    def header(self):
        # Create components for the header
        profile_icon = QLabel()
        profile_icon.setPixmap(Lab.get_icon('user.png').pixmap(50, 50))

        profile_icon.linkActivated.connect(self.open_profile)
        self.username_label.linkActivated.connect(self.open_profile)

        # Vertical layout for the profile
        profile_layout = QVBoxLayout()
        profile_layout.addWidget(profile_icon)
        profile_layout.addWidget(self.username_label)

        # General horizontal layout for the header
        header = QWidget()
        main_layout = QHBoxLayout(header)
        main_layout.addLayout(profile_layout)
        main_layout.addWidget(self.sold_label)

        # Connect button for login (if not logged in)
        connect = QPushButton('Se connecter')
        connect.clicked.connect(lambda: self.__main_window.initialize())
        Lab.set_size_policy_fixed(connect)

        return header if UserProfile.account_id else connect

    def set_username(self, username):
        # Set the displayed username with a hyperlink
        self.username_label.setText(f'<a style="text-decoration:none;color:black;" href="#">{username}</a>')

    def set_sold(self, sold):
        # Set the displayed sold amount
        self.sold_label.setText('Sold : ' + str(sold))

    def open_profile(self):
        # Switch to the user profile view
        self.set_title('User profile')
        self.__stacked_widget.setCurrentIndex(1)

    def logout(self):
        # Logout and switch to the login view
        self.set_title('Login')
        self.__main_window.initialize()

    def home(self):
        # Switch to the home view
        self.set_title()
        self.__stacked_widget.setCurrentIndex(0)

    def set_title(self, title='User home-page'):
        # Set the title of the main window from the user home page
        self.__main_window.setWindowTitle(title)
