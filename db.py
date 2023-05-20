import sqlite3
import sys
import pathlib

class BotDB:
    def __init__(self, db_file):
        # Инициализация соединения с БД
        script_dir = pathlib.Path(sys.argv[0]).parent
        db_file_way = script_dir / db_file
        self.conn = sqlite3.connect(db_file_way)
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id):
        """Проверяем, есть ли юзер в базе"""
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return bool(len(result.fetchall()))

    def get_user_id(self, user_id):
        """Достаем id юзера в базе по его user_id"""
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return result.fetchone()[0]

    def get_user_tg_id(self, user_id):
        """Достаем id юзера из телеграмма по его user_id"""
        result = self.cursor.execute("SELECT `user_id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return result

    def get_user_phone(self, user_id):
        result = self.cursor.execute("SELECT `user_phone_number` FROM `users` WHERE `user_id` = ?", (user_id,))
        return result.fetchone()[0]

    '''def add_user(self, user_id):
        """Добавляем юзера в базу"""
        self.cursor.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (user_id,))
        return self.conn.commit()'''

    def add_user(self, user_id, user_phone_number):
        """Добавляем юзера и его номер телефона в базу"""
        self.cursor.execute("INSERT INTO `users` (`user_id`, `user_phone_number`) VALUES (?, ?) ON CONFLICT (`user_id`) DO UPDATE SET user_id=excluded.user_id", (user_id, user_phone_number))
        return self.conn.commit()

    #----------
    def add_user_phone(self, user_id, number):
        """Добавляем номер телефона пользователя в базу"""
        '''self.cursor.execute("INSERT INTO `users` (`user_id`, `user_phone_number`) VALUES (?, ?)",
                            (self.get_user_id(user_id),
                             number))'''
        self.cursor.execute("INSERT INTO `users` (`user_phone_number`) VALUES (?)",
                            (number,))
    #----------


    def get_points(self, user_id):
        # Получение количества баллов
        result = self.cursor.execute("SELECT `bonus_points` FROM `users` WHERE `user_id` = ?", (user_id,))
        return result.fetchone()[0]

    def close(self):
        # Закрытие соединения с БД
        self.conn.close()