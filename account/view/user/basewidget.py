from PyQt5.QtWidgets import QWidget


class BaseWidget(QWidget):
    def __init__(self, layout):
        super().__init__()
        self.layout = layout

    def add_widget(self, widget):
        if self.layout.count() % 2 == 0:
            widget.setStyleSheet('background-color:rgb(250,250,250)')
        else:
            widget.setStyleSheet('background-color:rgb(240,240,240)')
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
        # Remove all items from the layout
        while self.layout.count():
            self.layout.takeAt(0)
