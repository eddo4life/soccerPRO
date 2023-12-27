import uuid
from datetime import datetime

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QSizePolicy, QHBoxLayout, QWidget


class Lab:
    """
     Back-end section
    """

    # auto generated id method for the user account_id
    @staticmethod
    def generate_id():
        unique_id = str(uuid.uuid4().hex)[:8]
        return unique_id

    # this method take a dictionary of list and returns the value of all the lists combined
    @staticmethod
    def get_flattened_values(input_dict):
        value_list = list(input_dict.values())
        flattened_keys = [val for sublist in value_list for val in sublist]
        return flattened_keys

    @staticmethod
    def get_current_date():
        """
        Returns the current date in the format 'YYYY-MM-DD'.
        """
        return datetime.now().strftime('%Y-%m-%d')

    @staticmethod
    def get_current_time():
        """
        Returns the current time in the format 'HH:MM'.
        """
        return datetime.now().strftime('%H:%M')

    """
    Front-end section
    """

    # make a widget fit it's initial size
    @staticmethod
    def set_size_policy_fixed(widget):
        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        widget.setSizePolicy(size_policy)

    # this takes a layout and return it centered
    @staticmethod
    def get_centered_layout(layout, w=500, h=250):
        layout.setSpacing(20)
        container_widget = QWidget()
        # container_widget.setStyleSheet("background-color: rgb(250,250,250);")
        container_widget.setLayout(layout)
        container_widget.setFixedSize(w, h)
        # Centered Layout
        center_layout = QHBoxLayout()
        center_layout.addWidget(container_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        return center_layout

    # load icons
    @staticmethod
    def get_icon(name):
        return QIcon("icon/" + name)
