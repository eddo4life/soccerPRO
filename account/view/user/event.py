from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QPushButton, QLineEdit
from PyQt5.QtWidgets import QWidget, QCheckBox, QLabel, QVBoxLayout, QHBoxLayout

from account.model.usereventmodel import UserEventModel
from account.view.user.basewidget import BaseWidget


def unselect_checkbox(widget, target_text='placer'):
    layout = widget.layout()
    for i in range(layout.count()):
        try:
            item = layout.itemAt(i)
            if isinstance(item.widget(), QCheckBox) and item.widget().text().lower() == target_text.lower():
                item.widget().setChecked(False)
        except Exception as e:
            print(f"An exception occurred: {str(e)}")


class Event(BaseWidget):
    def __init__(self):
        super().__init__()

        for d in UserEventModel.load():
            self.add_widget(self.card(d))

        # add both event and ticket horizontally to the main layout

        main_layout = QHBoxLayout(self)
        main_layout.addWidget(self.scroll_area)

        main_layout.setStretchFactor(self.scroll_area, 2)  # give more space to the events

        # manage ticket class

        self.ticket = Ticket()
        # add action for clearing the ticket
        self.ticket.clear_btn.clicked.connect(self.clear_ticket)

        # create a main layout for tickets
        main_layout_ticket = QVBoxLayout()
        main_layout_ticket.addWidget(self.ticket.scroll_area)
        main_layout_ticket.addLayout(self.ticket.add_buttons())
        # create a main widget for tickets
        ticket_widgets = QWidget()
        ticket_widgets.setLayout(main_layout_ticket)
        main_layout.addWidget(ticket_widgets)
        main_layout.setStretchFactor(ticket_widgets, 1)

        self.setLayout(main_layout)

    def card(self, dic):
        wdg = QWidget()
        wdg.setFixedHeight(150)
        top = dic['equipe_receveuse'] + " - " + dic['equipe_visiteuse'] + "(" + dic['heure_match'] + ")"
        middle = dic['pays'] + " - " + dic['type_de_match']
        bottom = dic['score_final'] + " - " + dic['score_final']
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

    def clear_ticket(self):
        # Remove and delete all items from the layout
        layout = self.ticket.layout
        while layout.count():
            widget = layout.takeAt(0).widget()
            if widget is not None:
                # search for the checkbox and unselect it
                unselect_checkbox(widget)
                self.add_widget(widget)


class Ticket(BaseWidget):
    def __init__(self):
        super().__init__()
        self.clear_btn = QPushButton('clear')

    def add_buttons(self):
        sold_input = QLineEdit()
        validator = QDoubleValidator()
        sold_input.setValidator(validator)
        sold_input.setPlaceholderText('sold')
        validate_btn = QPushButton('validate')
        # add components to the layout
        hbox = QHBoxLayout()
        hbox.addWidget(self.clear_btn)
        hbox.addWidget(sold_input)
        hbox.addWidget(validate_btn)
        # add actions
        validate_btn.clicked.connect(self.validate)
        return hbox

    def validate(self):
        print('validating')
