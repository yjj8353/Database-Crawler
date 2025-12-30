def select_columns_query() -> str:
    return """
            SELECT table_name 				-- 테이블 명
                 , column_name 				-- 컬럼 명 
                 , ordinal_position 		-- 시각적 순서
                 , data_type 				-- 데이터 타입
                 , udt_name 				-- PostgreSQL 고유 타입 명 
                 , character_maximum_length -- 문자열의 최대 길이
                 , numeric_precision 		-- 숫자형 데이터의 전체 자릿수와 소수점 자릿수
                 , is_nullable 				-- NULL 허용여부
                 , column_default 			-- 기본 값
                 , is_identity 				-- 'ALWAYS' 또는 'BY DEFAULT'로 설정되어 자동 증가하는 PK인지 여부
                 , is_generated 			-- 계산된 컬럼(Generated Column) 여부
                 , collation_name 			-- 문자열 정렬 규칙
                 , datetime_precision 		-- 타임스탬프의 밀리초 정밀도
              FROM information_schema.columns
             WHERE table_schema = %s
               AND table_name   = %s
             ORDER BY ordinal_position;
            """


def select_pk_query() -> str:
    return """
            SELECT kcu.column_name
              FROM information_schema.table_constraints tc
             INNER JOIN information_schema.key_column_usage kcu
                ON tc.constraint_name = kcu.constraint_name
               AND tc.constraint_schema = kcu.constraint_schema
             WHERE tc.constraint_type = 'PRIMARY KEY'
               AND tc.table_schema    = %s
               AND tc.table_name      = %s
             ORDER BY kcu.ordinal_position;
            """


def select_fk_query() -> str:
    return """
            SELECT kcu.column_name                          -- FK 컬럼 명
                 , ccu.table_schema AS foreign_table_schema -- 참조 테이블 스키마 명
                 , ccu.table_name   AS foreign_table_name   -- 참조 테이블 명
                 , ccu.column_name  AS foreign_column_name  -- 참조 컬럼 명
                 , rc.update_rule                           -- 갱신 규칙 (갱신_및_삭제_규칙.xlsx 참조)
                 , rc.delete_rule                           -- 삭제 규칙 (갱신_및_삭제_규칙.xlsx 참조)
                 , tc.constraint_name                       -- 제약조건 명
              FROM information_schema.table_constraints tc
             INNER JOIN information_schema.key_column_usage kcu
                ON tc.constraint_name = kcu.constraint_name
               AND tc.constraint_schema = kcu.constraint_schema
             INNER JOIN information_schema.referential_constraints rc
                ON tc.constraint_name = rc.constraint_name
               AND tc.constraint_schema = rc.constraint_schema
             INNER JOIN information_schema.constraint_column_usage ccu
                ON rc.unique_constraint_name = ccu.constraint_name
               AND rc.unique_constraint_schema = ccu.constraint_schema
             WHERE tc.constraint_type = 'FOREIGN KEY'
               AND tc.table_schema    = %s
               AND tc.table_name      = %s
             ORDER BY tc.constraint_name, kcu.ordinal_position;
            """


def select_columns_info_query() -> str:
    return """
        WITH TABLE_CONSTRAINTS AS (
            SELECT KCU.COLUMN_NAME
                 , TC.CONSTRAINT_TYPE
                 , RC.UNIQUE_CONSTRAINT_SCHEMA AS REFERENCED_TABLE_SCHEMA
                 , PK_TC.TABLE_NAME AS REFERENCED_TABLE_NAME
                 , PK_KCU.COLUMN_NAME AS REFERENCED_COLUMN_NAME
                 , RC.UPDATE_RULE
                 , RC.DELETE_RULE
                 , RC.CONSTRAINT_NAME AS FK_CONSTRAINT_NAME
                 , TC.CONSTRAINT_NAME AS PK_CONSTRAINT_NAME
            FROM information_schema.TABLE_CONSTRAINTS TC
           INNER JOIN information_schema.KEY_COLUMN_USAGE KCU
              ON TC.TABLE_SCHEMA = KCU.TABLE_SCHEMA
             AND TC.TABLE_NAME = KCU.TABLE_NAME
             AND TC.CONSTRAINT_NAME = KCU.CONSTRAINT_NAME
            LEFT OUTER JOIN information_schema.REFERENTIAL_CONSTRAINTS RC
              ON TC.TABLE_SCHEMA = RC.CONSTRAINT_SCHEMA
             AND TC.CONSTRAINT_NAME = RC.CONSTRAINT_NAME
            LEFT OUTER JOIN information_schema.KEY_COLUMN_USAGE PK_KCU
              ON RC.UNIQUE_CONSTRAINT_SCHEMA = PK_KCU.TABLE_SCHEMA
             AND RC.UNIQUE_CONSTRAINT_NAME = PK_KCU.CONSTRAINT_NAME
             AND KCU.POSITION_IN_UNIQUE_CONSTRAINT = PK_KCU.ORDINAL_POSITION
            LEFT OUTER JOIN information_schema.TABLE_CONSTRAINTS PK_TC
              ON PK_KCU.TABLE_SCHEMA = PK_TC.TABLE_SCHEMA
             AND PK_KCU.CONSTRAINT_NAME = PK_TC.CONSTRAINT_NAME
           WHERE TC.TABLE_SCHEMA = %s
             AND TC.TABLE_NAME   = %s
        )
        SELECT C.COLUMN_NAME AS "COLUMN_NAME"
             , (SELECT d.description 
                  FROM pg_catalog.pg_description d
                 INNER JOIN pg_catalog.pg_attribute a ON a.attrelid = d.objoid AND a.attnum = d.objsubid
                 INNER JOIN pg_catalog.pg_class t ON t.oid = a.attrelid
                 INNER JOIN pg_catalog.pg_namespace n ON n.oid = t.relnamespace
                 WHERE n.nspname = C.TABLE_SCHEMA 
                   AND t.relname = C.TABLE_NAME 
                   AND a.attname = C.COLUMN_NAME
               ) AS "COLUMN_COMMENT"
             , C.ORDINAL_POSITION AS "ORDINAL_POSITION"
             , C.DATA_TYPE AS "DATA_TYPE"
             , C.UDT_NAME AS "UDT_NAME"
             , C.CHARACTER_MAXIMUM_LENGTH AS "CHARACTER_MAXIMUM_LENGTH"
             , C.NUMERIC_PRECISION AS "NUMERIC_PRECISION"
             , C.IS_NULLABLE AS "IS_NULLABLE"
             , C.COLUMN_DEFAULT AS "COLUMN_DEFAULT"
             , CASE WHEN C.IS_IDENTITY = 'YES' OR C.COLUMN_DEFAULT LIKE 'nextval(%%' THEN 'T' 
                    ELSE 'F' 
                END AS "IS_IDENTITY"
             , CASE WHEN C.IS_GENERATED = 'ALWAYS' THEN 'T' ELSE 'F' END AS "IS_GENERATED"
             , C.COLLATION_NAME AS "COLLATION_NAME"
             , C.DATETIME_PRECISION AS "DATETIME_PRECISION"
             , MAX(CASE WHEN TC.CONSTRAINT_TYPE = 'PRIMARY KEY' THEN 'T' ELSE 'F' END) AS "IS_PK"
             , MAX(CASE WHEN TC.CONSTRAINT_TYPE = 'FOREIGN KEY' THEN 'T' ELSE 'F' END) AS "IS_FK"
             , MAX(TC.REFERENCED_TABLE_SCHEMA) AS "FOREIGN_TABLE_SCHEMA"
             , MAX(TC.REFERENCED_TABLE_NAME) AS "FOREIGN_TABLE_NAME"
             , MAX(TC.REFERENCED_COLUMN_NAME) AS "FOREIGN_COLUMN_NAME"
             , MAX(TC.UPDATE_RULE) AS "UPDATE_RULE"
             , MAX(TC.DELETE_RULE) AS "DELETE_RULE"
             , MAX(TC.FK_CONSTRAINT_NAME) AS "FK_CONSTRAINT_NAME"
             , MAX(TC.PK_CONSTRAINT_NAME) AS "PK_CONSTRAINT_NAME"
        FROM information_schema.COLUMNS C
        LEFT JOIN TABLE_CONSTRAINTS TC 
          ON C.COLUMN_NAME = TC.COLUMN_NAME
        WHERE C.TABLE_SCHEMA = %s
          AND C.TABLE_NAME   = %s
        GROUP BY C.TABLE_SCHEMA, C.TABLE_NAME, C.COLUMN_NAME, C.ORDINAL_POSITION
            , C.DATA_TYPE, C.UDT_NAME, C.CHARACTER_MAXIMUM_LENGTH, C.NUMERIC_PRECISION
            , C.IS_NULLABLE, C.COLUMN_DEFAULT, C.IS_IDENTITY, C.IS_GENERATED
            , C.COLLATION_NAME, C.DATETIME_PRECISION
        ORDER BY C.ORDINAL_POSITION;
    """
