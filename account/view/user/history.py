from PyQt5.QtWidgets import QTabWidget

from account.view.user.card import Card
from labs.lab import Lab


class HistoryTabs(QTabWidget):
    def __init__(self):
        super().__init__()
        self.addTab(self.pending(), Lab.get_icon('wait.png'), 'in progress')
        self.addTab(self.won(), Lab.get_icon('won.png'), 'won')

        self.addTab(self.lost(), Lab.get_icon('lose.png'), 'Lost')

    def pending(self):
        return Card('pending')

    def won(self):
        return Card('won')

    def lost(self):
        return Card('lost')
