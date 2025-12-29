from dotenv import load_dotenv
import os

from connector.oracle import OracleConnector
from connector.mysql import MysqlConnector
from connector.postgresql import PostgreSQLConnector
from crawler.mysql import MySQLCrawler
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
        connector = None
        if vendor == "postgresql":
            connector = PostgreSQLConnector(database, username, password, host, int(port))
        elif vendor == "mysql":
            connector = MysqlConnector(database, username, password, host, int(port))

        if connector is not None:
            conn = connector.connect()

        if not conn:
            print("연결 실패")
            return

        crawler = None
        if vendor == "postgresql":
            crawler = PostgreSQLCrawler(connector, ["public"])
        elif vendor == "mysql":
            crawler = MySQLCrawler(connector)

        crawler.crawling()

    except Exception as e:
        print(f"오류 발생: {e}")

    finally:
        if conn:
            conn.close()


# 스크립트를 실행하려면 여백의 녹색 버튼을 누릅니다.
if __name__ == '__main__':
    connect()
