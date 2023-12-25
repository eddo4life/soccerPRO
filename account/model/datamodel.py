
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import QObject, pyqtSignal

class DataModel(QObject):
    dataChanged = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._data = None

    def set_data(self, data):
        self._data = data
        self.dataChanged.emit()

    def get_data(self):
        return self._data

class CustomWidget(QWidget):
    def __init__(self, data_model, parent=None):
        super().__init__(parent)
        self.data_model = data_model

        layout = QVBoxLayout(self)
        self.label = QLabel(self)
        layout.addWidget(self.label)

        # Connect the signal to the slot
        data_model.dataChanged.connect(self.update_ui)

    def update_ui(self):
        data = self.data_model.get_data()
        if data is not None:
            self.label.setText(str(data))


# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#
#         self.data_model = DataModel()
#
#         self.stack_widget = QStackedWidget(self)
#         widget1 = CustomWidget(self.data_model)
#         widget2 = CustomWidget(self.data_model)
#         self.stack_widget.addWidget(widget1)
#         self.stack_widget.addWidget(widget2)
#
#         self.setCentralWidget(self.stack_widget)
#
#         # Example: Changing data and switching widgets
#         self.data_model.set_data("Initial Data")
#         self.stack_widget.setCurrentIndex(1)  # Switch to the second widget
#
# if __name__ == '__main__':
#     app = QApplication([])
#     window = MainWindow()
#     window.show()
#     app.exec_()
