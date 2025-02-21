# Desafio - Ciência de Dados

## Objetivo

Neste desafio, realizamos a análise e transformação dos dados do arquivo `dados_ficha_a_desafio.csv`, identificando problemas e aplicando tratamentos adequados com DBT.

---

## Tarefas

### 1. Exploração e apontamento de problemas
- Analisamos cada campo do dataset, identificando padrões e inconsistências.
- Apontamos possíveis problemas e inferimos hipóteses sobre a origem dessas questões.
- Documentamos questionamentos relevantes para melhor compreensão dos dados.

### 2. Tratamento de dados com DBT
- Criamos um modelo DBT para padronizar os dados e gerar uma tabela tratada.
- Aplicamos boas práticas para garantir modularização e legibilidade do código.

---

## Como rodar o projeto

O projeto utiliza o gerenciador de pacotes [Poetry](https://python-poetry.org/) para instalar dependências. Embora o uso do Poetry não seja obrigatório, ele facilita a organização e o gerenciamento das bibliotecas. Atualmente, foi utilizada a versão `2.0.1`, mas versões anteriores, como `1.8.4`, também funcionam, com a diferença de que, após a instalação das dependências, é necessário ativar o ambiente virtual manualmente via `poetry shell`.

### Passo a passo para execução
1. **Coloque o arquivo de dados original no diretório** `data/raw/`.
2. **Instale as dependências do projeto**:
   ```bash
   poetry install
   ```
3. **Executar os scripts:**
   - Para abrir um Jupyter Notebook com anotações detalhadas:
     ```bash
     poetry run jupyter lab
     ```
   - Para executar o pré-processamento dos dados diretamente:
     ```bash
     poetry run python src/preprocessing.py
     ```

Caso prefira usar `pip`, o arquivo `requirements.txt` está atualizado. Para gerar um novo `requirements.txt` após adicionar dependências:
```bash
poetry run pip freeze > requirements.txt
```

---

## Análises

Para explorar o dataset transformado, siga as etapas anteriores para gerar o arquivo `.csv` tratado e, em seguida, execute o notebook `notebooks/eda.ipynb`. 

> **Nota:** O notebook está sem execução prévia (`clear output`) para evitar exposição dos dados.

---

## DBT

Para preparar o ambiente de banco de dados, utilizamos **Docker**. Antes de executar os comandos a seguir, certifique-se de ter o **Docker** instalado.

1. **Subir o container do banco de dados**:
   ```bash
   docker-compose up -d
   ```
2. **Inicializar o banco de dados com os dados originais**:
   ```bash
   poetry run python src/dbt_init.py
   ```
3. **Testar a conexão do DBT com o banco**:
   ```bash
   cd dbt_project
   poetry run dbt debug
   ```
4. **Executar as transformações no DBT**:
   ```bash
   cd dbt_project
   poetry run dbt run
   ```

### Limitações encontradas
O DBT foi utilizado para estruturar e transformar os dados no **PostgreSQL**, porém algumas transformações complexas (como tratamento de colunas multivaloradas) se mostraram consideravelmente problemáticas em SQL. Em particular, a divisão de certos campos foi parcialmente implementada, mas a abordagem completa exigiria transformações mais elaboradas, tornando o código menos eficiente e difícil de manter. 

Como alternativa, foi verificado online a possibilidade de usar DBT com **Python**, que permitiria reutilizar parte das transformações feitas anteriormente em Pandas, e para alguns adaptadores de DBT isso pode ser feito.

---

## Tecnologias utilizadas
- **Python** para análise exploratória e pré-processamento.
- **SQL** para manipulação dos dados.
- **DBT** (Data Build Tool) para transformação e modelagem dos dados.
- **Docker** para gerenciamento do banco de dados.

---

## Estrutura do Repositório
```
📦 desafio-ciencia-dados
┣ 📂 data/           → Local para armazenar os dados brutos e tratados.
┣ 📂 notebooks/      → Notebooks de análise exploratória.
┣ 📂 dbt_project/    → Arquivos de configuração e modelos do DBT.
┣ 📂 src/            → Scripts Python utilizados no projeto.
┣ 📜 README.md       → Documentação principal do projeto.
```
