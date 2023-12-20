from PyQt5.QtWidgets import QWidget, QScrollArea, QVBoxLayout


class BaseWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        # scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        scroll_widget = QWidget()
        scroll_widget.setLayout(self.layout)

        self.scroll_area.setWidget(scroll_widget)

    def add_widget(self, widget):
        if self.layout.count() % 2 == 0:
            widget.setStyleSheet('background-color:rgb(253,253,253)')
        else:
            widget.setStyleSheet('background-color:rgb(247,247,247)')
        self.layout.addWidget(widget)

    def remove_widget(self, widget):
        self.layout.removeWidget(widget)
        widget.setParent(None)
        self.revalidate_layout()

    def revalidate_layout(self):
        # Store references to the widgets
        widgets = [self.layout.itemAt(i).widget() for i in range(self.layout.count()) if
                   self.layout.itemAt(i) is not None]

        # Clear the layout
        self.clear_layout()

        # Add the widgets back to the layout
        for widget in widgets:
            self.add_widget(widget)

    def clear_layout(self):
        # Remove and delete all items from the layout
        while self.layout.count():
            self.layout.takeAt(0)
