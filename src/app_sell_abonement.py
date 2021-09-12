from PyQt5 import QtCore, QtWidgets
from design.ui_app_sell_abonement import Ui_AppSellAbonement
import pymysql
import datetime
import db_sells
import sys


def select_abonements_rows():
    # Connect to the local MySQL 'Fitness' db
    con = pymysql.connect(host='127.0.0.1',
                          user='root',
                          password='gpnb0b',
                          db='Fitness',
                          charset='utf8mb4')

    with con:
        cur = con.cursor()
        cur.execute('SELECT AbonementId, RoomName, ServiceName, TimeName, AbonementPrice '
                    'FROM Abonements '
                    'INNER JOIN Rooms ON Rooms.RoomId = Abonements.RoomId '
                    'INNER JOIN Services ON Services.ServiceId = Abonements.ServiceId '
                    'INNER JOIN Times ON Times.TimeId = Abonements.TimeId '
                    'ORDER BY AbonementId')
        rows = cur.fetchall()
        return rows


class AppSellAbonement(QtWidgets.QWidget):
    abonements = select_abonements_rows()
    check_box_state = 0
    date = datetime.date.strftime(datetime.date.today() + datetime.timedelta(days=1), '%d.%m.%Y')
    spin_box_value = 1

    def fill_table(self):
        rownum = 0
        for row in self.abonements:
            colnum = 0
            for elem in row:
                cellinfo = QtWidgets.QTableWidgetItem(str(elem))
                cellinfo.setTextAlignment(QtCore.Qt.AlignCenter)
                # read only
                cellinfo.setFlags(
                    QtCore.Qt.ItemIsEnabled
                )
                self.ui.table.setItem(rownum, colnum, cellinfo)
                colnum += 1
            rownum += 1

    def check_box_slot(self, state):
        self.check_box_state = state
        if state > 0:
            self.ui.dateEdit.hide()
            self.ui.labelDate.hide()
        else:
            self.ui.dateEdit.show()
            self.ui.labelDate.show()

    def btn_slot(self):
        is_ok = True
        msg = ''
        if self.check_box_state > 0:
            (is_ok, msg) = db_sells.db_sell_oneday(self.spin_box_value)
        else:
            (is_ok, msg) = db_sells.db_sell_abonement(self.spin_box_value, self.date)
        if not is_ok:
            msgbox = QtWidgets.QMessageBox()
            msgbox.setIcon(QtWidgets.QMessageBox.Critical)
            msgbox.setWindowTitle('Ошибка')
            msgbox.setText(msg)
            msgbox.exec()
        else:
            msgbox = QtWidgets.QMessageBox()
            msgbox.setIcon(QtWidgets.QMessageBox.Information)
            msgbox.setWindowTitle('Успех')
            msgbox.setText(msg)
            msgbox.exec()

    def date_slot(self, qdate):
        self.date = '{:0>2}.{:0>2}.{}'.format(qdate.day(), qdate.month(), qdate.year())

    def spin_box_slot(self, value):
        self.spin_box_value = value

    def __init__(self):
        super(AppSellAbonement, self).__init__()
        self.ui = Ui_AppSellAbonement()
        self.ui.setupUi(self)
        size_policy = QtWidgets.QSizePolicy()
        size_policy.setRetainSizeWhenHidden(True)
        self.ui.labelDate.setSizePolicy(size_policy)
        self.ui.dateEdit.setSizePolicy(size_policy)
        self.ui.table.setRowCount(len(self.abonements))
        self.ui.table.setColumnCount(len(self.abonements[0]))
        self.ui.table.setHorizontalHeaderLabels(
            ['Id абонемента', 'Название зала', 'Название услуги', 'Время', 'Цена\nза день']
        )
        self.ui.table.verticalHeader().hide()
        self.fill_table()
        self.ui.table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.ui.table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self.ui.table.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.ui.table.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        self.ui.table.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
        self.ui.dateEdit.setDate(datetime.date.today() + datetime.timedelta(days=1))
        self.ui.dateEdit.setMinimumDate(datetime.date.today() + datetime.timedelta(days=1))
        self.ui.dateEdit.setCalendarPopup(True)
        self.ui.abonementIdSpinBox.setMinimum(1)
        self.ui.abonementIdSpinBox.setMaximum(len(self.abonements))
        self.ui.oneDayCheckBox.stateChanged.connect(self.check_box_slot)
        self.ui.abonementIdSpinBox.valueChanged.connect(self.spin_box_slot)
        self.ui.dateEdit.dateChanged.connect(self.date_slot)
        self.ui.sellButton.clicked.connect(self.btn_slot)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    app.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
    application = AppSellAbonement()
    application.show()

    sys.exit(app.exec())
