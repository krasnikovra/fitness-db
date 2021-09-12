import pymysql


# Connects to the MySQL server and creates 'Fitness' db
def db_init():
    # Connect to the local MySQL server
    con = pymysql.connect(host='127.0.0.1',
                          user='root',
                          password='gpnb0b',
                          charset='utf8mb4')

    with con:
        cur = con.cursor()
        cur.execute("SELECT VERSION()")

        version = cur.fetchone()

        print("Database version: {}".format(version[0]))

        try:
            # Create MySQL database
            cur.execute('CREATE DATABASE Fitness;')
        except Exception as e:
            print("Error: {}".format(e))
            return

        print('Database \'Fitness\' has been created')
        return


# Connects to the 'Fitness' db and creates all the tables according
# to the scheme of db
def db_create_tables():
    # Connect to the local MySQL 'Fitness' db
    con = pymysql.connect(host='127.0.0.1',
                          user='root',
                          password='gpnb0b',
                          db='Fitness',
                          charset='utf8mb4')

    with con:
        cur = con.cursor()
        try:
            cur.execute('CREATE TABLE Rooms '
                        '('
                        'RoomId INT PRIMARY KEY AUTO_INCREMENT, '
                        'RoomName NVARCHAR(64) NOT NULL, '
                        'RoomCapacity INT NOT NULL'
                        ');')
            cur.execute('CREATE TABLE Services '
                        '('
                        'ServiceId INT PRIMARY KEY AUTO_INCREMENT, '
                        'ServiceName NVARCHAR(64) NOT NULL'
                        ');')
            cur.execute('CREATE TABLE Times '
                        '('
                        'TimeId INT PRIMARY KEY AUTO_INCREMENT, '
                        'TimeName NVARCHAR(64) NOT NULL'
                        ');')
            cur.execute('CREATE TABLE Abonements '
                        '('
                        'AbonementId INT PRIMARY KEY AUTO_INCREMENT, '
                        'RoomId INT, '
                        'ServiceId INT, '
                        'TimeId INT, '
                        'AbonementPrice INT NOT NULL, '
                        'FOREIGN KEY (RoomId) REFERENCES Rooms (RoomId), '
                        'FOREIGN KEY (ServiceId) REFERENCES Services (ServiceId), '
                        'FOREIGN KEY (TimeId) REFERENCES Times (TimeId)'
                        ');')
            cur.execute('CREATE TABLE Orders '
                        '('
                        'OrderId INT PRIMARY KEY AUTO_INCREMENT, '
                        'AbonementId INT, '
                        'OrderDateStart DATE NOT NULL, '
                        'OrderDateEnd DATE NOT NULL, '
                        'FOREIGN KEY (AbonementId) REFERENCES Abonements (AbonementId)'
                        ');')
        except Exception as e:
            print("Error: {}".format(e))
            return

        cur.execute('SHOW TABLES;')
        tables = cur.fetchall()
        print("Tables in Fitness db: {}".format(tables))

        # In tables we have (('example',),...) so tables' instance need to be
        # unpacked too
        for tablename_tuple in tables:
            cur.execute('DESCRIBE {}'.format(tablename_tuple[0]))
            tabledesc = cur.fetchall()
            print('Table \'{}\' has these columns:'.format(tablename_tuple[0]))
            for column in tabledesc:
                print(column)
        return


# Destroys the 'Fitness' db
def db_destroy():
    # Connect to the local MySQL server
    con = pymysql.connect(host='127.0.0.1',
                          user='root',
                          password='gpnb0b',
                          charset='utf8mb4')

    with con:
        cur = con.cursor()

        try:
            cur.execute('DROP DATABASE Fitness;')
        except Exception as e:
            print("Error: {}".format(e))
            return
        print('Database \'Fitness\' has been destroyed')
        return


# Fills all the default constants according to the task
def db_insert_constants():
    # Connect to the local MySQL 'Fitness' db
    con = pymysql.connect(host='127.0.0.1',
                          user='root',
                          password='gpnb0b',
                          db='Fitness',
                          charset='utf8mb4')

    with con:
        cur = con.cursor()
        rooms_data = (('Силовой зал комфорт', 30),
                      ('Силовой зал эконом', 15),
                      ('Зал аэробики', 25),
                      ('Зал для бокса', 10),
                      ('Кардио зал', 20))
        # Inserting rooms data
        for room_data in rooms_data:
            cur.execute('INSERT INTO Rooms (RoomName, RoomCapacity) '
                        'VALUES ("{}", {})'.format(room_data[0], room_data[1]))
        print('Constants inserted into Rooms table successfully')
        services_data = ('Силовая тренировка',
                         'Гимнастика',
                         'Групповое занятие по аэробике',
                         'Тренировка по боксу',
                         'Кардио тренировка')
        # Inserting services data
        for service_data in services_data:
            cur.execute('INSERT INTO Services (ServiceName) '
                        'VALUES ("{}")'.format(service_data))
        print('Constants inserted into Services table successfully')
        times_data = ('Утро',
                      'Вечер')
        # Inserting times data
        for time_data in times_data:
            cur.execute('INSERT INTO Times (TimeName) '
                        'VALUES ("{}")'.format(time_data))
        print('Constants inserted into Times table successfully')
        abonements_data = ((1, 1, 1, 600),
                           (1, 1, 2, 700),
                           (2, 1, 1, 400),
                           (2, 1, 2, 500),
                           (3, 2, 1, 550),
                           (3, 2, 2, 680),
                           (3, 3, 1, 250),
                           (3, 3, 2, 300),
                           (4, 4, 1, 700),
                           (4, 4, 2, 850),
                           (4, 5, 1, 470),
                           (4, 5, 2, 620),
                           (5, 5, 1, 350),
                           (5, 5, 2, 460))
        # Inserting abonements data
        for abon_data in abonements_data:
            cur.execute('INSERT INTO Abonements (RoomId, ServiceId, TimeId, AbonementPrice) '
                        'VALUES ({}, {}, {}, {})'.format(abon_data[0], abon_data[1],
                                                         abon_data[2], abon_data[3]))
        print('Constants inserted into Abonements table successfully')
        # Now we need to commit all the rows into db
        con.commit()
