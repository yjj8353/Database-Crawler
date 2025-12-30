from typing import Optional


class Column:
    __column_name: str
    __column_comment: Optional[str]
    __ordinal_position: int
    __data_type: str
    __udt_name: str
    __character_maximum_length: Optional[int]
    __numeric_precision: Optional[int]
    __is_nullable: str
    __column_default: Optional[str]
    __is_identity: bool
    __is_generated: bool
    __collation_name: Optional[str]
    __datetime_precision: Optional[int]
    __is_pk: bool
    __is_fk: bool
    __foreign_table_schema: Optional[str]
    __foreign_table_name: Optional[str]
    __foreign_column_name: Optional[str]
    __update_rule: Optional[str]
    __delete_rule: Optional[str]
    __pk_constraint_name: Optional[str]
    __fk_constraint_name: Optional[str]

    def __init__(self, row: dict):
        self.__column_name = row["COLUMN_NAME"]
        self.__column_comment = row["COLUMN_COMMENT"]
        self.__ordinal_position = row["ORDINAL_POSITION"]
        self.__data_type = row["DATA_TYPE"]
        self.__udt_name = row["UDT_NAME"]
        self.__character_maximum_length = row["CHARACTER_MAXIMUM_LENGTH"]
        self.__numeric_precision = row["NUMERIC_PRECISION"]
        self.__is_nullable = row["IS_NULLABLE"]
        self.__column_default = row["COLUMN_DEFAULT"]
        self.__is_identity = row["IS_IDENTITY"]
        self.__is_generated = row["IS_GENERATED"]
        self.__collation_name = row["COLLATION_NAME"]
        self.__datetime_precision = row["DATETIME_PRECISION"]
        self.__is_pk = row["IS_PK"]
        self.__is_fk = row["IS_FK"]
        self.__foreign_table_schema = row["FOREIGN_TABLE_SCHEMA"]
        self.__foreign_table_name = row["FOREIGN_TABLE_NAME"]
        self.__foreign_column_name = row["FOREIGN_COLUMN_NAME"]
        self.__update_rule = row["UPDATE_RULE"]
        self.__delete_rule = row["DELETE_RULE"]
        self.__pk_constraint_name = row["PK_CONSTRAINT_NAME"]
        self.__fk_constraint_name = row["FK_CONSTRAINT_NAME"]

