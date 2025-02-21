-- models/pressao_limites.sql
WITH pressao_limites AS (
    SELECT
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY pressao_sistolica) AS PAS_q1,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY pressao_sistolica) AS PAS_q3,
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY pressao_diastolica) AS PAD_q1,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY pressao_diastolica) AS PAD_q3
    FROM {{ ref('fichas_transform') }}
)

SELECT * FROM pressao_limites
