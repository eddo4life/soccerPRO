import uuid

from PyQt5.QtGui import QColor


class Lab:

    @staticmethod
    def generate_id():
        unique_id = str(uuid.uuid4().hex)[:8]
        return unique_id


def adjust_second_widget_color(first_widget, second_widget):
    # Access the background colors of the first and second widgets
    first_widget_color = first_widget.palette().color(first_widget.backgroundRole())
    second_widget_color = second_widget.palette().color(second_widget.backgroundRole())

    # Compare the background colors
    if (
            first_widget_color.red() == second_widget_color.red() and
            first_widget_color.green() == second_widget_color.green() and
            first_widget_color.blue() == second_widget_color.blue()
    ):
        # Check the property of the first widget's color
        if first_widget_color == QColor(250, 250, 250):
            # Adjust the second widget's color accordingly
            if second_widget_color == QColor(250, 250, 250):
                second_widget.setStyleSheet("background-color: 240, 240, 240;")
            elif second_widget_color == QColor(240, 240, 240):
                second_widget.setStyleSheet("background-color: 250, 250, 250;")
    # If the background colors are not equal, do nothing
