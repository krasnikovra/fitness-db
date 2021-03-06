import datetime


def db_check_for_free_space(con, abonement_id):
    cur = con.cursor()
    cur.execute('SELECT * FROM Abonements WHERE AbonementId = {}'.format(abonement_id))
    abonement = cur.fetchone()
    cur.execute('SELECT COUNT(*) '
                'FROM Orders '
                'INNER JOIN Abonements on Abonements.AbonementId = Orders.AbonementId '
                'INNER JOIN Rooms on Rooms.RoomId = Abonements.RoomId '
                'INNER JOIN Services on Services.ServiceId = Abonements.ServiceId '
                'INNER JOIN Times on Times.TimeId = Abonements.TimeId '
                'WHERE Rooms.RoomId = {} AND Times.TimeId = {} AND STR_TO_DATE("{}", "%d.%m.%Y") BETWEEN '
                'OrderDateStart AND OrderDateEnd'.format(abonement[1],
                                                         abonement[3],
                                                         datetime.date.strftime(datetime.date.today(), '%d.%m.%Y')))
    room_curcapacity = cur.fetchone()
    cur.execute('SELECT RoomCapacity, RoomName, Times.TimeName '
                'FROM Abonements '
                'INNER JOIN Rooms ON Rooms.RoomId = Abonements.RoomId '
                'INNER JOIN Times ON Times.TimeId = Abonements.TimeId '
                'WHERE AbonementId = {}'.format(abonement_id))
    room = cur.fetchone()
    if room[0] <= room_curcapacity[0]:
        return (False, 'Мест в зале "{}" на {} не осталось!'.format(room[1],
                                                                    room[2].lower()))
    return (True, 'Есть свободные места в зале "{}" на {}.'.format(room[1],
                                                                   room[2].lower()))


# Sell an abonement; date_end in format dd.mm.yyyy
# Returns '' if ok and error message if error has occurred
def db_sell_abonement(con, abonement_id, date_end):
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
    is_ok, msg = db_check_for_free_space(con, abonement_id)
    if not is_ok:
        return (False, msg)
    # After checking, we need to insert new order row
    cur.execute('INSERT INTO Orders (AbonementId, OrderDateStart, OrderDateEnd) '
                'VALUES ({}, CURDATE(), STR_TO_DATE("{}", "%d.%m.%Y"))'.format(abonement_id, date_end))
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
        row[0], row[1], row[2], row[3] * days, days))


def db_sell_oneday(con, abonement_id):
    cur = con.cursor()
    # We need to check if there is such abonement_id
    cur.execute('SELECT * FROM Abonements WHERE AbonementId = {}'.format(abonement_id))
    temp = cur.fetchall()
    if len(temp) == 0:
        return (False, 'Нет абонемента с указанным Id!')
    # Check for free spaces in room
    is_ok, msg = db_check_for_free_space(con, abonement_id)
    if not is_ok:
        return (False, msg)
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
        row[0], row[1], row[2], row[3],
        datetime.date.strftime(datetime.date.today(), '%d.%m.%Y')
    ))


# Deny an abonement
def db_deny_abonement(con, order_id):
    cur = con.cursor()
    # Firstly we need to check if there is such order
    cur.execute('SELECT * FROM Orders WHERE OrderId = {}'.format(order_id))
    temp = cur.fetchone()
    if len(temp) == 0:
        return (False, 'Нет чека с указанным Id!')
    # Now we need to check if this order is a true abonement
    if temp[2] == temp[3]:
        return (False, 'Нельзя отказаться от разового посещения!')
    if temp[3] < datetime.date.today():
        return (False, 'Срок действия этого абонемента уже истек!')
    # Collect information about sold abonement
    cur.execute('SELECT RoomName, ServiceName, TimeName, AbonementPrice, OrderDateStart, OrderDateEnd '
                'FROM Orders '
                'INNER JOIN Abonements on Abonements.AbonementId = Orders.AbonementId '
                'INNER JOIN Rooms on Rooms.RoomId = Abonements.RoomId '
                'INNER JOIN Services on Services.ServiceId = Abonements.ServiceId '
                'INNER JOIN Times on Times.TimeId = Abonements.TimeId '
                'WHERE OrderId = {}'.format(order_id))
    row = cur.fetchone()
    days = (row[5] - datetime.date.today()).days + 1
    # After checking, we need to update orders date
    cur.execute('UPDATE Orders SET OrderDateEnd = DATE_SUB(CURDATE(), INTERVAL 1 DAY) '
                'WHERE OrderId = {}'.format(order_id))
    con.commit()
    return (True, 'Абонемент "{} - {} - {}" от {} успешно отменен, к возврату {} рублей'.format(
        row[0], row[1], row[2],
        datetime.date.strftime(row[4], '%d.%m.%Y'), days * row[3]))
