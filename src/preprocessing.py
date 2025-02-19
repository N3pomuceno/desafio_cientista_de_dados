# importações
import pandas as pd
import numpy as np
import re
from unidecode import unidecode
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s : %(message)s")
logger = logging.getLogger(__name__)


# Variáveis Globais
COLS_DADOS_CATEGORICOS = [
    'luz_eletrica',
    'obito',
    'em_situacao_de_rua',
    'possui_plano_saude',
    'vulnerabilidade_social',
    'familia_beneficiaria_auxilio_brasil',
    'crianca_matriculada_creche_pre_escola',
]

COLS_DADOS_DATA = [
    'data_cadastro',
    'data_nascimento',
    'data_atualizacao_cadastro',
    'updated_at',
]

COLS_DADOS_MULTIVALORADOS = [
    'meios_transporte',
    'doencas_condicoes',
    'meios_comunicacao',
    'em_caso_doenca_procura',
]


# Funções
def change_to_bool(val: str) -> int:
    return int(str(val).lower() in ["true", "1"])


def trata_registro(row):
    if pd.isna(row) or row == '[]':
        return None
    return [
        elem.strip(' "\'').encode('ISO-8859-1').decode('unicode_escape')
        for elem in row[1:-1].split(',')
    ] if row[0] == '[' else row.split(', ')


def verif_pressao(row: float | int, lim_inf: float, lim_sup: float):
    return False if lim_inf < row < lim_sup else True


def tratamento_cols(df_original: pd.DataFrame) -> pd.DataFrame:
    """Trata as colunas em relação as formatações necessárias para melhorar o dataset."""
    df = df_original.copy()

    for col in COLS_DADOS_CATEGORICOS:
        df[col] = df[col].map(change_to_bool)

    for col in COLS_DADOS_DATA:
        df[col] = pd.to_datetime(df[col], format='mixed')

    # Aplicação da função corrigida ao DataFrame
    for col in COLS_DADOS_MULTIVALORADOS:
        df[col] = df[col].apply(lambda x: trata_registro(x))
        df_explodido = df.explode(col)
        df = pd.get_dummies(df_explodido, columns=[col]).groupby(level=0).max()

    return df


def tratamento_inconsistencias(df_original: pd.DataFrame) -> pd.DataFrame:
    """Tratamento dos dados inconsistentes"""
    df = df_original.copy()

    valores_invalidos_religiao = [
        "ESB ALMIRANTE", "10 EAP 01", "ORQUIDEA", "Acomp. Cresc. e Desenv. da Criança", "Sim",
    ]
    valores_invalidos_renda_familiar = [
        "Manhã", "Internet",
    ]
    valores_invalidos_ident_genero = [
        "Não", "Sim", "Homossexual (gay / lésbica)", "Heterossexual", "Bissexual",
    ]
    valores_invalidos_sit_prof = [
        "Autônomo sem previdência social", "Autônomo com previdência social",
    ]
    df['raca_cor'] = df['raca_cor'].replace('Não', np.nan)
    df["religiao"] = df["religiao"].replace(valores_invalidos_religiao, np.nan)
    df["religiao"] = df["religiao"].replace("Não", "Sem religião")
    df["renda_familiar"] = df["renda_familiar"].replace(valores_invalidos_renda_familiar, np.nan)
    df["identidade_genero"] = df["identidade_genero"].replace(valores_invalidos_ident_genero, np.nan)
    df["situacao_profissional"] = df["situacao_profissional"].replace(valores_invalidos_sit_prof, "Autônomo")
    df["situacao_profissional"] = df["situacao_profissional"].replace("Médico Urologista", "Emprego Formal")
    df["situacao_profissional"] = df["situacao_profissional"].replace("SMS CAPS DIRCINHA E LINDA BATISTA AP 33", np.nan)

    q1, q3 = df['pressao_sistolica'].quantile([0.25, 0.75])
    intervalo_interquartil = (q3 - q1)
    PAS_limite_inf = q1 - 1.5*intervalo_interquartil
    PAS_limite_sup = q3 + 1.5*intervalo_interquartil

    q1, q3 = df['pressao_diastolica'].quantile([0.25, 0.75])
    intervalo_interquartil = (q3 - q1)
    PAD_limite_inf = q1 - 1.5*intervalo_interquartil
    PAD_limite_sup = q3 + 1.5*intervalo_interquartil

    # Verificando as pressões e criando a coluna de verificação para cada uma
    df['verificacao_pressao_sistolica'] = df.apply(lambda x: verif_pressao(x['pressao_sistolica'],
                                                                           PAS_limite_inf, PAS_limite_sup), axis=1)
    df['verificacao_pressao_diastolica'] = df.apply(lambda x: verif_pressao(x['pressao_diastolica'],
                                                                            PAD_limite_inf, PAD_limite_sup), axis=1)

    # Criando a terceira coluna para casos que precisam ser verificados
    df['verificacao_pressao'] = df['verificacao_pressao_sistolica'] | df['verificacao_pressao_diastolica']
    df.drop(['verificacao_pressao_sistolica', 'verificacao_pressao_diastolica'], axis=1, inplace=True)

    # Tratamendo de colunas extras.
    df.drop(['meios_comunicacao_3 Salários Mínimos',
             'meios_comunicacao_4 Salários Mínimos',
             'meios_comunicacao_Mais de 4 Salários Mínimos',
             'em_caso_doenca_procura_1 Salário Mínimo'], axis=1,
            inplace=True)
    return df


# Função para padronizar nomes das colunas
def padronizar_nome_coluna(nome):
    nome = unidecode(nome)  # Remove acentos
    nome = nome.lower()  # Converte para minúsculas
    nome = re.sub(r'[^a-z0-9_]', '_', nome)  # Substitui caracteres especiais por "_"
    nome = re.sub(r'_+', '_', nome).strip('_')  # Remove múltiplos "_" seguidos
    return nome


def main():
    try:
        logger.info("Iniciando pipeline de ETL...")
        logger.info("Realizando leitura dos dados")
        df = pd.read_csv(Path("./data/raw/dados_ficha_a_desafio.csv"), encoding="UTF-8")

        # Tratamento de colunas
        logger.info("Começando Tratamento de Colunas")
        df = tratamento_cols(df)

        # Tratamento de Inconsistências
        logger.info("Começando Tratamento de Inconsistências")
        df = tratamento_inconsistencias(df)

        # Tratamento dos nomes das colunas
        logger.info("Padronizando nome das colunas")
        df.columns = [padronizar_nome_coluna(col) for col in df.columns]
    except Exception as e:
        logger.error(f"Erro no pipeline: {e}", exc_info=True)

    # Criar o arquivo .csv transformado
    df.to_csv(Path("./data/processed/dados_ficha_a_desafio_processed.csv"), index=False)


if __name__ == "__main__":
    main()
