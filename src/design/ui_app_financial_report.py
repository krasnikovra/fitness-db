# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design\ui_app_financial_report.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AppFinancialReport(object):
    def setupUi(self, AppFinancialReport):
        AppFinancialReport.setObjectName("AppFinancialReport")
        AppFinancialReport.resize(1200, 600)
        self.verticalLayoutWidget = QtWidgets.QWidget(AppFinancialReport)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(9, 160, 1181, 431))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.topLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.topLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.topLabel.setObjectName("topLabel")
        self.verticalLayout.addWidget(self.topLabel)
        self.tableWidget = QtWidgets.QTableWidget(self.verticalLayoutWidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget)
        self.summaryLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.summaryLabel.setFont(font)
        self.summaryLabel.setTextFormat(QtCore.Qt.AutoText)
        self.summaryLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.summaryLabel.setObjectName("summaryLabel")
        self.verticalLayout.addWidget(self.summaryLabel)
        self.gridLayoutWidget = QtWidgets.QWidget(AppFinancialReport)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(419, 10, 361, 141))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.radioButtonDay = QtWidgets.QRadioButton(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.radioButtonDay.sizePolicy().hasHeightForWidth())
        self.radioButtonDay.setSizePolicy(sizePolicy)
        self.radioButtonDay.setObjectName("radioButtonDay")
        self.gridLayout.addWidget(self.radioButtonDay, 0, 1, 1, 1)
        self.getReportLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.getReportLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.getReportLabel.setObjectName("getReportLabel")
        self.gridLayout.addWidget(self.getReportLabel, 0, 0, 1, 1)
        self.radioButtonMonth = QtWidgets.QRadioButton(self.gridLayoutWidget)
        self.radioButtonMonth.setObjectName("radioButtonMonth")
        self.gridLayout.addWidget(self.radioButtonMonth, 1, 1, 1, 1)
        self.radioButtonYear = QtWidgets.QRadioButton(self.gridLayoutWidget)
        self.radioButtonYear.setObjectName("radioButtonYear")
        self.gridLayout.addWidget(self.radioButtonYear, 2, 1, 1, 1)
        self.dateEdit = QtWidgets.QDateEdit(self.gridLayoutWidget)
        self.dateEdit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.dateEdit.setObjectName("dateEdit")
        self.gridLayout.addWidget(self.dateEdit, 3, 0, 1, 1)
        self.getReportButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.getReportButton.setObjectName("getReportButton")
        self.gridLayout.addWidget(self.getReportButton, 3, 1, 1, 1)

        self.retranslateUi(AppFinancialReport)
        QtCore.QMetaObject.connectSlotsByName(AppFinancialReport)

    def retranslateUi(self, AppFinancialReport):
        _translate = QtCore.QCoreApplication.translate
        AppFinancialReport.setWindowTitle(_translate("AppFinancialReport", "Финансовый отчет"))
        self.topLabel.setText(_translate("AppFinancialReport", "Финансовый отчет"))
        self.summaryLabel.setText(_translate("AppFinancialReport", "<b>Итого:</b> "))
        self.radioButtonDay.setText(_translate("AppFinancialReport", "День"))
        self.getReportLabel.setText(_translate("AppFinancialReport", "Получить отчет за: "))
        self.radioButtonMonth.setText(_translate("AppFinancialReport", "Месяц"))
        self.radioButtonYear.setText(_translate("AppFinancialReport", "Год"))
        self.getReportButton.setText(_translate("AppFinancialReport", "Получить отчет"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AppFinancialReport = QtWidgets.QWidget()
    ui = Ui_AppFinancialReport()
    ui.setupUi(AppFinancialReport)
    AppFinancialReport.show()
    sys.exit(app.exec_())
