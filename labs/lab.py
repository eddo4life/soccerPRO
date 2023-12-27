import uuid
from datetime import datetime

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QSizePolicy, QWidget, QHBoxLayout


class Lab:
    """
    Back-end section
    """

    @staticmethod
    def generate_id():
        """
        Generates a unique ID using uuid.
        Returns:
            str: A unique ID.
        """
        unique_id = str(uuid.uuid4().hex)[:8]
        return unique_id

    @staticmethod
    def get_flattened_values(input_dict):
        """
        Takes a dictionary of lists and returns the combined values of all the lists.
        Args:
            input_dict (dict): A dictionary of lists.
        Returns:
            list: A list containing the values of all the lists.
        """
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

    @staticmethod
    def set_size_policy_fixed(widget):
        """
        Sets the size policy of a widget to fixed.
        Args:
            widget (QWidget): The widget to set the size policy for.
        """
        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        widget.setSizePolicy(size_policy)

    @staticmethod
    def get_centered_layout(layout, w=500, h=250):
        """
        Takes a layout and returns it centered within a fixed-size container widget.
        Args:
            layout: The layout to be centered.
            w (int): Width of the container widget.
            h (int): Height of the container widget.
        Returns:
            QHBoxLayout: A centered layout.
        """
        layout.setSpacing(20)
        container_widget = QWidget()
        container_widget.setLayout(layout)
        container_widget.setFixedSize(w, h)
        center_layout = QHBoxLayout()
        center_layout.addWidget(container_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        return center_layout

    @staticmethod
    def get_icon(name):
        """
        Loads and returns an icon by name.
        Args:
            name (str): The name of the icon file.
        Returns:
            QIcon: The loaded icon.
        """
        return QIcon("icon/" + name)
