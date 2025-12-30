def select_columns_info_query():
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
        IS_IDENTITY                   자동 증가하는 pk인지 여부
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
        WITH TABLE_CONSTRAINTS AS (
            SELECT KCU.COLUMN_NAME
                 , TC.CONSTRAINT_TYPE
                 , KCU.REFERENCED_TABLE_SCHEMA
                 , KCU.REFERENCED_TABLE_NAME
                 , KCU.REFERENCED_COLUMN_NAME
                 , RC.UPDATE_RULE
                 , RC.DELETE_RULE
                 , RC.CONSTRAINT_NAME AS FK_CONSTRAINT_NAME
                 , TC.CONSTRAINT_NAME AS PK_CONSTRAINT_NAME
             FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS TC
            INNER JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE KCU
               ON TC.TABLE_SCHEMA    = %s
              AND TC.TABLE_NAME      = %s
              AND TC.CONSTRAINT_NAME = KCU.CONSTRAINT_NAME
             LEFT OUTER JOIN INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS RC
               ON TC.TABLE_SCHEMA    = RC.CONSTRAINT_SCHEMA
              AND TC.TABLE_NAME      = RC.TABLE_NAME
              AND TC.CONSTRAINT_NAME = RC.CONSTRAINT_NAME
        )
        SELECT C.COLUMN_NAME
             , C.COLUMN_COMMENT
             , C.ORDINAL_POSITION
             , C.DATA_TYPE
             , C.COLUMN_TYPE AS UDT_NAME
             , C.CHARACTER_MAXIMUM_LENGTH
             , C.NUMERIC_PRECISION
             , C.IS_NULLABLE
             , C.COLUMN_DEFAULT
             , CASE WHEN C.EXTRA LIKE '%auto_increment%' THEN 'T'
                    ELSE 'F'
                END AS IS_IDENTITY
             , CASE WHEN C.GENERATION_EXPRESSION IS NOT NULL AND C.GENERATION_EXPRESSION <> '' THEN 'T'
                    ELSE 'F'
                END AS IS_GENERATED
             , C.COLLATION_NAME
             , C.DATETIME_PRECISION
             , MAX(CASE WHEN TC.CONSTRAINT_TYPE = 'PRIMARY KEY' THEN 'T' ELSE 'F' END) AS IS_PK
             , MAX(CASE WHEN TC.CONSTRAINT_TYPE = 'FOREIGN KEY' THEN 'T' ELSE 'F' END) AS IS_FK
             , MAX(TC.REFERENCED_TABLE_SCHEMA) AS FOREIGN_TABLE_SCHEMA
             , MAX(TC.REFERENCED_TABLE_NAME) AS FOREIGN_TABLE_NAME
             , MAX(TC.REFERENCED_COLUMN_NAME) AS FOREIGN_COLUMN_NAME
             , MAX(TC.UPDATE_RULE) AS UPDATE_RULE
             , MAX(TC.DELETE_RULE) AS DELETE_RULE
             , MAX(TC.FK_CONSTRAINT_NAME) AS FK_CONSTRAINT_NAME
             , MAX(TC.PK_CONSTRAINT_NAME) AS PK_CONSTRAINT_NAME
          FROM INFORMATION_SCHEMA.COLUMNS C
          LEFT OUTER JOIN TABLE_CONSTRAINTS TC 
            ON C.COLUMN_NAME = TC.COLUMN_NAME
         WHERE C.TABLE_SCHEMA = %s
           AND C.TABLE_NAME   = %s
         GROUP BY C.COLUMN_NAME
             , C.COLUMN_COMMENT
             , C.ORDINAL_POSITION
             , C.DATA_TYPE
             , C.COLUMN_TYPE
             , C.CHARACTER_MAXIMUM_LENGTH
             , C.NUMERIC_PRECISION
             , C.IS_NULLABLE
             , C.COLUMN_DEFAULT
             , C.EXTRA
             , C.GENERATION_EXPRESSION 
             , C.COLLATION_NAME 
             , C.DATETIME_PRECISION
         ORDER BY C.ORDINAL_POSITION;
    """