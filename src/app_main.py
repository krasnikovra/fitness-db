from PyQt5 import QtCore, QtWidgets
from design.ui_app_main import Ui_AppMain
from app_sell_abonement import AppSellAbonement
from app_deny_abonement import AppDenyAbonement
from app_rooms_capacity import AppRoomsCapacity
from app_financial_report import AppFinancialReport
import sys


class AppMain(QtWidgets.QMainWindow):
    app_sell_abonement = None
    app_deny_abonement = None
    app_rooms_capacity = None
    app_financial_report = None

    def app_sell_abonement_btn_slot(self):
        self.app_sell_abonement.show()

    def app_deny_abonement_btn_slot(self):
        self.app_deny_abonement.show()

    def app_rooms_capacity_btn_slot(self):
        self.app_rooms_capacity.show()

    def app_financial_report_btn_slot(self):
        self.app_financial_report.show()

    def __init__(self):
        super(AppMain, self).__init__()
        self.ui = Ui_AppMain()
        self.ui.setupUi(self)
        self.app_sell_abonement = AppSellAbonement()
        self.app_deny_abonement = AppDenyAbonement()
        self.app_rooms_capacity = AppRoomsCapacity()
        self.app_financial_report = AppFinancialReport()
        self.ui.appSellAbonementButton.clicked.connect(self.app_sell_abonement_btn_slot)
        self.ui.appDenyAbonementButton.clicked.connect(self.app_deny_abonement_btn_slot)
        self.ui.appRoomsCapacityButton.clicked.connect(self.app_rooms_capacity_btn_slot)
        self.ui.appFinancialReportButton.clicked.connect(self.app_financial_report_btn_slot)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    app.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
    application = AppMain()
    application.show()

    sys.exit(app.exec())
