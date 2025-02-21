import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s : %(message)s")
logger = logging.getLogger(__name__)

def load_environment_variables():
    # Recarrega o .env
    load_dotenv()
    return {
        "POSTGRES_USER": os.getenv("POSTGRES_USER"),
        "POSTGRES_PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "POSTGRES_DB": os.getenv("POSTGRES_DB"),
        "POSTGRES_HOST": os.getenv("POSTGRES_HOST"),
        "POSTGRES_PORT": os.getenv("POSTGRES_PORT"),
        "TABLE_NAME": os.getenv("TABLE_NAME"),
    }


def get_database_engine(env_vars):
    database_url = (
        f"postgresql://{env_vars['POSTGRES_USER']}:"
        f"{env_vars['POSTGRES_PASSWORD']}@"
        f"{env_vars['POSTGRES_HOST']}:"
        f"{env_vars['POSTGRES_PORT']}/"
        f"{env_vars['POSTGRES_DB']}"
    )
    return create_engine(database_url)


def save_to_database(df, table_name, engine):
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)


def main():
    logger.info("Definindo variáveis de ambiente")
    env_vars = load_environment_variables()
    engine = get_database_engine(env_vars)

    logger.info("Carregando dados para o banco de dados")
    df = pd.read_csv('data/raw/dados_ficha_a_desafio.csv')
    save_to_database(df, env_vars["TABLE_NAME"], engine)
    logger.info("Dados carregados com sucesso!")


if __name__ == "__main__":
    main()
