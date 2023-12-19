from PyQt5.QtWidgets import QLabel, QTabWidget


class HistoryTabs(QTabWidget):
    def __init__(self):
        super().__init__()
        tw = QTabWidget()
        self.addTab(self.pending(), 'in progress')
        self.addTab(self.win(), 'won')
        self.addTab(self.lose(), 'Lost')

    def pending(self):
        return QLabel('pending')

    def win(self):
        return QLabel('won')

    def lose(self):
        return QLabel('Lost')
