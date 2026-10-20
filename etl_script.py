import requests
import pandas as pd
import sqlite3
from datetime import datetime, timedelta


def extract_weather_data(latitude, longitude, start_date, end_date):
    
    print(f"Extraindo dados de {start_date} até {end_date}...")
    
    url = f"https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": ["temperature_2m", "relative_humidity_2m", "precipitation"],
        "timezone": "America/Fortaleza"
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        print("Dados extraídos com sucesso!")
        return response.json()
    else:
        print(f"Erro na extração: Status {response.status_code}")
        return None


lat_fortaleza = -3.7172
lon_fortaleza = -38.5431

hoje = datetime.now()
data_fim = hoje - timedelta(days=7) 
data_inicio = data_fim - timedelta(days=30)

str_inicio = data_inicio.strftime('%Y-%m-%d')
str_fim = data_fim.strftime('%Y-%m-%d')

dados_brutos = extract_weather_data(lat_fortaleza, lon_fortaleza, str_inicio, str_fim)


if dados_brutos:
    print(f"Chaves do JSON: {dados_brutos.keys()}")


def transform_data(raw_json):
   
    print("Iniciando transformação dos dados...")
    
    hourly_data = raw_json['hourly']
    
    df = pd.DataFrame(hourly_data)
    
    df.rename(columns={
        'time': 'data_hora',
        'temperature_2m': 'temperatura_celsius',
        'relative_humidity_2m': 'umidade_relativa_pct',
        'precipitation': 'precipitacao_mm'
    }, inplace=True)
    
    df['data_hora'] = pd.to_datetime(df['data_hora'])
    
    df['data_registro'] = df['data_hora'].dt.date
    df['hora_registro'] = df['data_hora'].dt.time
    
    df['precipitacao_mm'].fillna(0, inplace=True)
    df.dropna(subset=['temperatura_celsius', 'umidade_relativa_pct'], inplace=True)
    
    print(f"Transformação concluída. O dataset tem {df.shape[0]} linhas e {df.shape[1]} colunas.")
    return df

df_limpo = transform_data(dados_brutos)
print(df_limpo.head())


def load_data_to_sqlite(df, db_name="clima_fortaleza.db", table_name="historico_climatico"):
    """
    Carrega o DataFrame em um banco de dados SQLite.
    """
    print(f"Conectando ao banco de dados '{db_name}'...")
    
    conn = sqlite3.connect(db_name)
    
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    
    print(f"Dados carregados com sucesso na tabela '{table_name}'.")
    
    conn.close()

load_data_to_sqlite(df_limpo)


print("Validando a carga com uma consulta SQL...\n")

conn = sqlite3.connect("clima_fortaleza.db")
cursor = conn.cursor()

query = """
    SELECT 
        data_registro,
        ROUND(AVG(temperatura_celsius), 2) as temp_media,
        MAX(temperatura_celsius) as temp_maxima,
        SUM(precipitacao_mm) as precipitacao_total
    FROM historico_climatico
    GROUP BY data_registro
    ORDER BY data_registro ASC
    LIMIT 5;
"""

cursor.execute(query)
resultados = cursor.fetchall()

print(f"{'Data':<15} | {'Temp. Média':<12} | {'Temp. Máxima':<12} | {'Precipitação':<12}")
print("-" * 60)
for linha in resultados:
    print(f"{linha[0]:<15} | {linha[1]:<12} | {linha[2]:<12} | {linha[3]:<12}")

conn.close()