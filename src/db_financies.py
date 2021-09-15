import pymysql


# Returns OrderId, Orders.AbonementId, RoomName, ServiceName, TimeName, OrderDays, OrderPrice
# date in format 'dd.mm.YYYY'
def db_financies_day(date):
    # Connect to the local MySQL 'Fitness' db
    con = pymysql.connect(host='127.0.0.1',
                          user='root',
                          password='gpnb0b',
                          db='Fitness',
                          charset='utf8mb4')

    with con:
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
# date in mm.YYYY
def db_financies_month(date):
    # Connect to the local MySQL 'Fitness' db
    con = pymysql.connect(host='127.0.0.1',
                          user='root',
                          password='gpnb0b',
                          db='Fitness',
                          charset='utf8mb4')

    with con:
        cur = con.cursor()
        cur.execute('SELECT OrderId, Orders.AbonementId, RoomName, ServiceName, TimeName, '
                    'DATE_FORMAT(OrderDateStart, "%d.%m.%Y"), DATEDIFF(OrderDateEnd, OrderDateStart) + 1, '
                    'AbonementPrice * (DATEDIFF(OrderDateEnd, OrderDateStart) + 1) '
                    'FROM Orders '
                    'INNER JOIN Abonements ON Abonements.AbonementId = Orders.AbonementId '
                    'INNER JOIN Rooms ON Rooms.RoomId = Abonements.RoomId '
                    'INNER JOIN Services ON Services.ServiceId = Abonements.ServiceId '
                    'INNER JOIN Times ON Times.TimeId = Abonements.TimeId '
                    'WHERE MONTH(STR_TO_DATE("{}", "%m.%Y")) = MONTH(OrderDateStart) '
                    'AND YEAR(STR_TO_DATE("{}", "%m.%Y")) = YEAR(OrderDateStart) '
                    'ORDER BY OrderId'.format(date, date))
        rows = cur.fetchall()
        return rows


# Returns OrderId, Orders.AbonementId, RoomName, ServiceName, TimeName, OrderDays, OrderPrice
# date in YYYY
def db_financies_year(date):
    # Connect to the local MySQL 'Fitness' db
    con = pymysql.connect(host='127.0.0.1',
                          user='root',
                          password='gpnb0b',
                          db='Fitness',
                          charset='utf8mb4')

    with con:
        cur = con.cursor()
        cur.execute('SELECT OrderId, Orders.AbonementId, RoomName, ServiceName, TimeName, '
                    'DATE_FORMAT(OrderDateStart, "%d.%m.%Y"), DATEDIFF(OrderDateEnd, OrderDateStart) + 1, '
                    'AbonementPrice * (DATEDIFF(OrderDateEnd, OrderDateStart) + 1) '
                    'FROM Orders '
                    'INNER JOIN Abonements ON Abonements.AbonementId = Orders.AbonementId '
                    'INNER JOIN Rooms ON Rooms.RoomId = Abonements.RoomId '
                    'INNER JOIN Services ON Services.ServiceId = Abonements.ServiceId '
                    'INNER JOIN Times ON Times.TimeId = Abonements.TimeId '
                    'WHERE YEAR(STR_TO_DATE("{}", "%m.%Y")) = YEAR(OrderDateStart) '
                    'ORDER BY OrderId'.format(date))
        rows = cur.fetchall()
        return rows


if __name__ == '__main__':
    rows = db_financies_year('2021')
