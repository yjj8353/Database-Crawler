from dotenv import load_dotenv
import os

from connector.oracle import OracleConnector
from connector.mysql import MysqlConnector
from connector.postgresql import PostgreSQLConnector
from crawler.postgresql import PostgreSQLCrawler


load_dotenv()


def connect():
    vendor = os.getenv("VENDOR")
    database = os.getenv("DATABASE")
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    host = os.getenv("HOST")
    port = os.getenv("PORT")

    conn = None
    try:
        connector = PostgreSQLConnector(host, int(port), database, username, password)
        conn = connector.connect()
        if not conn:
            print("연결 실패")
            return

        crawler = PostgreSQLCrawler(connector, ["public"])
        crawler.crawling()

    except Exception as e:
        print(f"오류 발생: {e}")

    finally:
        if conn:
            conn.close()


# 스크립트를 실행하려면 여백의 녹색 버튼을 누릅니다.
if __name__ == '__main__':
    connect()
