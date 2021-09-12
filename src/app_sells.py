from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import scrolledtext
from tkcalendar import DateEntry
from db_sells import *


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
        res = 'Id абонемента - Название зала - Название услуги - Утро/Вечер - Цена за день\n'
        res += '-----------------------------------------------------------------------------\n'
        for row in rows:
            for i in range(len(row) - 1):
                res += str(row[i]) + ' - '
            res += str(row[len(row) - 1]) + ' р./день\n'
        return res


# Main functiom
def app_sells():
    window = Tk()
    window.title('Продажа')
    window.geometry('800x400')
    label_sell_oneday = Label(window, text='Id абонемента')
    entry_abonement_id = Entry(window, width=5)

    date_label = ttk.Label(window, text='Дата окончания')
    date_entry = DateEntry(window, width=12, background='darkblue',
                           foreground='white', borderwidth=2,
                           date_pattern='dd.mm.YYYY')

    def btn_sell_oneday_onclick():
        try:
            is_ok = True
            msg = ''
            (is_ok, msg) = db_sell_oneday(int(entry_abonement_id.get()))
        except ValueError as err:
            messagebox.showerror(title='Ошибка', message='Некорректный ввод')
            return

        if not is_ok:
            messagebox.showerror(title='Ошибка', message=msg)
        else:
            messagebox.showinfo(title='Успех', message=msg)

    btn_sell_oneday = Button(window, text='Продать разовое посещение',
                             command=btn_sell_oneday_onclick,
                             width=25, height=1)

    def btn_sell_abonement_onclick():
        try:
            is_ok = True
            msg = ''
            (is_ok, msg) = db_sell_abonement(int(entry_abonement_id.get()),
                                             datetime.date.strftime(date_entry.get_date(), '%d.%m.%Y'))
        except ValueError as err:
            messagebox.showerror(title='Ошибка', message='Некорректный ввод')
            return

        if not is_ok:
            messagebox.showerror(title='Ошибка', message=msg)
        else:
            messagebox.showinfo(title='Успех', message=msg)

    btn_sell_abonement = Button(window, text='Продать абонемент',
                                command=btn_sell_abonement_onclick,
                                width=25, height=1)

    scrolled_text = scrolledtext.ScrolledText(window, width=90, height=17)
    scrolled_text.insert(INSERT, select_abonements_rows())

    entry_abonement_id.grid(row=0, column=1, sticky=W, padx=10, pady=10)
    label_sell_oneday.grid(row=0, column=0, sticky=E, padx=10, pady=10)
    btn_sell_oneday.grid(row=0, column=2, sticky=W, padx=10, pady=10)
    date_label.grid(row=1, column=0, sticky=E, padx=10, pady=10)
    date_entry.grid(row=1, column=1, sticky=W, padx=10, pady=10)
    btn_sell_abonement.grid(row=1, column=2, sticky=W, padx=10, pady=10)
    scrolled_text.grid(row=2, column=0, sticky=W+E+S, columnspan=3, padx=20, pady=10)
    window.mainloop()


if __name__ == '__main__':
    app_sells()
