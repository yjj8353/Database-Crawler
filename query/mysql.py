def select_columns_query() -> str:
    return """
            SELECT TABLE_NAME                                        -- 테이블 명
                 , COLUMN_NAME                                       -- 컬럼 명
                 , ORDINAL_POSITION                                  -- 시각적 순서
                 , DATA_TYPE                                         -- 데이터 타입
                 , COLUMN_TYPE AS udt_name                           -- MySQL 고유 타입 명 (예: varchar(255))
                 , CHARACTER_MAXIMUM_LENGTH                          -- 문자열의 최대 길이
                 , NUMERIC_PRECISION                                 -- 숫자형 정밀도
                 , IS_NULLABLE                                       -- NULL 허용여부
                 , COLUMN_DEFAULT                                    -- 기본 값
                 , (EXTRA LIKE '%%auto_increment%%') AS is_identity  -- 자동 증가 여부
                 , (CASE WHEN GENERATION_EXPRESSION IS NOT NULL AND GENERATION_EXPRESSION <> '' 
                         THEN 'YES' ELSE 'NO' 
                     END) AS is_generated
                 , COLLATION_NAME                                    -- 문자열 정렬 규칙
                 , DATETIME_PRECISION                                -- 타임스탬프 정밀도
              FROM information_schema.COLUMNS
             WHERE TABLE_NAME = %s
             ORDER BY ORDINAL_POSITION;
            """


def select_pk_query() -> str:
    return """
            SELECT kcu.COLUMN_NAME
              FROM information_schema.TABLE_CONSTRAINTS tc
             INNER JOIN information_schema.KEY_COLUMN_USAGE kcu
                ON tc.CONSTRAINT_NAME = kcu.CONSTRAINT_NAME
               AND tc.TABLE_SCHEMA    = kcu.TABLE_SCHEMA
               AND tc.TABLE_NAME      = kcu.TABLE_NAME
             WHERE tc.CONSTRAINT_TYPE = 'PRIMARY KEY'
               AND tc.TABLE_NAME      = %s
             ORDER BY kcu.ORDINAL_POSITION;
            """


def select_fk_query() -> str:
    return """
            SELECT kcu.COLUMN_NAME                                     -- FK 컬럼 명 (로컬)
                 , kcu.REFERENCED_TABLE_SCHEMA AS foreign_table_schema -- 참조 테이블 스키마 명
                 , kcu.REFERENCED_TABLE_NAME   AS foreign_table_name   -- 참조 테이블 명
                 , kcu.REFERENCED_COLUMN_NAME  AS foreign_column_name  -- 참조 컬럼 명
                 , rc.UPDATE_RULE                                      -- 갱신 규칙
                 , rc.DELETE_RULE                                      -- 삭제 규칙
                 , tc.CONSTRAINT_NAME                                  -- 제약조건 명
              FROM information_schema.TABLE_CONSTRAINTS tc
             INNER JOIN information_schema.KEY_COLUMN_USAGE kcu
                ON tc.CONSTRAINT_NAME = kcu.CONSTRAINT_NAME
               AND tc.TABLE_SCHEMA    = kcu.TABLE_SCHEMA
               AND tc.TABLE_NAME      = kcu.TABLE_NAME
             LEFT JOIN information_schema.REFERENTIAL_CONSTRAINTS rc
                ON rc.CONSTRAINT_NAME = tc.CONSTRAINT_NAME
               AND rc.CONSTRAINT_SCHEMA = tc.TABLE_SCHEMA
             WHERE tc.CONSTRAINT_TYPE = 'FOREIGN KEY'
               AND tc.TABLE_NAME      = %s
             ORDER BY tc.CONSTRAINT_NAME, kcu.ORDINAL_POSITION;
            """
