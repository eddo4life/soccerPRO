from PyQt5.QtWidgets import QWidget, QTableWidget, QAbstractItemView, QHBoxLayout, QFormLayout, QLineEdit, QPushButton, \
    QTableWidgetItem

from account.model.userprofilemodel import UserProfileModel


class Reload(QWidget):
    def __init__(self):
        super().__init__()
        self.hbLayout = QHBoxLayout()
        self.formulaire()
        self.tableview()
        self.setLayout(self.hbLayout)
        self.load()

    def formulaire(self):
        self.form = QFormLayout()
        self.txt_id = QLineEdit()
        self.txt_id.setPlaceholderText("ID")
        self.txt_id.setDisabled(True)
        self.txt_nom = QLineEdit()
        self.txt_nom.setPlaceholderText("Nom")
        self.txt_nom.setDisabled(True)
        self.txt_prenom = QLineEdit()
        self.txt_prenom.setPlaceholderText("Prenom")
        self.txt_prenom.setDisabled(True)
        self.new_sold = QLineEdit()

        self.bt_reload = QPushButton("Recharger")
        self.bt_reload.clicked.connect(self.reload)

        self.form.addRow("ID", self.txt_id)
        self.form.addRow("Nom", self.txt_nom)
        self.form.addRow("Prenom", self.txt_prenom)
        self.form.addRow("Solde", self.new_sold)
        self.form.addRow("", self.bt_reload)

        self.hbLayout.addLayout(self.form)
        self.hbLayout.setStretchFactor(self.form,1)


    def tableview(self):

        self.table = QTableWidget()
        self.table.clicked.connect(self.handle_table_click)
        # Set the table as not editable
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # definir le nombre de ligne et de colonne
        header = ["ID", "PSEUDO", "NOM", "PRENOM", "SEXE", "TELEPHONE", "ADRESSE", "SOLDE", "ETAT"]
        self.table.setColumnCount(len(header))
        self.table.setRowCount(0)
        self.table.setAlternatingRowColors(True)
        self.table.setHorizontalHeaderLabels(header)
        # ajouter le tableau dans le hbLayout
        self.hbLayout.addWidget(self.table)
        self.hbLayout.setStretchFactor(self.table, 3)

    def handle_table_click(self, item):
        selected_row = item.row()
        if selected_row >= 0:
            code = self.table.item(selected_row, 0)
            name = self.table.item(selected_row, 1)
            first_name = self.table.item(selected_row, 2)
            if code and name and first_name:
                self.txt_id.setText(code.text())
                self.txt_nom.setText(name.text())
                self.txt_prenom.setText(first_name.text())

    def load(self):
        data = UserProfileModel().get_all()
        if data:
            for row_number, row_data in enumerate(data):
                self.table.insertRow(row_number)
                for column_number, column_data in enumerate(row_data):
                    item = QTableWidgetItem(str(column_data))
                    self.table.setItem(row_number, column_number, item)
        else:
            print('no data')

    def reload(self):
        print('reloading')
