from crawler import AbstractCrawler
from data.column import Column

from query import oracle as ora
from data.table import Table


class OracleCrawler(AbstractCrawler):
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
            SELECT UT.TABLE_NAME
                 , NVL(UTC.COMMENTS, '') AS TABLE_COMMENT
            FROM USER_TABLES UT
            LEFT OUTER JOIN USER_TAB_COMMENTS UTC
              ON UT.TABLE_NAME = UTC.TABLE_NAME
            ORDER BY UT.TABLE_NAME
        """

        conn = self.connector.connect()
        try:
            tables: list[Table] = []
            with conn.cursor() as cur:
                cur.execute(query)
                cols = [desc[0] for desc in cur.description]
                rows = cur.fetchall()
                for row in rows:
                    row_dict = dict(zip(cols, row))
                    table = Table(row_dict)
                    tables.append(table)
        finally:
            conn.close()

        return tables

    def get_table_info(self, table):
        print(f"Table: {table.table_name}")
        columns: list[Column] = []

        conn = self.connector.connect()
        try:
            with conn.cursor() as cur:
                cur.execute(ora.select_columns_info_query(), { "owner": self.schema, "table_name": table.table_name })
                cols = [d[0] for d in cur.description] if cur.description else []
                rows = cur.fetchall()
                for row in rows:
                    row_dict = dict(zip(cols, row))
                    column = Column(row_dict)
                    columns.append(column)

        except Exception as e:
            print(f"테이블 정보 조회 오류: {e}")

        finally:
            conn.close()

        return columns