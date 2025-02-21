-- models/fichas_tratadas.sql
WITH fichas_lida_pressao AS (
    SELECT
        f.*,
        CASE 
            WHEN (f.pressao_sistolica < l.PAS_q1 - 1.5 * (l.PAS_q3 - l.PAS_q1)) 
              OR (f.pressao_sistolica > l.PAS_q3 + 1.5 * (l.PAS_q3 - l.PAS_q1)) 
            THEN TRUE ELSE FALSE 
        END AS verificacao_pressao_sistolica,

        CASE 
            WHEN (f.pressao_diastolica < l.PAD_q1 - 1.5 * (l.PAD_q3 - l.PAD_q1)) 
              OR (f.pressao_diastolica > l.PAD_q3 + 1.5 * (l.PAD_q3 - l.PAD_q1)) 
            THEN TRUE ELSE FALSE 
        END AS verificacao_pressao_diastolica,

        -- Verificação de pressão combinada
        CASE
            WHEN 
                (f.pressao_sistolica < l.PAS_q1 - 1.5 * (l.PAS_q3 - l.PAS_q1) OR f.pressao_sistolica > l.PAS_q3 + 1.5 * (l.PAS_q3 - l.PAS_q1))
                OR 
                (f.pressao_diastolica < l.PAD_q1 - 1.5 * (l.PAD_q3 - l.PAD_q1) OR f.pressao_diastolica > l.PAD_q3 + 1.5 * (l.PAD_q3 - l.PAD_q1))
            THEN TRUE 
            ELSE FALSE 
        END AS verificacao_pressao
    FROM {{ ref('fichas_transform') }} f
    CROSS JOIN {{ ref('pressao_limites') }} l
)

SELECT * FROM fichas_lida_pressao
