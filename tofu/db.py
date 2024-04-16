import sqlite3

class Film:
    def __init__(self, title, direction, genere, duration, cast, time_slots, reservation, trailer):
        self.title = title 
        self.direction = direction
        self.genere = genere
        self.duration = duration
        self.cast = cast
        self.time_slots = time_slots # day and time of movie 
        self.reservation = reservation # link for reservate a seat
        self.trailer = trailer # link to see the movie's trailer

def db_insert(title, direction, genere, duration, cast, time_slots, reservation, trailer):
    f = Film(title, direction, genere, duration, cast, time_slots, reservation, trailer)

    connection = sqlite3.connect("movies.db")

    cursor = connection.cursor()

    # , direction INTEGER, genre TEXT, duration INTEGER, cast TEXT, time_slots TEXT, reservation TEXT, trailer TEXT

    cursor.execute("CREATE TABLE IF NOT EXISTS example (title TEXT, direction INTEGER, genre TEXT, duration INTEGER, cast TEXT, time_slots TEXT, reservation TEXT, trailer TEXT)")

    f.time_slots = str(f.time_slots)

    cursor.execute("INSERT INTO example VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (f.title, f.direction, f.genere, f.duration, f.cast, f.time_slots, f.reservation, f.trailer))

    connection.commit()

    connection.close()

def db_test():

    connection = sqlite3.connect("movies.db")
    
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM example")

    rows = cursor.fetchall()

    # Print elements actually in the database
    for row in rows:
        print(row[0])

    connection.close()

class User:
    def __init__(self, name, password, favourites):
        self.name = name 
        self.password = password
        self.favourites = favourites

def db_insert_user(name, password, favourites):
    u = User(name, password, favourites)

    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS users (name TEXT PRIMARY KEY, password TEXT, favourites TEXT)")
    cursor.execute("INSERT INTO users VALUES (?, ?, ?)", (u.name, u.password, u.favourites))
    connection.commit()
    connection.close()