import psycopg2

from connector import AbstractConnector


class PostgreSQLConnector(AbstractConnector):
    def __init__(self, database, username, password, host="127.0.0.1", port=5432):
        super().__init__(database, username, password, host, port)

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                host = self.host,
                port = self.port,
                dbname = self.database,
                user = self.username,
                password = self.password
            )
            return self.conn

        except Exception as e:
            print(f"PostgreSQL 데이터베이스 연결 오류: {e}")
            return None
