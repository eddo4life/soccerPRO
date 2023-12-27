from PyQt5.QtWidgets import QTabWidget

from account.view.user.card import Card
from labs.lab import Lab


class HistoryTabs(QTabWidget):
    def __init__(self):
        super().__init__()

        # Add tabs for pending, won, and lost history
        self.addTab(self.pending(), Lab.get_icon('wait.png'), 'In Progress')
        self.addTab(self.won(), Lab.get_icon('won.png'), 'Won')
        self.addTab(self.lost(), Lab.get_icon('lose.png'), 'Lost')

    def pending(self):
        # Create a Card widget for pending history
        return Card('pending')

    def won(self):
        # Create a Card widget for won history
        return Card('won')

    def lost(self):
        # Create a Card widget for lost history
        return Card('lost')
