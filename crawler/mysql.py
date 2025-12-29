from crawler import AbstractCrawler

from query import mysql as my


class MySQLCrawler(AbstractCrawler):
    def __init__(self, connector):
        super().__init__(connector)

    def crawling(self):
        tables = self.get_tables()
        print(f"Tables: {tables}")

        for table in tables:
            table_info = self.get_table_info(table)
            print(f"Info: {table_info}")

    def get_tables(self):
        query = """
            SELECT TABLE_NAME
              FROM information_schema.TABLES
             WHERE TABLE_SCHEMA = DATABASE()
               AND TABLE_TYPE = 'BASE TABLE'
             ORDER BY TABLE_NAME;
        """

        conn = self.connector.connect()
        try:
            with conn.cursor() as cur:
                cur.execute(query)
                rows = cur.fetchall()
                tables = [row[0] for row in rows]
        finally:
            conn.close()
        return tables

    def get_table_info(self, table):
        print(f"Table: {table}")
        columns = []
        pks = []
        fks = []

        select_col_query = my.select_columns_query()
        select_pk_query = my.select_pk_query()
        select_fk_query = my.select_fk_query()

        conn = self.connector.connect()
        try:
            with conn.cursor() as cur:
                cur.execute(select_col_query, (table, ))
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
                cur.execute(select_pk_query, (table, ))
                rows = cur.fetchall()
                for row in rows:
                    pks.append(row[0])

                # FK 정보 조회
                cur.execute(select_fk_query, (table, ))
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