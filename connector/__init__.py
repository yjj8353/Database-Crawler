from abc import ABCMeta, abstractmethod
from typing import Any


class AbstractConnector(metaclass=ABCMeta):
    host: str
    port: int
    database: str
    username: str
    password: str
    conn: Any

    def __init__(self, host: str, port: int, database: str, username: str, password: str):
        self.host = host
        self.port = port
        self.database = database
        self.username = username
        self.password = password
        self.conn = None

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    def cursor(self):
        return self.conn.cursor()
