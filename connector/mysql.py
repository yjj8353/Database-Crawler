import mysql.connector as connector
from mysql.connector import Error

from connector import AbstractConnector


class MysqlConnector(AbstractConnector):
    def __init__(self, database, username, password, host="127.0.0.1", port=3306):
        super().__init__(database, username, password, host, port)

    def connect(self):
        try:
            self.conn = connector.connect(
                host = self.host,
                port = self.port,
                database = self.database,
                user = self.username,
                password = self.password
            )
            return self.conn
        except Error as e:
            print(f"MySQL 데이터베이스 연결 중 오류 발생: {e}")
            return None
