WITH fichas_raw AS (
    SELECT
        *,
        -- Converte colunas categóricas para 0/1
        CASE WHEN luz_eletrica IN ('true', '1') THEN 1 ELSE 0 END AS luz_eletrica_binario,
        CASE WHEN obito IN ('true', '1') THEN 1 ELSE 0 END AS obito_binario,
        CASE WHEN em_situacao_de_rua IN ('true', '1') THEN 1 ELSE 0 END AS em_situacao_de_rua_binario,
        CASE WHEN possui_plano_saude IN ('true', '1') THEN 1 ELSE 0 END AS possui_plano_saude_binario,
        CASE WHEN vulnerabilidade_social IN ('true', '1') THEN 1 ELSE 0 END AS vulnerabilidade_social_binario,
        CASE WHEN familia_beneficiaria_auxilio_brasil IN ('true', '1') THEN 1 ELSE 0 END AS familia_beneficiaria_auxilio_brasil_binario,
        CASE WHEN crianca_matriculada_creche_pre_escola IN ('true', '1') THEN 1 ELSE 0 END AS crianca_matriculada_creche_pre_escola_binario,

        -- Converte datas para o formato correto
        TO_TIMESTAMP(data_cadastro, 'YYYY-MM-DD HH24:MI:SS.MS')::timestamp AS data_cadastro_formatada,
        TO_DATE(data_nascimento, 'YYYY-MM-DD')::date AS data_nascimento_formatada,    
        TO_TIMESTAMP(data_atualizacao_cadastro, 'YYYY-MM-DD HH24:MI:SS.MS')::timestamp AS data_atualizacao_cadastro_formatada,
        TO_TIMESTAMP(updated_at, 'YYYY-MM-DD HH24:MI:SS.MS')::timestamp AS updated_at_formatada,

        -- Corrige valores inválidos
        NULLIF(raca_cor, 'Não') AS raca_cor_tratada,
        NULLIF(
            CASE 
                WHEN religiao IN ('ESB ALMIRANTE', '10 EAP 01', 'ORQUIDEA', 'Acomp. Cresc. e Desenv. da Criança', 'Sim') THEN NULL
                WHEN religiao = 'Não' THEN 'Sem religião'
                ELSE religiao 
            END, ''
        ) AS religiao_tratada,
        
        NULLIF(
            CASE 
                WHEN renda_familiar IN ('Manhã', 'Internet') THEN NULL 
                ELSE renda_familiar
            END, ''
        ) AS renda_familiar_tratada,

        NULLIF(
            CASE 
                WHEN identidade_genero IN ('Não', 'Sim', 'Homossexual (gay / lésbica)', 'Heterossexual', 'Bissexual') THEN NULL 
                ELSE identidade_genero
            END, ''
        ) AS identidade_genero_tratada,

        CASE 
            WHEN situacao_profissional IN ('Autônomo sem previdência social', 'Autônomo com previdência social') THEN 'Autônomo'
            WHEN situacao_profissional = 'Médico Urologista' THEN 'Emprego Formal'
            WHEN situacao_profissional = 'SMS CAPS DIRCINHA E LINDA BATISTA AP 33' THEN NULL
            ELSE situacao_profissional
        END AS situacao_profissional_tratada
    FROM public.fichas
)

Select * from fichas_raw