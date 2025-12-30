def select_columns_info_query():
    """
        COLUMN_NAME                   컬럼 명
        COLUMN_COMMENT                컬럼 설명
        ORDINAL_POSITION              시각적 순서
        DATA_TYPE                     데이터 타입
        UDT_NAME                      고유 타입 명 (Oracle에서는 사용자 정의 타입인 경우만 해당함)
        CHARACTER_MAXIMUM_LENGTH      문자열의 최대 길이
        NUMERIC_PRECISION             숫자형 데이터의 전체 자릿수와 소수점 자릿수
        IS_NULLABLE                   NULL 허용여부
        COLUMN_DEFAULT                기본 값
        IS_IDENTITY                   자동 증가하는 pk인지 여부
        IS_GENERATED                  계산된 컬럼 여부
        COLLATION_NAME                문자열 정렬 규칙
        DATETIME_PRECISION            타임스탬프의 밀리초 정밀도
        IS_PK                         PK 여부
        IS_FK                         FK 여부
        FOREIGN_TABLE_SCHEMA          참조 테이블 스키마 명
        FOREIGN_TABLE_NAME            참조 테이블 명
        FOREIGN_COLUMN_NAME           참조 컬럼 명
        UPDATE_RULE                   갱신 규칙 (Oracle에서는 사용하지 않음)
        DELETE_RULE                   삭제 규칙 (갱신_및_삭제_규칙.xlsx 참조)
        PK_CONSTRAINT_NAME            PK 제약조건 명
        FK_CONSTRAINT_NAME            FK 제약조건 명
        """

    return """
        WITH TABLE_CONSTRAINTS AS (
            SELECT ACC.OWNER
                 , ACC.TABLE_NAME
                 , ACC.COLUMN_NAME
                 , MAX(CASE WHEN AC.CONSTRAINT_TYPE = 'P' THEN 'T' ELSE 'F' END) AS IS_PK
                 , MAX(CASE WHEN AC.CONSTRAINT_TYPE = 'R' THEN 'T' ELSE 'F' END) AS IS_FK
                 , MAX(RAC.OWNER) AS FOREIGN_TABLE_SCHEMA
                 , MAX(RAC.TABLE_NAME) AS FOREIGN_TABLE_NAME
                 , MAX(RAC.COLUMN_NAME) AS FOREIGN_COLUMN_NAME
                 , MAX(AC.DELETE_RULE) AS DELETE_RULE
                 , MAX(CASE WHEN AC.CONSTRAINT_TYPE = 'P' THEN AC.CONSTRAINT_NAME END) AS PK_CONSTRAINT_NAME
                 , MAX(CASE WHEN AC.CONSTRAINT_TYPE = 'R' THEN AC.CONSTRAINT_NAME END) AS FK_CONSTRAINT_NAME
              FROM ALL_CONSTRAINTS AC
             INNER JOIN ALL_CONS_COLUMNS ACC 
                ON AC.OWNER = ACC.OWNER 
               AND AC.CONSTRAINT_NAME = ACC.CONSTRAINT_NAME
              LEFT OUTER JOIN ALL_CONS_COLUMNS RAC 
                ON AC.R_OWNER = RAC.OWNER 
               AND AC.R_CONSTRAINT_NAME = RAC.CONSTRAINT_NAME
               AND ACC.POSITION = RAC.POSITION
             WHERE AC.OWNER = :owner
               AND AC.TABLE_NAME = :table_name
             GROUP BY ACC.OWNER
                 , ACC.TABLE_NAME
                 , ACC.COLUMN_NAME
        )
        SELECT C.COLUMN_NAME
             , COMM.COMMENTS                                                               AS COLUMN_COMMENT
             , C.COLUMN_ID                                                                 AS ORDINAL_POSITION
             , C.DATA_TYPE
             , C.DATA_TYPE                                                                 AS UDT_NAME
             , CASE WHEN C.DATA_TYPE IN ('CHAR', 'VARCHAR2', 'RAW') THEN C.DATA_LENGTH END AS CHARACTER_MAXIMUM_LENGTH
             , C.DATA_PRECISION                                                            AS NUMERIC_PRECISION
             , CASE WHEN C.NULLABLE = 'Y' THEN 'YES' ELSE 'NO' END                         AS IS_NULLABLE
             , C.DATA_DEFAULT                                                              AS COLUMN_DEFAULT
             , CASE WHEN C.IDENTITY_COLUMN = 'YES' THEN 'T' ELSE 'F' END                   AS IS_IDENTITY
             , CASE WHEN C.VIRTUAL_COLUMN = 'YES' THEN 'T' ELSE 'F' END                    AS IS_GENERATED
             , (SELECT VALUE FROM NLS_DATABASE_PARAMETERS WHERE PARAMETER = 'NLS_SORT')	   AS COLLATION_NAME
             , C.DATA_SCALE                                                                AS DATETIME_PRECISION
             , NVL(TC.IS_PK, 'F')                                                          AS IS_PK
             , NVL(TC.IS_FK, 'F')                                                          AS IS_FK
             , TC.FOREIGN_TABLE_SCHEMA
             , TC.FOREIGN_TABLE_NAME
             , TC.FOREIGN_COLUMN_NAME
             , NULL                                                                        AS UPDATE_RULE
             , TC.DELETE_RULE
             , TC.PK_CONSTRAINT_NAME
             , TC.FK_CONSTRAINT_NAME 
          FROM ALL_TAB_COLS C
          LEFT OUTER JOIN ALL_COL_COMMENTS COMM
            ON C.OWNER = COMM.OWNER
           AND C.TABLE_NAME = COMM.TABLE_NAME
           AND C.COLUMN_NAME = COMM.COLUMN_NAME
          LEFT OUTER JOIN TABLE_CONSTRAINTS TC 
            ON C.OWNER = TC.OWNER
           AND C.TABLE_NAME = TC.TABLE_NAME
           AND C.COLUMN_NAME = TC.COLUMN_NAME
         WHERE C.OWNER = :owner
           AND C.TABLE_NAME = :table_name
           AND C.HIDDEN_COLUMN = 'NO'
         ORDER BY C.COLUMN_ID
    """