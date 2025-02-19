# Desafio - Ciência de Dados

**Objetivo**

Neste desafio, analisamos e transformamos os dados do arquivo `dados_ficha_a_desafio.csv`, identificando problemas e aplicando tratamento adequado com DBT.

## Tarefas
1. Exploração e apontamento de problemas

* Analisamos cada campo do dataset, identificando padrões e inconsistências.
* Apontamos possíveis problemas e inferimos hipóteses sobre a origem dessas questões.
* Documentamos questionamentos relevantes para melhor compreensão dos dados.

2. Tratamento de dados com DBT

* Criamos um modelo DBT para padronizar os dados e gerar uma tabela tratada.
* Aplicamos boas práticas para garantir modularização e legibilidade do código.

----

## Como rodar o projeto

O projeto atualmente utiliza o gerenciador de pacotes [Poetry](https://python-poetry.org/), sendo ele requisito para instalar as dependências. A utilização dele não é necessária, porém tornar o gerenciamento de dependências mais práticos e mais fácil de ser compreendido. Atualmente no projeto é utilizado a versão 2.0.1.

E uma vez instalado, para começar a rodar o programa precisará colocar o dado de origem no diretório `data/raw`, e depois disso pode trabalhar com o poetry para instalar as bibliotecas necessárias para rodar o programa:

```bash
poetry install
```

Se quiser trabalhar pelo notebook, que contém mais anotações, pode ir pelo comando:

```bash
poetry run jupyter lab
```

Ou se preferir uma abordagem mais direta, executando do diretório principal:

```bash
poetry run python src/preprocessing.py
```

Essa parte é mais dedicada para preparar os dados e tratá-los para fazer as análises.

---


Caso queira trabalhar com pip, existe o requirements que está atualizado com as versões de cada dependência. Se adicionar novas dependências, para atualizar o requirements.txt:

```bash
poetry run pip freeze > requirements.txt
```

---

## Análises

_WIP_

## DBT

_WIP_


### Tecnologias utilizadas

* Python para análise exploratória e pré-processamento.
* SQL para manipulação dos dados.
* DBT (Data Build Tool) para transformação e modelagem dos dados.

### Estrutura do Repositório
```
📦 desafio-ciencia-dados
┣ 📂 data/ → Local para encontrar os dados brutos e tratados.
┣ 📂 notebooks/ → Contém os notebooks de análise exploratória.
┣ 📂 dbt_project/ → Contém os arquivos do DBT.
┣ 📂 src/ → Contém os scripts Python utilizados.
┣ 📜 README.md → Documentação principal do projeto.
```
