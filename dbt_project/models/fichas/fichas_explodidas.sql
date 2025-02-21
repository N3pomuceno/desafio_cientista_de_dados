-- models/dados_explodidos.sql

WITH dados_explodidos AS (
    SELECT 
        f.*, 
        -- Explode os meios de transporte e realiza o tratamento da string
        TRIM(
            REPLACE(
                REPLACE(
                    REPLACE(
                        REPLACE(unnest(string_to_array(f.meios_transporte, ',')), '"', ''),   -- Remove aspas duplas
                        '''', ''),                            -- Remove aspas simples (corrigido com duas aspas simples)
                    '[', ''),                                  -- Remove colchetes de abertura
                ']', '')                                    -- Remove colchetes de fechamento
        ) AS meios_transporte_tratado,
        
        -- Substitui as sequências Unicode pelos valores corretos
        REPLACE(
            REPLACE(
                TRIM(
                    REPLACE(
                        REPLACE(
                            REPLACE(
                                REPLACE(unnest(string_to_array(f.meios_transporte, ',')), '"', ''), 
                                '''', ''), 
                            '[', ''),
                        ']', '')
                ),
                '\u00d4nibus', 'Ônibus'),   -- Substitui \u00d4nibus por Ônibus
            'Metr\u00f4', 'Metrô') AS meios_transporte_final
    FROM {{ ref('fichas_lida_pressao') }} f
)

SELECT * FROM dados_explodidos
