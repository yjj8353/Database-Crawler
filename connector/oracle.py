import cx_Oracle

from connector import AbstractConnector


class OracleConnector(AbstractConnector):
    service_name: str = "orcl"
    sid: str = None

    def __init__(self, host="localhost", port=1521, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.host = host
        self.port = port

    def connect(self):
        if self.sid:
            dsn = cx_Oracle.makedsn(self.host, self.port, sid=self.sid)
        else:
            dsn = cx_Oracle.makedsn(self.host, self.port, service_name=self.service_name)

        try:
            self.conn = cx_Oracle.connect(
                user=self.username,
                password=self.password,
                dsn=dsn
            )
            return self.conn
        except cx_Oracle.DatabaseError as e:
            print(f"Oracle 데이터베이스 연결 오류: {e}")
            return None
