from crawler import AbstractCrawler
from data.column import Column
from data.table import Table

from query import postgresql as pq

class PostgreSQLCrawler(AbstractCrawler):
    def __init__(self, connector, schemas=None):
        super().__init__(connector)
        self.schemas = schemas

    def crawling(self):

        # 스키마 조회 (지정된 스키마가 없으면, 전체 스키마를 조회함)
        if self.schemas is None:
            self.schemas = self.get_schemas()

        # 스키마별 테이블 조회
        for schema in self.schemas:
            tables = self.get_tables(schema)
            print(f"Schema: {schema}, Tables: {tables}")

            for table in tables:
                table_info = self.get_table_info(schema, table)
                print(f"Table: {schema}.{table}, Info: {table_info}")

    def get_schemas(self):
        query = """
            SELECT schema_name
              FROM information_schema.schemata
             ORDER BY schema_name;
        """
        conn = self.connector.connect()

        try:
            with conn.cursor() as cur:
                cur.execute(query)
                rows = cur.fetchall()
                schemas = [row[0] for row in rows]
        finally:
            conn.close()
        return schemas

    # 특정 스키마의 전체 테이블 정보 조회
    def get_tables(self, schema):
        query = """
            SELECT t.TABLE_NAME as "TABLE_NAME"
                 , obj_description(c.oid, 'pg_class') AS "TABLE_COMMENT"
              FROM information_schema.tables t
             INNER JOIN pg_catalog.pg_class c ON c.relname = t.table_name
             INNER JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace AND n.nspname = t.table_schema
             WHERE t.table_schema = %s
               AND t.table_type   = 'BASE TABLE' -- View 제외
             ORDER BY t.table_name;
        """

        tables: list[Table] = []
        conn = self.connector.connect()
        try:
            with conn.cursor() as cur:
                cur.execute(query, (schema, ))
                rows = cur.fetchall()
                for row in rows:
                    table = Table(row)
                    tables.append(table)
        finally:
            conn.close()

        return tables

    def get_table_info(self, schema, table):
        print(f"Schema: {schema}, Table: {table}")
        columns: list[Column] = []

        conn = self.connector.connect()
        try:
            with conn.cursor() as cur:
                cur.execute(pq.select_columns_info_query(), (schema, table.table_name, schema, table.table_name))
                rows = cur.fetchall()
                for row in rows:
                    col = Column(row)
                    columns.append(col)

        except Exception as e:
            print(f"테이블 정보 조회 오류: {e}")

        finally:
            conn.close()

        return columns
