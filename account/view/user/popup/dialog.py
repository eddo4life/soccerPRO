from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel


class MyDialog(QDialog):
    def __init__(self, card=None, title=None):
        super().__init__()

        self.setWindowTitle(title)

        # Set up layout
        layout = QVBoxLayout()

        # Create widgets
        if title.startswith('Fond'):
            label = QLabel('<h2>' + title + '</h2>')
            layout.addWidget(label)

        else:
            card.setEnabled(False)
            layout.addWidget(card)

        # Set the layout for the dialog
        self.setLayout(layout)

        self.setModal(True)
        self.show()

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#
#     # Create an instance of the QDialog class
#     dialog = MyDialog(title='Fond insuffisant')
#
#     sys.exit(app.exec_())
