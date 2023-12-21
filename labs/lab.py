import uuid
from datetime import datetime

from PyQt5.QtWidgets import QSizePolicy


class Lab:
    # Back-end section
    @staticmethod
    def generate_id():
        unique_id = str(uuid.uuid4().hex)[:8]
        return unique_id

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

    #     Front-end section
    @staticmethod
    def set_size_policy_fixed( widget):
        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        widget.setSizePolicy(size_policy)
