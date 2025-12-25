from dotenv import load_dotenv
import os

from connector.oracle import OracleConnector
from connector.mysql import MysqlConnector
from connector.postgresql import PostgresqlConnector


load_dotenv()


def connect():
    vendor = os.getenv("VENDOR")
    database = os.getenv("DATABASE")
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    host = os.getenv("HOST")
    port = os.getenv("PORT")
    service_name = os.getenv("SERVICE_NAME")
    sid = os.getenv("SID")
    connector = None
    conn = None
    try:
        if vendor == "oracle":
            connector = OracleConnector()
        elif vendor == "mysql":
            connector = MysqlConnector()
        elif vendor == "postgresql":
            connector = PostgresqlConnector(host, int(port), database, username, password)

        if connector:
            conn = connector.connect()

        if conn:
            print(f"{vendor} 데이터베이스에 성공적으로 연결되었습니다.")
        else:
            ConnectionError(f"{vendor} 데이터베이스에 연결하지 못했습니다.")
    except Exception as e:
        print(f"데이터베이스 커넥터 생성 중 오류 발생: {e}")
        return


# 스크립트를 실행하려면 여백의 녹색 버튼을 누릅니다.
if __name__ == '__main__':
    connect()
