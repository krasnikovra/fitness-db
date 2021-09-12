import pymysql
import datetime


# Sell an abonement; date_end in format dd.mm.yyyy
# Returns '' if ok and error message if error has occurred
def db_sell_abonement(abonement_id, date_end):
    # Connect to the local MySQL 'Fitness' db
    con = pymysql.connect(host='127.0.0.1',
                          user='root',
                          password='gpnb0b',
                          db='Fitness',
                          charset='utf8mb4',
                          cursorclass=pymysql.cursors.DictCursor)

    with con:
        cur = con.cursor()
        # We need to check if there is such abonement_id
        cur.execute('SELECT * FROM Abonements WHERE AbonementId = {}'.format(abonement_id))
        temp = cur.fetchall()
        if len(temp) == 0:
            return (False, 'Нет абонемента с указанным Id!')
        # Also we need to check if the date is not from the past
        if datetime.datetime.strptime(date_end, "%d.%m.%Y").date() < datetime.date.today():
            return (False, 'Указана неверная дата, невозможно продать абонемент в прошлое!')
        # Check for free spaces in room
        cur.execute('SELECT * FROM Abonements WHERE AbonementId = {}'.format(abonement_id))
        abonement = cur.fetchone()
        cur.execute('SELECT COUNT(*) '
                    'FROM Orders '
                    'INNER JOIN Abonements on Abonements.AbonementId = Orders.AbonementId '
                    'INNER JOIN Rooms on Rooms.RoomId = Abonements.RoomId '
                    'INNER JOIN Services on Services.ServiceId = Abonements.ServiceId '
                    'INNER JOIN Times on Times.TimeId = Abonements.TimeId '
                    'WHERE Rooms.RoomId = {} AND Times.TimeId = {} AND STR_TO_DATE("{}", "%d.%m.%Y") BETWEEN '
                    'OrderDateStart AND OrderDateEnd'.format(abonement['RoomId'],
                                                             abonement['TimeId'],
                                                             datetime.date.strftime(datetime.date.today(),
                                                                                        '%d.%m.%Y')))
        room_curcapacity = cur.fetchone()
        cur.execute('SELECT RoomCapacity, RoomName, Times.TimeName '
                    'FROM Abonements '
                    'INNER JOIN Rooms ON Rooms.RoomId = Abonements.RoomId '
                    'INNER JOIN Times ON Times.TimeId = Abonements.TimeId '
                    'WHERE AbonementId = {}'.format(abonement_id))
        room = cur.fetchone()
        if room['RoomCapacity'] <= room_curcapacity['COUNT(*)']:
            return (False, 'Мест в зале "{}" на {} не осталось!'.format(room['RoomName'],
                                                                        room['TimeName'].lower()))
        # After checking, we need to insert new order row
        cur.execute('INSERT INTO Orders (AbonementId, OrderDateStart, OrderDateEnd) '
                    'VALUES ({}, CURDATE(), STR_TO_DATE("{}", "%d.%m.%Y"))'.format(abonement_id,
                                                                                     date_end))
        con.commit()
        # Collect information about sold abonement
        cur.execute('SELECT RoomName, ServiceName, TimeName, AbonementPrice '
                    'FROM Abonements '
                    'INNER JOIN Rooms on Rooms.RoomId = Abonements.RoomId '
                    'INNER JOIN Services on Services.ServiceId = Abonements.ServiceId '
                    'INNER JOIN Times on Times.TimeId = Abonements.TimeId '
                    'WHERE AbonementId = {}'.format(abonement_id))
        row = cur.fetchone()
        days = (datetime.datetime.strptime(date_end, "%d.%m.%Y").date() - datetime.date.today()).days + 1
        return (True, 'Абонемент "{} - {} - {}" на сумму {} рублей на {} дней успешно продан'.format(
            row['RoomName'], row['ServiceName'], row['TimeName'], row['AbonementPrice'] * days, days))


def db_sell_oneday(abonement_id):
    # Connect to the local MySQL 'Fitness' db
    con = pymysql.connect(host='127.0.0.1',
                          user='root',
                          password='gpnb0b',
                          db='Fitness',
                          charset='utf8mb4',
                          cursorclass=pymysql.cursors.DictCursor)

    with con:
        cur = con.cursor()
        # We need to check if there is such abonement_id
        cur.execute('SELECT * FROM Abonements WHERE AbonementId = {}'.format(abonement_id))
        temp = cur.fetchall()
        if len(temp) == 0:
            return (False, 'Нет абонемента с указанным Id!')
        # Check for free spaces in room
        cur.execute('SELECT * FROM Abonements WHERE AbonementId = {}'.format(abonement_id))
        abonement = cur.fetchone()
        cur.execute('SELECT COUNT(*) '
                    'FROM Orders '
                    'INNER JOIN Abonements on Abonements.AbonementId = Orders.AbonementId '
                    'INNER JOIN Rooms on Rooms.RoomId = Abonements.RoomId '
                    'INNER JOIN Services on Services.ServiceId = Abonements.ServiceId '
                    'INNER JOIN Times on Times.TimeId = Abonements.TimeId '
                    'WHERE Rooms.RoomId = {} AND Times.TimeId = {} AND STR_TO_DATE("{}", "%d.%m.%Y") BETWEEN '
                    'OrderDateStart AND OrderDateEnd'.format(abonement['RoomId'],
                                                             abonement['TimeId'],
                                                             datetime.date.strftime(datetime.date.today(),
                                                                                    '%d.%m.%Y')))
        room_curcapacity = cur.fetchone()
        cur.execute('SELECT RoomCapacity, RoomName, Times.TimeName '
                    'FROM Abonements '
                    'INNER JOIN Rooms ON Rooms.RoomId = Abonements.RoomId '
                    'INNER JOIN Times ON Times.TimeId = Abonements.TimeId '
                    'WHERE AbonementId = {}'.format(abonement_id))
        room = cur.fetchone()
        if room['RoomCapacity'] <= room_curcapacity['COUNT(*)']:
            return (False, 'Мест в зале "{}" на {} не осталось!'.format(room['RoomName'],
                                                                        room['TimeName'].lower()))
        # After checking, we need to insert new order row
        cur.execute('INSERT INTO Orders (AbonementId, OrderDateStart, OrderDateEnd) '
                    'VALUES ({}, CURDATE(), STR_TO_DATE("{}", "%d.%m.%Y"))'.format(abonement_id,
                                                                                   datetime.date.strftime(
                                                                                       datetime.date.today(),
                                                                                       '%d.%m.%Y')))
        con.commit()
        # Collect information about sold abonement
        cur.execute('SELECT RoomName, ServiceName, TimeName, AbonementPrice '
                    'FROM Abonements '
                    'INNER JOIN Rooms on Rooms.RoomId = Abonements.RoomId '
                    'INNER JOIN Services on Services.ServiceId = Abonements.ServiceId '
                    'INNER JOIN Times on Times.TimeId = Abonements.TimeId '
                    'WHERE AbonementId = {}'.format(abonement_id))
        row = cur.fetchone()
        return (True, 'Разовое посещение "{} - {} - {}" на сумму {} рублей на {} успешно продано'.format(
            row['RoomName'], row['ServiceName'], row['TimeName'], row['AbonementPrice'],
            datetime.date.strftime(datetime.date.today(), '%d.%m.%Y')
        ))


# Deny an abonement
def db_deny_abonement(order_id):
    # Connect to the local MySQL 'Fitness' db
    con = pymysql.connect(host='127.0.0.1',
                          user='root',
                          password='gpnb0b',
                          db='Fitness',
                          charset='utf8mb4',
                          cursorclass=pymysql.cursors.DictCursor)

    with con:
        cur = con.cursor()
        # Firstly we need to check if there is such order
        cur.execute('SELECT * FROM Orders WHERE OrderId = {}'.format(order_id))
        temp = cur.fetchone()
        if len(temp) == 0:
            return (False, 'Нет чека с указанным Id!')
        # Now we need to check if this order is a true abonement
        if temp['OrderDateStart'] == temp['OrderDateEnd']:
            return (False, 'Нельзя отказаться от разового посещения!')
        # Collect information about sold abonement
        cur.execute('SELECT RoomName, ServiceName, TimeName, AbonementPrice, OrderDateStart, OrderDateEnd '
                    'FROM Orders '
                    'INNER JOIN Abonements on Abonements.AbonementId = Orders.AbonementId '
                    'INNER JOIN Rooms on Rooms.RoomId = Abonements.RoomId '
                    'INNER JOIN Services on Services.ServiceId = Abonements.ServiceId '
                    'INNER JOIN Times on Times.TimeId = Abonements.TimeId '
                    'WHERE OrderId = {}'.format(order_id))
        row = cur.fetchone()
        days = (row['OrderDateEnd'] - datetime.date.today()).days + 1
        # After checking, we need to update orders date
        cur.execute('UPDATE Orders SET OrderDateEnd = DATE_SUB(CURDATE(), INTERVAL 1 DAY) '
                    'WHERE OrderId = {}'.format(order_id))
        con.commit()
        return (True, 'Абонемент "{} - {} - {}" от {} успешно отменен, к возврату {} рублей'.format(
            row['RoomName'], row['ServiceName'], row['TimeName'],
            datetime.date.strftime(row['OrderDateStart'], '%d.%m.%Y'), days * row['AbonementPrice']))
