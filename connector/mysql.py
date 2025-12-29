import mysql.connector as connector
from mysql.connector import Error

from connector import AbstractConnector


class MysqlConnector(AbstractConnector):
    def __init__(self, host="localhost", port=3306, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.host = host
        self.port = port

    def connect(self):
        try:
            self.conn = connector.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.username,
                password=self.password
            )
            return self.conn
        except Error as e:
            print(f"MySQL 데이터베이스 연결 중 오류 발생: {e}")
            return None
