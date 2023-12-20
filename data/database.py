from sqlite3 import connect, Cursor


def db_session(method):
    def wrapper(self, *args, **kwargs):
        connection = connect('data/data.db')
        cursor = connection.cursor()
        try:
            return method(self, *args, **kwargs, cursor=cursor)
        finally:
            connection.commit()
            connection.close()
    return wrapper


class Database:
    @db_session
    def __init__(self, cursor: Cursor):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL UNIQUE,
                points INTEGER NOT NULL
            )
        ''')

    @db_session
    def insert_user(user_id: int, points: int = 0):
        cursor.execute('INSERT INTO Users (user_id, points) VALUES (?, ?)', (user_id, points))

    @db_session
    def select_user(self, user_id: int):
        cursor.exexute('SELECT * FROM Users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        return result

    @db_session
    def update_user(user_id: int, points: int):
        cursor.execute('UPDATE Users SET points = ? WHERE user_id = ?', (points, user_id,))