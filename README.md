# Pipeline ETL: Dados Climáticos (Open-Meteo API -> SQLite)

Este projeto demonstra a construção de um pipeline de dados completo (Extração, Transformação e Carga) voltado para análise climática. O script automatiza a coleta de dados de uma API pública, realiza limpezas e transformações estruturais, e armazena os resultados em um banco de dados relacional.

## O Problema Resolvido
Profissionais de dados gastam até 80% do seu tempo preparando informações. O objetivo deste projeto é mostrar proficiência na automação dessa etapa fundamental. Ao invés de baixar planilhas manualmente, este pipeline coleta dados meteorológicos brutos (temperatura e precipitação de Fortaleza-CE), padroniza o formato e consolida as informações em um banco SQL pronto para consultas de negócio.

## Ferramentas Tecnológicas
*   **Linguagem:** Python
*   **Extração (Extract):** Biblioteca `requests` (Integração com a API REST Open-Meteo).
*   **Transformação (Transform):** Biblioteca `pandas` (Conversão de JSON aninhado para formato tabular, tratamento de nulos, tipagem de datas e *feature engineering*).
*   **Carga (Load):** `sqlite3` e comandos SQL (Persistência dos dados em banco relacional local).

## Fluxo da Arquitetura

1.  **Extract:** O script envia uma requisição `GET` para a API de histórico da Open-Meteo, solicitando dados horários (temperatura, umidade, chuva) dos últimos 30 dias válidos, retornando um objeto JSON complexo.
2.  **Transform:** O Pandas recebe o nó `hourly` do JSON. As colunas são renomeadas para o padrão de banco de dados (`snake_case`), os *timestamps* são convertidos para o tipo `datetime`, e novas *features* são criadas (separação de data e hora para facilitar agregações futuras).
3.  **Load:** Uma conexão com um banco local (`clima_fortaleza.db`) é estabelecida. O DataFrame transformado é inserido em uma tabela SQL chamada `historico_climatico`.
4.  **Validação:** O próprio script finaliza executando uma *Query SQL* (`SELECT`, `GROUP BY`, `AVG`, `MAX`) diretamente no banco para provar que a carga foi bem-sucedida, exibindo um relatório agregado por dia no terminal.

## Como Executar o Pipeline

1. Clone o repositório,
2. Instale as bibliotecas necessárias:

    `pip install requests pandas sqlite3`

3. Execute o script principal:

    `python etl_script.py`

##
O script irá rodar silenciosamente informando as etapas no terminal e criará (ou atualizará) o arquivo clima_fortaleza.db na mesma pasta.

## Próximos Passos

    [ ] Conectar ferramentas de Business Intelligence (Tableau ou Power BI) diretamente ao banco .db para criar painéis interativos sobre o comportamento climático.

    [ ] Migrar a orquestração do script para o Apache Airflow, programando execuções diárias automáticas.