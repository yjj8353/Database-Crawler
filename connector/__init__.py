from abc import ABCMeta, abstractmethod
from typing import Any


class AbstractConnector(metaclass=ABCMeta):
    database: str
    username: str
    password: str
    host: str
    port: int
    conn: Any

    def __init__(self, database: str, username: str, password: str, host: str, port: int):
        self.database = database
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.conn = None

    @abstractmethod
    def connect(self):
        pass

    def disconnect(self):
        if self.conn:
            self.conn.close()

    def cursor(self):
        return self.conn.cursor()
