from data.column import Column


class Table:
    __table_name: str
    __table_comment: str
    __columns: list[Column]

    def __init__(self, row: dict):
        self.__table_name = row["TABLE_NAME"]
        self.__table_comment = row["TABLE_COMMENT"]
        self.__columns = []

    def add_column(self, column: Column):
        self.__columns.append(column)

    @property
    def table_name(self) -> str:
        return self.__table_name

    @property
    def get_table_comment(self) -> str:
        return self.__table_comment
