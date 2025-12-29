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
               AND tc.table_schema = %s
               AND tc.table_name   = %s
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
               AND tc.table_schema = %s
               AND tc.table_name   = %s
             ORDER BY tc.constraint_name, kcu.ordinal_position;
            """
