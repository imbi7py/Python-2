import sys
from PyQt5 import QtCore, QtWidgets, QtSql


class CrudDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(CrudDialog, self).__init__(parent)

        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('films.db')

        self.view = QtWidgets.QTableView()
        self.view.setToolTip("Change the fields")
        self.view.setWindowTitle("Table Model")

        btn_add = QtWidgets.QPushButton("Add a row")
        btn_add.clicked.connect(self.add_row)

        btn_del = QtWidgets.QPushButton("Delete a row")
        btn_del.clicked.connect(self.remove_row)

        lay = QtWidgets.QVBoxLayout(self)
        lay.addWidget(self.view)
        lay.addWidget(btn_add)
        lay.addWidget(btn_del)

        self.model = QtSql.QSqlTableModel()
        self.model.setTable('genres')
        self.model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
        self.model.select()
        self.model.setHeaderData(0, QtCore.Qt.Horizontal, "ИД")
        self.model.setHeaderData(1, QtCore.Qt.Horizontal, "Жанр")
        self.view.setModel(self.model)
        self.resize(1100, 600)

    @QtCore.pyqtSlot()
    def add_row(self):
        self.model.insertRows(self.model.rowCount(), 1)

    @QtCore.pyqtSlot()
    def remove_row(self):
        self.model.removeRow(self.view.currentIndex().row())
        self.model.select()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    button = QtWidgets.QPushButton("Show")
    c = CrudDialog()
    button.clicked.connect(c.exec_)
    button.show()
    sys.exit(app.exec_())