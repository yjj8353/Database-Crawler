from crawler import AbstractCrawler

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
            SELECT table_name
              FROM information_schema.tables
             WHERE table_schema = %s
             ORDER BY table_name;
        """

        conn = self.connector.connect()
        try:
            with conn.cursor() as cur:
                cur.execute(query, (schema, ))
                rows = cur.fetchall()
                tables = [row[0] for row in rows]
        finally:
            conn.close()
        return tables

    def get_table_info(self, schema, table):
        print(f"Schema: {schema}, Table: {table}")
        columns = []
        pks = []
        fks = []

        select_col_query = pq.select_columns_query()
        select_pk_query = pq.select_pk_query()
        select_fk_query = pq.select_fk_query()

        conn = self.connector.connect()
        try:
            with conn.cursor() as cur:
                cur.execute(select_col_query, (schema, table))
                rows = cur.fetchall()
                for row in rows:
                    col = {
                        "table_name": row[0],
                        "column_name": row[1],
                        "ordinal_position": row[2],
                        "data_type": row[3],
                        "udt_name": row[4],
                        "character_maximum_length": row[5],
                        "numeric_precision": row[6],
                        "is_nullable": row[7],
                        "column_default": row[8],
                        "is_identity": row[9],
                        "is_generated": row[10],
                        "collation_name": row[11],
                        "datetime_precision": row[12]
                    }
                    columns.append(col)

                # PK 정보 조회
                cur.execute(select_pk_query, (schema, table))
                rows = cur.fetchall()
                for row in rows:
                    pks.append(row[0])

                # FK 정보 조회
                cur.execute(select_fk_query, (schema, table))
                rows = cur.fetchall()
                for row in rows:
                    fk = {
                        "column_name": row[0],
                        "foreign_table_schema": row[1],
                        "foreign_table_name": row[2],
                        "foreign_column_name": row[3],
                        "update_rule": row[4],
                        "delete_rule": row[5],
                        "constraint_name": row[6]
                    }
                    fks.append(fk)

        except Exception as e:
            print(f"테이블 정보 조회 오류: {e}")

        finally:
            conn.close()

        return {
            "columns": columns,
            "primary_keys": pks,
            "foreign_keys": fks
        }