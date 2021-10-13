from PyQt5 import QtWidgets
from design.ui_app_deny_abonement import Ui_AppDenyAbonement
from db_utils import db_connect
import db_sells
import sys


def get_orders_count(con):
    cur = con.cursor()
    cur.execute('SELECT * FROM Orders')
    rows = cur.fetchall()
    return len(rows)


class AppDenyAbonement(QtWidgets.QWidget):
    spin_box_value = 1

    def update(self):
        orders_count = get_orders_count(self.con)
        if orders_count > 0:
            self.ui.button.setEnabled(True)
        else:
            self.ui.button.setDisabled(True)
        self.ui.spinBox.setMaximum(orders_count)

    def spin_box_slot(self, value):
        self.spin_box_value = value

    def btn_slot(self):
        is_ok = True
        msg = ''
        (is_ok, msg) = db_sells.db_deny_abonement(self.con, self.spin_box_value)
        msgbox = QtWidgets.QMessageBox()
        if not is_ok:
            msgbox.setIcon(QtWidgets.QMessageBox.Critical)
            msgbox.setWindowTitle('Ошибка')
        else:
            msgbox.setIcon(QtWidgets.QMessageBox.Information)
            msgbox.setWindowTitle('Успех')
        msgbox.setText(msg)
        msgbox.exec()

    def __init__(self, con):
        super(AppDenyAbonement, self).__init__()
        self.ui = Ui_AppDenyAbonement()
        self.ui.setupUi(self)
        self.con = con
        self.ui.spinBox.setMinimum(1)
        self.update()
        self.ui.spinBox.valueChanged.connect(self.spin_box_slot)
        self.ui.button.clicked.connect(self.btn_slot)


if __name__ == '__main__':
    con = db_connect()
    app = QtWidgets.QApplication([])
    app.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
    application = AppDenyAbonement(con)
    application.show()

    sys.exit(app.exec())
