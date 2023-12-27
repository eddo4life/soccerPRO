from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QWidget, QTableWidget, QAbstractItemView, QHBoxLayout, QFormLayout, QLineEdit, QPushButton, \
    QTableWidgetItem, QMessageBox

from account.model.userprofilemodel import UserProfileModel


class Reload(QWidget):
    def __init__(self):
        super().__init__()
        self.hbLayout = QHBoxLayout()

        self.formulaire()
        self.tableview()
        self.setLayout(self.hbLayout)

    def formulaire(self):
        self.form = QFormLayout()
        self.account_id = QLineEdit()
        self.account_id.setPlaceholderText("ID")
        self.account_id.setDisabled(True)
        self.txt_nom = QLineEdit()
        self.txt_nom.setPlaceholderText("Nom")
        self.txt_nom.setDisabled(True)
        self.txt_prenom = QLineEdit()
        self.txt_prenom.setPlaceholderText("Prenom")
        self.txt_prenom.setDisabled(True)
        self.new_sold = QLineEdit()
        self.new_sold.setValidator(QDoubleValidator())
        self.new_sold.setPlaceholderText('Min(10)')

        self.bt_reload = QPushButton("Recharger")
        self.bt_reload.clicked.connect(self.reload)

        self.form.addRow("ID", self.account_id)
        self.form.addRow("Nom", self.txt_nom)
        self.form.addRow("Prenom", self.txt_prenom)
        self.form.addRow("Solde", self.new_sold)
        self.form.addRow("", self.bt_reload)

        self.hbLayout.addLayout(self.form)
        self.hbLayout.setStretchFactor(self.form, 1)

    def tableview(self):
        self.table = QTableWidget()
        self.table.clicked.connect(self.handle_table_click)
        # Set the table as not editable
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        header = ["ID", "PSEUDO", "NOM", "PRENOM", "SEXE", "TELEPHONE", "ADRESSE", "SOLDE", "ETAT"]
        self.table.setColumnCount(len(header))
        self.table.setAlternatingRowColors(True)
        self.table.setHorizontalHeaderLabels(header)
        self.table.verticalHeader().setVisible(False)
        self.hbLayout.addWidget(self.table)
        self.hbLayout.setStretchFactor(self.table, 3)
        self.load_data()

    def handle_table_click(self, item):
        selected_row = item.row()
        if selected_row >= 0:
            code = self.table.item(selected_row, 0)
            name = self.table.item(selected_row, 1)
            first_name = self.table.item(selected_row, 2)
            if code and name and first_name:
                self.account_id.setText(code.text())
                self.txt_nom.setText(name.text())
                self.txt_prenom.setText(first_name.text())

    def load_data(self):
        self.table.setRowCount(0)
        data = UserProfileModel.get_all()
        if data:
            for row_number, row_data in enumerate(data):
                self.table.insertRow(row_number)
                for column_number, column_data in enumerate(row_data):
                    item = QTableWidgetItem(str(column_data))
                    self.table.setItem(row_number, column_number, item)

    def reload(self):
        if self.account_id.text():
            sold = self.new_sold.text().strip()
            if sold:
                sold = float(sold)
                if sold >= 10:
                    UserProfileModel.update_sold(self.account_id.text(), sold)
                    self.load_data()
                    # clear the solde line edit
                    self.new_sold.setText('')

                else:
                    QMessageBox.warning(None, "Echec", 'Le montant doit etre >=10', QMessageBox.Ok)
            else:
                QMessageBox.warning(None, "Echec", 'Veuillez saisir un montant valide', QMessageBox.Ok)
        else:
            QMessageBox.warning(None, "Echec", 'Veuillez selectionner un utilisateur', QMessageBox.Ok)
