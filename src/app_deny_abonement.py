from PyQt5 import QtWidgets
from design.ui_app_deny_abonement import Ui_AppDenyAbonement
import pymysql
import db_sells
import sys


def get_orders_count():
    # Connect to the local MySQL 'Fitness' db
    con = pymysql.connect(host='127.0.0.1',
                          user='root',
                          password='gpnb0b',
                          db='Fitness',
                          charset='utf8mb4')

    with con:
        cur = con.cursor()
        cur.execute('SELECT * FROM Orders')
        rows = cur.fetchall()
        return len(rows)


class AppDenyAbonement(QtWidgets.QWidget):
    spin_box_value = 1

    def spin_box_slot(self, value):
        self.spin_box_value = value

    def btn_slot(self):
        is_ok = True
        msg = ''
        (is_ok, msg) = db_sells.db_deny_abonement(self.spin_box_value)
        msgbox = QtWidgets.QMessageBox()
        if not is_ok:
            msgbox.setIcon(QtWidgets.QMessageBox.Critical)
            msgbox.setWindowTitle('Ошибка')
        else:
            msgbox.setIcon(QtWidgets.QMessageBox.Information)
            msgbox.setWindowTitle('Успех')
        msgbox.setText(msg)
        msgbox.exec()

    def __init__(self):
        super(AppDenyAbonement, self).__init__()
        self.ui = Ui_AppDenyAbonement()
        self.ui.setupUi(self)
        self.ui.spinBox.setMinimum(1)
        self.ui.spinBox.setMaximum(get_orders_count())
        self.ui.spinBox.valueChanged.connect(self.spin_box_slot)
        self.ui.button.clicked.connect(self.btn_slot)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    app.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
    application = AppDenyAbonement()
    application.show()

    sys.exit(app.exec())
