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

    def get_users(self):
        result = self.cursor.execute("SELECT `user_id` FROM `users`")
        return result.fetchall()

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
        self.cursor.execute(
            "INSERT INTO `users` (`user_id`, `user_phone_number`) VALUES (?, ?) ON CONFLICT (`user_id`) DO UPDATE SET user_id=excluded.user_id",
            (user_id, user_phone_number))
        return self.conn.commit()

    def add_user_phone(self, number):  # нахер это здесь? оно используется?
        """Добавляем номер телефона пользователя в базу"""
        self.cursor.execute("INSERT INTO `users` (`user_phone_number`) VALUES (?)",
                            (number,))

    def add_new_product(self, name, amount, cost):
        self.cursor.execute(
            "INSERT INTO `products` (`name`, `amount`, `cost`) VALUES (?, ?, ?)",
            (name, amount, cost,)
        )
        return self.conn.commit()

    def show_products(self):
        result = self.cursor.execute("SELECT product_id, name, amount, cost FROM `products`")
        return result.fetchall()

    def delete_product(self, product_id):
        self.cursor.execute("DELETE FROM products WHERE product_id = (?)", (product_id,))
        return self.conn.commit()

    def add_to_cart(self, user_id, product_id):
        # Добавление товара в корзину
        self.cursor.execute("SELECT `cart` FROM `users` WHERE `user_id` = ?", (product_id, user_id,))

    def get_points(self, user_id):
        # Получение количества баллов
        result = self.cursor.execute("SELECT `bonus_points` FROM `users` WHERE `user_id` = ?", (user_id,))
        return result.fetchone()[0]

    def get_lang(self, user_id):
        # Получение выбранного языка
        result = self.cursor.execute("SELECT  `lang` FROM `users` WHERE `user_id` = ?", (user_id,))
        return result.fetchone()[0]

    def change_lang(self, user_id, lang):
        # Смена языка
        self.cursor.execute("UPDATE `users` SET `lang` = ? WHERE `user_id` = ?", (lang, user_id,))
        return self.conn.commit()

    def change_phone_num(self, user_id, phone_num):
        # Смена номера телефона
        self.cursor.execute("UPDATE `users` SET `user_phone_number` = ? WHERE `user_id` = ?", (phone_num, user_id,))
        return self.conn.commit()

    def close(self):
        # Закрытие соединения с БД
        self.conn.close()
