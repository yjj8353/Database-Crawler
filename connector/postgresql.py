import psycopg2

from connector import AbstractConnector


class PostgresqlConnector(AbstractConnector):
    def __init__(self, host="localhost", port=5432, database="", username="", password=""):
        super().__init__(host, port, database, username, password)
        self.host = host
        self.port = port

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                dbname=self.database,
                user=self.username,
                password=self.password
            )
            return self.conn
        except Exception as e:
            print(f"PostgreSQL 데이터베이스 연결 오류: {e}")
            return None

    def disconnect(self):
        if self.conn:
            self.conn.close()
