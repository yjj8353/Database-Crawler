import oracledb

from connector import AbstractConnector


class OracleConnector(AbstractConnector):
    service_name: str = "orcl"
    sid: str = None

    def __init__(self, database, username, password, host="localhost", port=1521):
        super().__init__(database, username, password, host, port)

    def connect(self):
        if self.sid:
            dsn = oracledb.makedsn(self.host, self.port, sid=self.sid)
        else:
            dsn = oracledb.makedsn(self.host, self.port, service_name=self.service_name)

        try:
            self.conn = oracledb.connect(
                user=self.username,
                password=self.password,
                dsn=dsn
            )
            return self.conn
        except oracledb.DatabaseError as e:
            print(f"Oracle 데이터베이스 연결 오류: {e}")
            return None
