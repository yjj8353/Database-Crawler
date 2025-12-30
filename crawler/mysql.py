from crawler import AbstractCrawler
from data.column import Column

from query import mysql as my
from data.table import Table


class MySQLCrawler(AbstractCrawler):
    def __init__(self, connector, schema):
        super().__init__(connector)
        self.schema = schema

    def crawling(self):
        tables = self.get_tables()
        print(f"Tables: {tables}")

        for table in tables:
            table_info = self.get_table_info(table)
            print(f"Info: {table_info}")

    def get_tables(self):
        query = """
            SELECT TABLE_NAME
                 , TABLE_COMMENT
              FROM information_schema.TABLES
             WHERE TABLE_SCHEMA = DATABASE()
               AND TABLE_TYPE = 'BASE TABLE'
             ORDER BY TABLE_NAME;
        """

        conn = self.connector.connect()
        try:
            tables: list[Table] = []
            with conn.cursor() as cur:
                cur.execute(query)
                rows = cur.fetchall()
                for row in rows:
                    table = Table(row)
                    tables.append(table)
        finally:
            conn.close()

        return tables

    def get_table_info(self, table):
        print(f"Table: {table.table_name}")
        columns = []

        conn = self.connector.connect()
        try:
            with conn.cursor() as cur:
                cur.execute(my.select_columns_info_query(), (table, ))
                rows = cur.fetchall()
                for row in rows:
                    column = Column(row)
                    columns.append(column)

        except Exception as e:
            print(f"테이블 정보 조회 오류: {e}")

        finally:
            conn.close()

        return columns