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
                user_id INTEGER NOT NULL,
                username TEXT NOT NULL,
                points INTEGER NOT NULL,
                time_voice INTEGER NOT NULL
            )
        ''')

    @db_session
    def insert_user(self, user_id: int, username: str, points: int, time_voice: int, cursor: Cursor):
        cursor.execute('SELECT * FROM Users WHERE user_id = ?', (user_id,))
        user = cursor.fetchone()
        if user:
            print('Такой юзер уже есть')
            return
        else:
            print('Добавил нового юзера')
            cursor.execute('INSERT INTO Users (user_id, username, points, time_voice) VALUES (?, ?, ?, ?)', (user_id, username, points, time_voice,))

    @db_session
    def select_user(self, user_id: int, cursor: Cursor):
        cursor.execute('SELECT * FROM Users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        return result

    @db_session
    def update_points(self, user_id: int, points: int, cursor: Cursor):
        cursor.execute('UPDATE Users SET points = ? WHERE user_id = ?', (points, user_id,))

    @db_session
    def update_time_voice(self, user_id: int, time_voice: int, cursor: Cursor):
        cursor.execute('UPDATE Users SET time_voice = ? WHERE user_id = ?', (time_voice, user_id,))