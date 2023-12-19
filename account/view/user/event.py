from PyQt5.QtWidgets import QPushButton, QLineEdit
from PyQt5.QtWidgets import QWidget, QCheckBox, QLabel, QVBoxLayout, QScrollArea, QHBoxLayout

from account.view.user.basewidget import BaseWidget


class Event(BaseWidget):
    def __init__(self):
        super().__init__(QVBoxLayout())

        dct = {
            'home-team': 'Barcelona',
            'away-team': 'Real Madrid',
            'time': '12:30',
            'country': 'Spain',
            'championship': 'LaLiga',
            'score 1': '0',
            'score 2': '0'
        }

        for i in range(100):
            self.add_widget(self.card(dct))

        # scroll area for events
        scroll_area_event = QScrollArea()
        scroll_area_event.setWidgetResizable(True)

        scroll_widget_event = QWidget()
        scroll_widget_event.setLayout(self.layout)

        scroll_area_event.setWidget(scroll_widget_event)

        # create instance for ticket
        self.ticket = Ticket()

        # scroll area for ticket
        scroll_area_ticket = QScrollArea()
        scroll_area_ticket.setWidgetResizable(True)

        scroll_widget_ticket = QWidget()
        scroll_widget_ticket.setLayout(self.ticket.layout)

        scroll_area_ticket.setWidget(scroll_widget_ticket)
        # add both event and ticket horizontally to the main layout
        main_layout = QHBoxLayout(self)
        main_layout.addWidget(scroll_area_event)
        main_layout.addWidget(scroll_area_ticket)
        main_layout.setStretchFactor(scroll_area_event, 2)  # give more space to the events

        # create a main layout for tickets
        main_layout.setStretchFactor(scroll_area_ticket, 1)

        self.setLayout(main_layout)

    def card(self, dic):
        wdg = QWidget()
        wdg.setFixedHeight(150)
        top = dic['home-team'] + " - " + dic['away-team'] + "(" + dic['time'] + ")"
        middle = dic['country'] + " - " + dic['championship']
        bottom = dic['score 1'] + " - " + dic['score 2']
        vbox = QVBoxLayout()
        vbox.addWidget(QLabel(top))
        vbox.addWidget(QLabel(middle))
        vbox.addWidget(QLabel(bottom))
        # add unique checkbox to select a specific match
        chb = QCheckBox('Placer')
        vbox.addWidget(chb)
        wdg.setLayout(vbox)
        chb.clicked.connect(lambda: self.add_remove(chb, wdg))

        return wdg

    def add_remove(self, chb, card):

        if chb.isChecked():
            self.remove_widget(card)  # remove from the event list
            self.ticket.add_widget(card)  # add to the ticket
        else:
            self.ticket.remove_widget(card)  # remove from the ticket list
            self.add_widget(card)  # add to the event list


class Ticket(BaseWidget):
    def __init__(self):
        super().__init__(QVBoxLayout())


    def add_buttons(self):
        clear_btn = QPushButton('clear')
        sold_input = QLineEdit()
        sold_input.setPlaceholderText('sold')
        validate_btn = QPushButton('validate')

        hbox = QHBoxLayout()
        hbox.addWidget(clear_btn)
        hbox.addWidget(sold_input)
        hbox.addWidget(validate_btn)

        return hbox

    def clear_ticket(self):
        self.clear_layout()
