# Select current rooms capacities
# date in format dd.mm.yyyy
# Returns tuple of rows(tuples) with RoomId, RoomName, RoomCurrentCapacity, RoomCapacity
def db_select_rooms_current_capacity(con, date, time_id):
    cur = con.cursor()
    cur.execute('SELECT Rooms.RoomId, Rooms.RoomName, Rooms.RoomCapacity '
                'FROM Rooms '
                'ORDER BY Rooms.RoomId')
    rooms = cur.fetchall()
    res = [[None for x in range(len(rooms[0]) + 1)] for x in range(len(rooms))]
    for i in range(len(rooms)):
        cur.execute('SELECT COUNT(*) '
                    'FROM Orders '
                    'INNER JOIN Abonements on Abonements.AbonementId = Orders.AbonementId '
                    'INNER JOIN Rooms on Rooms.RoomId = Abonements.RoomId '
                    'INNER JOIN Services on Services.ServiceId = Abonements.ServiceId '
                    'INNER JOIN Times on Times.TimeId = Abonements.TimeId '
                    'WHERE Rooms.RoomId = {} AND Times.TimeId = {} AND STR_TO_DATE("{}", "%d.%m.%Y") BETWEEN '
                    'OrderDateStart AND OrderDateEnd'.format(rooms[i][0], time_id, date))
        room_curcapacity = cur.fetchone()
        res[i][0] = rooms[i][0]
        res[i][1] = rooms[i][1]
        res[i][2] = rooms[i][2]
        res[i][3] = rooms[i][2] - room_curcapacity[0]
    return res
