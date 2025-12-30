def select_columns_info_query() -> str:
    """
    COLUMN_NAME                   컬럼 명
    COLUMN_COMMENT                컬럼 설명
    ORDINAL_POSITION              시각적 순서
    DATA_TYPE                     데이터 타입
    UDT_NAME                      PostgreSQL 고유 타입 명
    CHARACTER_MAXIMUM_LENGTH      문자열의 최대 길이
    NUMERIC_PRECISION             숫자형 데이터의 전체 자릿수와 소수점 자릿수
    IS_NULLABLE                   NULL 허용여부
    COLUMN_DEFAULT                기본 값
    IS_IDENTITY                   'ALWAYS' 또는 'BY DEFAULT'로 설정되어 자동 증가하는 pk인지 여부
    IS_GENERATED                  계산된 컬럼(Generated Column) 여부
    COLLATION_NAME                문자열 정렬 규칙
    DATETIME_PRECISION            타임스탬프의 밀리초 정밀도
    IS_PK                         PK 여부
    IS_FK                         FK 여부
    FOREIGN_TABLE_SCHEMA          참조 테이블 스키마 명
    FOREIGN_TABLE_NAME            참조 테이블 명
    FOREIGN_COLUMN_NAME           참조 컬럼 명
    UPDATE_RULE                   갱신 규칙 (갱신_및_삭제_규칙.xlsx 참조)
    DELETE_RULE                   삭제 규칙 (갱신_및_삭제_규칙.xlsx 참조)
    PK_CONSTRAINT_NAME            PK 제약조건 명
    FK_CONSTRAINT_NAME            FK 제약조건 명
    """

    return """
        WITH table_constraints AS (
            SELECT kcu.column_name
                 , tc.constraint_type
                 , rc.unique_constraint_schema AS referenced_table_schema
                 , pk_tc.table_name AS referenced_table_name
                 , pk_kcu.column_name AS referenced_column_name
                 , rc.update_rule
                 , rc.delete_rule
                 , rc.constraint_name AS fk_constraint_name
                 , tc.constraint_name AS pk_constraint_name
              FROM information_schema.table_constraints tc
             INNER JOIN information_schema.key_column_usage kcu
                ON tc.table_schema = kcu.table_schema
               AND tc.table_name = kcu.table_name
               AND tc.constraint_name = kcu.constraint_name
              LEFT OUTER JOIN information_schema.referential_constraints rc
                ON tc.table_schema = rc.constraint_schema
               AND tc.constraint_name = rc.constraint_name
              LEFT OUTER JOIN information_schema.key_column_usage pk_kcu
                ON rc.unique_constraint_schema = pk_kcu.table_schema
               AND rc.UNIQUE_constraint_name = pk_kcu.constraint_name
               AND kcu.position_in_unique_constraint = pk_kcu.ordinal_position
              LEFT OUTER JOIN information_schema.table_constraints pk_tc
                ON pk_kcu.table_schema = pk_tc.table_schema
               AND pk_kcu.constraint_name = pk_tc.constraint_name
             WHERE tc.table_schema = %s
               AND tc.table_name   = %s
        )
        SELECT c.column_name                                                                   AS "COLUMN_NAME"
             , (SELECT d.description 
                  FROM pg_catalog.pg_description d
                 INNER JOIN pg_catalog.pg_attribute a
                    ON a.attrelid = d.objoid
                   AND a.attnum = d.objsubid
                 INNER JOIN pg_catalog.pg_class t
                    ON t.oid = a.attrelid
                 INNER JOIN pg_catalog.pg_namespace n
                    ON n.oid = t.relnamespace
                 WHERE n.nspname = C.table_schema 
                   AND t.relname = C.table_name 
                   AND a.attname = C.column_name
               )                                                                                AS "COLUMN_COMMENT"
             , c.ordinal_position                                                               AS "ORDINAL_POSITION"
             , c.data_type                                                                      AS "DATA_TYPE"
             , c.udt_name                                                                       AS "UDT_NAME"
             , c.character_maximum_length                                                       AS "CHARACTER_MAXIMUM_LENGTH"
             , c.numeric_precision                                                              AS "NUMERIC_PRECISION"
             , c.is_nullable                                                                    AS "IS_NULLABLE"
             , c.column_default                                                                 AS "COLUMN_DEFAULT"
             , CASE WHEN c.is_identity = 'YES' OR c.column_default LIKE 'nextval(%%' THEN 'T' 
                    ELSE 'F' 
                END                                                                             AS "IS_IDENTITY"
             , CASE WHEN c.is_generated = 'ALWAYS' THEN 'T'
                    ELSE 'F'
                END                                                                             AS "IS_GENERATED"
             , c.collation_name                                                                 AS "COLLATION_NAME"
             , c.datetime_precision                                                             AS "DATETIME_PRECISION"
             , MAX(CASE WHEN tc.constraint_type = 'PRIMARY KEY' THEN 'T' ELSE 'F' END)          AS "IS_PK"
             , MAX(CASE WHEN tc.constraint_type = 'FOREIGN KEY' THEN 'T' ELSE 'F' END)          AS "IS_FK"
             , MAX(tc.referenced_table_schema)                                                  AS "FOREIGN_TABLE_SCHEMA"
             , MAX(tc.referenced_table_name)                                                    AS "FOREIGN_TABLE_NAME"
             , MAX(tc.referenced_column_name)                                                   AS "FOREIGN_COLUMN_NAME"
             , MAX(tc.update_rule)                                                              AS "UPDATE_RULE"
             , MAX(tc.delete_rule)                                                              AS "DELETE_RULE"
             , MAX(tc.pk_constraint_name)                                                       AS "PK_CONSTRAINT_NAME"
             , MAX(tc.fk_constraint_name)                                                       AS "FK_CONSTRAINT_NAME"
          FROM information_schema.columns c
          LEFT OUTER JOIN table_constraints tc 
            ON c.column_name = tc.column_name
         WHERE c.table_schema = %s
           AND c.table_name   = %s
         GROUP BY c.table_schema
             , c.table_name
             , c.column_name
             , c.ordinal_position
             , c.data_type
             , c.udt_name
             , c.character_maximum_length
             , c.numeric_precision
             , c.is_nullable
             , c.column_default
             , c.is_identity
             , c.is_generated
             , c.collation_name
             , c.datetime_precision
         ORDER BY c.ordinal_position;
    """
