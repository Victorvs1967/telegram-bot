import sqlite3

class DbLighter:

    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def get_subscriptions(self, status=True):
        with self.connection:
            return self.cursor.execute(f"SELECT * FROM `subscriptions` WHERE `status` = {status}").fetchall()

    def subscriber_exist(self, user_id):
        with self.connection:
            result = self.cursor.execute(f"SELECT * FROM `subscriptions` WHERE `user_id` = {user_id}").fetchall()
            return bool(len(result))

    def add_subscriber(self, user_id, status=True):
        with self.connection:
            return self.cursor.execute(f"INSERT INTO `subscriptions` (`user_id`, `status`) VALUES ({user_id}, {status})").fetchall()

    def update_subscription(self, user_id, status):
        with self.connection:
            return self.cursor.execute(f"UPDATE `subscriptions` SET `status` = {status} WHERE `user_id` = {user_id}").fetchall()

    def close(self):
        self.connection.close



# app.py for SQLight
# from config import DB_FILE
# db = DbLighter(DB_FILE) 
