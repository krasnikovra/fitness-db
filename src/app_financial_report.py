from PyQt5 import QtWidgets, QtCore
from design.ui_app_financial_report import Ui_AppFinancialReport
from db_utils import db_connect
import db_financies
import datetime
import sys


class AppFinancialReport(QtWidgets.QWidget):
    radio_btn_checked = 'day'
    date = datetime.date.strftime(datetime.date.today(), "%d.%m.%Y")

    def radio_btn_day_slot(self, value):
        self.ui.radioButtonDay.setChecked(value)
        if value:
            self.radio_btn_checked = 'day'
            self.ui.dateEdit.setDisplayFormat("dd.MM.yyyy")

    def radio_btn_month_slot(self, value):
        self.ui.radioButtonMonth.setChecked(value)
        if value:
            self.radio_btn_checked = 'month'
            self.ui.dateEdit.setDisplayFormat("MM.yyyy")

    def radio_btn_year_slot(self, value):
        self.ui.radioButtonYear.setChecked(value)
        if value:
            self.radio_btn_checked = 'year'
            self.ui.dateEdit.setDisplayFormat("yyyy")

    def dateedit_slot(self, qdate):
        self.date = '{:0>2}.{:0>2}.{}'.format(qdate.day(), qdate.month(), qdate.year())

    def fill_table(self, rows):
        if len(rows) == 0:
            self.ui.tableWidget.setRowCount(0)
            return
        self.ui.tableWidget.setRowCount(len(rows))
        rownum = 0
        for row in rows:
            colnum = 0
            for elem in row:
                cellinfo = QtWidgets.QTableWidgetItem(str(elem))
                cellinfo.setTextAlignment(QtCore.Qt.AlignCenter)
                # read only
                cellinfo.setFlags(
                    QtCore.Qt.ItemIsEnabled
                )
                self.ui.tableWidget.setItem(rownum, colnum, cellinfo)
                colnum += 1
            rownum += 1
        self.ui.tableWidget.update()

    def fill_report(self):
        rows = ''
        if self.radio_btn_checked == 'day':
            rows = db_financies.db_financies_day(self.con, self.date)
        elif self.radio_btn_checked == 'month':
            rows = db_financies.db_financies_month(self.con, self.date)
        elif self.radio_btn_checked == 'year':
            rows = db_financies.db_financies_year(self.con, self.date)
        self.fill_table(rows)
        # calculating sum
        sum = 0
        for row in rows:
            sum += row[-1]
        self.ui.summaryLabel.setText('<b>Итого: {}</b>'.format(sum))
        if self.radio_btn_checked == 'day':
            self.ui.topLabel.setText('Финансовый отчет на {}'.format(self.date))
        elif self.radio_btn_checked == 'month':
            self.ui.topLabel.setText('Финансовый отчет на {}'.format(self.date[3:]))
        else:
            self.ui.topLabel.setText('Финансовый отчет на {}'.format(self.date[6:]))
        if self.ui.topLabel.isHidden():
            self.ui.topLabel.show()

    def btn_slot(self):
        self.fill_report()

    def __init__(self, con):
        super(AppFinancialReport, self).__init__()
        self.ui = Ui_AppFinancialReport()
        self.ui.setupUi(self)
        self.con = con
        self.ui.radioButtonDay.setChecked(True)
        self.ui.radioButtonDay.clicked.connect(self.radio_btn_day_slot)
        self.ui.radioButtonMonth.clicked.connect(self.radio_btn_month_slot)
        self.ui.radioButtonYear.clicked.connect(self.radio_btn_year_slot)
        self.ui.dateEdit.setMinimumDate(datetime.date(2010, 1, 1))
        self.ui.dateEdit.setDate(datetime.date.today())
        self.ui.dateEdit.setMaximumDate(datetime.date.today())
        self.ui.dateEdit.dateChanged.connect(self.dateedit_slot)
        self.ui.getReportButton.clicked.connect(self.btn_slot)
        columns = ['Id заказа', 'Id абонемента', 'Название зала', 'Название услуги',
                   'Время', 'Дата покупки', 'Количество дней', 'Стоимость']
        self.ui.tableWidget.setColumnCount(len(columns))
        self.ui.tableWidget.setHorizontalHeaderLabels(columns)
        self.ui.tableWidget.verticalHeader().hide()
        for i in range(len(columns)):
            self.ui.tableWidget.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(len(columns) - 1, QtWidgets.QHeaderView.Stretch)


if __name__ == '__main__':
    con = db_connect()
    app = QtWidgets.QApplication([])
    app.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
    application = AppFinancialReport(con)
    application.show()

    sys.exit(app.exec())
