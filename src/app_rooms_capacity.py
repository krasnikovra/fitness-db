from PyQt5 import QtCore, QtWidgets
from design.ui_app_rooms_capacity import Ui_AppRoomsCapacity
import datetime
import db_rooms_queries
import sys


class AppRoomsCapacity(QtWidgets.QWidget):
    time_id = 1
    date = datetime.date.strftime(datetime.date.today(), '%d.%m.%Y')

    def update_table(self):
        self.ui.label.setText('Загруженность залов по состоянию на {} {}'.format(
            self.ui.timesComboBox.itemText(self.time_id - 1).lower(),
            self.date
        ))
        self.fill_table(db_rooms_queries.db_select_rooms_current_capacity(self.date, self.time_id))

    def update_table_from_combo_box(self, index):
        self.time_id = index + 1
        self.update_table()

    def update_table_from_date_entry(self, qdate):
        self.date = '{:0>2}.{:0>2}.{}'.format(qdate.day(), qdate.month(), qdate.year())
        self.update_table()

    def fill_table(self, rows):
        rownum = 0
        for row in rows:
            colnum = 0
            for i in range(2):
                cellinfo = QtWidgets.QTableWidgetItem(str(row[i]))
                cellinfo.setTextAlignment(QtCore.Qt.AlignCenter)
                # read only
                cellinfo.setFlags(
                    QtCore.Qt.ItemIsEnabled
                )
                self.ui.table.setItem(rownum, colnum, cellinfo)
                colnum += 1
            progress = QtWidgets.QProgressBar()
            progress.setMinimum(0)
            progress.setMaximum(row[2])
            progress.setValue(row[3])
            progress.setFormat('{}/{}'.format(row[3], row[2]))
            self.ui.table.setCellWidget(rownum, 2, progress)
            rownum += 1

    def __init__(self):
        super(AppRoomsCapacity, self).__init__()
        self.ui = Ui_AppRoomsCapacity()
        self.ui.setupUi(self)
        self.ui.timesComboBox.addItem('Утро')
        self.ui.timesComboBox.addItem('Вечер')
        self.ui.dateEdit.setDate(datetime.date.today())
        self.ui.dateEdit.setMinimumDate(datetime.date.today())
        self.ui.dateEdit.setCalendarPopup(True)
        self.ui.label.setText('Загруженность залов по состоянию на {} {}'.format(
            'утро',
            datetime.date.strftime(datetime.date.today(), '%d.%m.%Y')
        ))
        room_rows = db_rooms_queries.db_select_rooms_current_capacity(
            datetime.date.strftime(datetime.date.today(), '%d.%m.%Y'),
            1
        )
        self.ui.table.setRowCount(len(room_rows))
        self.ui.table.setColumnCount(len(room_rows[0]) - 1)
        self.ui.table.setHorizontalHeaderLabels(
            ['Id зала', 'Название зала', 'Свободно мест']
        )
        self.ui.table.verticalHeader().hide()
        self.ui.table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.ui.table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self.ui.table.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        self.ui.table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.fill_table(db_rooms_queries.db_select_rooms_current_capacity(
            self.date, self.time_id
        ))
        self.ui.timesComboBox.currentIndexChanged.connect(self.update_table_from_combo_box)
        self.ui.dateEdit.dateChanged.connect(self.update_table_from_date_entry)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    app.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
    application = AppRoomsCapacity()
    application.show()

    sys.exit(app.exec())

