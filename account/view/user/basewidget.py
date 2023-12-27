from PyQt5.QtWidgets import QWidget, QScrollArea, QVBoxLayout


class BaseWidget(QWidget):
    def __init__(self):
        """
        Initializes the BaseWidget.

        Returns:
        None
        """
        super().__init__()
        self.layout = QVBoxLayout()

        # Scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        scroll_widget = QWidget()
        scroll_widget.setLayout(self.layout)

        self.scroll_area.setWidget(scroll_widget)

    def add_widget(self, widget):
        """
        Adds a widget to the layout with alternating background colors.

        Parameters:
        - widget: QWidget
            The widget to be added.

        Returns:
        None
        """
        if self.layout.count() % 2 == 0:
            widget.setStyleSheet('background-color:rgb(255,255,255)')
        else:
            widget.setStyleSheet('background-color:rgb(225,225,225)')
        self.layout.addWidget(widget)

    def remove_widget(self, widget):
        """
        Removes a widget from the layout and revalidates it.

        Parameters:
        - widget: QWidget
            The widget to be removed.

        Returns:
        None
        """
        self.layout.removeWidget(widget)
        widget.setParent(None)
        self.revalidate_layout()

    def revalidate_layout(self):
        """
        Revalidates the layout by storing references to widgets, clearing the layout,
        and adding the widgets back.

        Returns:
        None
        """
        # Store references to the widgets
        widgets = [self.layout.itemAt(i).widget() for i in range(self.layout.count()) if
                   self.layout.itemAt(i) is not None]

        # Clear the layout
        self.clear_layout()

        # Add the widgets back to the layout
        for widget in widgets:
            self.add_widget(widget)

    def clear_layout(self):
        """
        Clears the layout by removing and deleting all items.

        Returns:
        None
        """
        while self.layout.count():
            self.layout.takeAt(0)
