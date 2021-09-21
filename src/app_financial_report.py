from PyQt5 import QtWidgets, QtCore
from design.ui_app_financial_report import Ui_AppFinancialReport
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
        if self.radio_btn_checked == 'day':
            self.date = '{:0>2}.{:0>2}.{}'.format(qdate.day(), qdate.month(), qdate.year())
        elif self.radio_btn_checked == 'month':
            self.date = '{:0>2}.{}'.format(qdate.month(), qdate.year())
        else:
            self.date = '{}'.format(qdate.year())

    # TODO: fix refill debug
    def fill_table(self, rows):
        if len(rows) == 0:
            self.ui.tableWidget.setRowCount(0)
            return
        self.ui.tableWidget.setRowCount(len(rows))
        self.ui.tableWidget.setColumnCount(len(rows[0]) if len(rows[0]) > 0 else 0)
        self.ui.tableWidget.setHorizontalHeaderLabels(
            ['Id заказа', 'Id абонемента', 'Название зала', 'Название услуги',
             'Дата покупки', 'Время', 'Количество дней', 'Стоимость']
        )
        self.ui.tableWidget.verticalHeader().hide()
        for i in range(len(rows[0])):
            self.ui.tableWidget.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(len(rows[0]) - 1, QtWidgets.QHeaderView.Stretch)
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

    def fill_report(self, date, radio_btn_checked):
        rows = ''
        if radio_btn_checked == 'day':
            rows = db_financies.db_financies_day(date)
        elif radio_btn_checked == 'month':
            rows = db_financies.db_financies_month(date)
        elif radio_btn_checked == 'year':
            rows = db_financies.db_financies_year(date)
        self.fill_table(rows)
        # calculating sum
        sum = 0
        for row in rows:
            sum += row[-1]
        self.ui.summaryLabel.setText('<b>Итого: {}</b>'.format(sum))
        self.ui.topLabel.setText('Финансовый отчет на {}'.format(date))

    def btn_slot(self):
        self.fill_report(self.date, self.radio_btn_checked)

    def __init__(self):
        super(AppFinancialReport, self).__init__()
        self.ui = Ui_AppFinancialReport()
        self.ui.setupUi(self)
        size_policy = QtWidgets.QSizePolicy()
        size_policy.setRetainSizeWhenHidden(True)
        self.ui.topLabel.setSizePolicy(size_policy)
        self.ui.topLabel.hide()
        self.ui.radioButtonDay.setChecked(True)
        self.ui.radioButtonDay.clicked.connect(self.radio_btn_day_slot)
        self.ui.radioButtonMonth.clicked.connect(self.radio_btn_month_slot)
        self.ui.radioButtonYear.clicked.connect(self.radio_btn_year_slot)
        self.ui.dateEdit.setMinimumDate(datetime.date(2010, 1, 1))
        self.ui.dateEdit.setMaximumDate(datetime.date.today())
        self.ui.dateEdit.dateChanged.connect(self.dateedit_slot)
        self.ui.getReportButton.clicked.connect(self.btn_slot)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    app.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
    application = AppFinancialReport()
    application.show()

    sys.exit(app.exec())
