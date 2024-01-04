import re
import sys
import uuid
from datetime import datetime

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QSizePolicy, QWidget, QHBoxLayout, QDialog, QMessageBox


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
    def validate_score_format(input_string):
        """
        Validates the format of a score input string.

        Args:
            input_string (str): The input string representing the score in the format 'mm:ss',
                               where mm is minutes (1 or 2 digits) and ss is seconds (1 or 2 digits).

        Returns:
            bool: True if the input string has a valid score format, False otherwise.
        """
        pattern = r'^(\d{1,2}:\d{1,2})$'
        return bool(re.match(pattern, input_string))

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
    def invoke_config(msg):
        """
        Displays a warning message and invokes the configuration dialog.

        Args:
            msg (str): The warning message to be displayed.

        Returns:
            None

        The function displays a warning message using QMessageBox and then opens the
        configuration dialog from config.config.Configuration. If the configuration
        dialog is not accepted (user cancels or closes it), the program exits.
        """
        QMessageBox.warning(None, "Table or database not found ", msg, QMessageBox.Ok)
        from config.config import Configuration
        dialog = Configuration()
        if dialog.exec_() != QDialog.Accepted:
            sys.exit()

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

    @staticmethod
    def show_confirm_dialog(title, msg):
        """
        Display a confirmation dialog with the specified title and message.

        Parameters:
        - title (str): The title of the confirmation dialog.
        - msg (str): The message to be displayed in the confirmation dialog.

        Returns:
        bool: True if the user clicks 'Yes,' False otherwise.
        """
        confirm_box = QMessageBox()
        confirm_box.setWindowTitle(title)
        confirm_box.setIcon(QMessageBox.Question)
        confirm_box.setText(msg)
        confirm_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        return confirm_box.exec_() == QMessageBox.Yes

    @staticmethod
    def get_logout_btn_style():
        return '''
            QPushButton:hover {
                color: red;
            }
            '''

    @staticmethod
    def apply_table_style(table):
        stylesheet = """
        QTableWidget {
            border: 1px solid black;
            gridline-color: #555;
            background-color: #f0f0f0;
        }

        QTableWidget::item {
            padding: 5px;
            border: 1px solid #ccc;
        }

        QTableWidget::item:selected {
            background-color: #99c5ff;
        }

        /* Header styling */
        QHeaderView::section {
            background-color: #eee;
            padding: 5px;
            border: 1px solid #ccc;
            font-weight: bold;
        }
        """
        table.setStyleSheet(stylesheet)
