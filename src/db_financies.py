import pymysql


# Returns OrderId, Orders.AbonementId, RoomName, ServiceName, TimeName, OrderDays, OrderPrice
# date in format 'dd.mm.YYYY'
def db_financies_day(con, date):
    cur = con.cursor()
    cur.execute('SELECT OrderId, Orders.AbonementId, RoomName, ServiceName, TimeName, '
                'DATE_FORMAT(OrderDateStart, "%d.%m.%Y"), DATEDIFF(OrderDateEnd, OrderDateStart) + 1, '
                'AbonementPrice * (DATEDIFF(OrderDateEnd, OrderDateStart) + 1) '
                'FROM Orders '
                'INNER JOIN Abonements ON Abonements.AbonementId = Orders.AbonementId '
                'INNER JOIN Rooms ON Rooms.RoomId = Abonements.RoomId '
                'INNER JOIN Services ON Services.ServiceId = Abonements.ServiceId '
                'INNER JOIN Times ON Times.TimeId = Abonements.TimeId '
                'WHERE STR_TO_DATE("{}", "%d.%m.%Y") = OrderDateStart'.format(date))
    rows = cur.fetchall()
    return rows


# Returns OrderId, Orders.AbonementId, RoomName, ServiceName, TimeName, OrderDays, OrderPrice
def db_financies_month(con, date):
    cur = con.cursor()
    cur.execute('SELECT OrderId, Orders.AbonementId, RoomName, ServiceName, TimeName, '
                'DATE_FORMAT(OrderDateStart, "%d.%m.%Y"), DATEDIFF(OrderDateEnd, OrderDateStart) + 1, '
                'AbonementPrice * (DATEDIFF(OrderDateEnd, OrderDateStart) + 1) '
                'FROM Orders '
                'INNER JOIN Abonements ON Abonements.AbonementId = Orders.AbonementId '
                'INNER JOIN Rooms ON Rooms.RoomId = Abonements.RoomId '
                'INNER JOIN Services ON Services.ServiceId = Abonements.ServiceId '
                'INNER JOIN Times ON Times.TimeId = Abonements.TimeId '
                'WHERE MONTH(STR_TO_DATE("{}", "%d.%m.%Y")) = MONTH(OrderDateStart) '
                'AND YEAR(STR_TO_DATE("{}", "%d.%m.%Y")) = YEAR(OrderDateStart) '
                'ORDER BY OrderId'.format(date, date))
    rows = cur.fetchall()
    return rows


# Returns OrderId, Orders.AbonementId, RoomName, ServiceName, TimeName, OrderDays, OrderPrice
def db_financies_year(con, date):
    cur = con.cursor()
    cur.execute('SELECT OrderId, Orders.AbonementId, RoomName, ServiceName, TimeName, '
                'DATE_FORMAT(OrderDateStart, "%d.%m.%Y"), DATEDIFF(OrderDateEnd, OrderDateStart) + 1, '
                'AbonementPrice * (DATEDIFF(OrderDateEnd, OrderDateStart) + 1) '
                'FROM Orders '
                'INNER JOIN Abonements ON Abonements.AbonementId = Orders.AbonementId '
                'INNER JOIN Rooms ON Rooms.RoomId = Abonements.RoomId '
                'INNER JOIN Services ON Services.ServiceId = Abonements.ServiceId '
                'INNER JOIN Times ON Times.TimeId = Abonements.TimeId '
                'WHERE YEAR(STR_TO_DATE("{}", "%d.%m.%Y")) = YEAR(OrderDateStart) '
                'ORDER BY OrderId'.format(date))
    rows = cur.fetchall()
    return rows
