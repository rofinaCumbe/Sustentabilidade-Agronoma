"""
Sustentabilidade Agrónoma — Módulo de Dados Meteorológicos
Consumo da API Open-Meteo para previsões e dados de clima em Moçambique.
"""

import requests
import pandas as pd
from datetime import datetime
import streamlit as st
from utils.i18n import traduzir_dia_semana

# Cidades de Moçambique com coordenadas geográficas
CIDADES_MOCAMBIQUE = {
    'Maputo': {'lat': -25.9653, 'lon': 32.5892, 'provincia': 'Maputo'},
    'Beira': {'lat': -19.8436, 'lon': 34.8389, 'provincia': 'Sofala'},
    'Nampula': {'lat': -15.1165, 'lon': 39.2666, 'provincia': 'Nampula'},
    'Quelimane': {'lat': -17.8784, 'lon': 36.8882, 'provincia': 'Zambézia'},
    'Tete': {'lat': -16.1564, 'lon': 33.5867, 'provincia': 'Tete'},
    'Chimoio': {'lat': -19.1164, 'lon': 33.4833, 'provincia': 'Manica'},
    'Lichinga': {'lat': -13.3126, 'lon': 35.2403, 'provincia': 'Niassa'},
    'Pemba': {'lat': -12.9736, 'lon': 40.5176, 'provincia': 'Cabo Delgado'},
    'Maxixe': {'lat': -23.8597, 'lon': 35.3473, 'provincia': 'Inhambane'},
    'Xai-Xai': {'lat': -25.0519, 'lon': 34.5603, 'provincia': 'Gaza'},
}

# Mapeamento de códigos WMO para descrições técnicas
WMO_DESCRICOES = {
    0: ('Céu limpo', 'SOL'),
    1: ('Quase limpo', 'SOL'),
    2: ('Parcialmente nublado', 'NUVENS'),
    3: ('Nublado', 'NUBLADO'),
    45: ('Nevoeiro', 'NEVOEIRO'),
    48: ('Nevoeiro com geada', 'NEVOEIRO'),
    51: ('Chuvisco fraco', 'CHUVISCO'),
    53: ('Chuvisco moderado', 'CHUVISCO'),
    55: ('Chuvisco forte', 'CHUVA'),
    61: ('Chuva fraca', 'CHUVA'),
    63: ('Chuva moderada', 'CHUVA'),
    65: ('Chuva forte', 'CHUVA'),
    71: ('Neve fraca', 'FRIO'),
    73: ('Neve moderada', 'FRIO'),
    75: ('Neve forte', 'FRIO'),
    80: ('Aguaceiro fraco', 'CHUVA'),
    81: ('Aguaceiro moderado', 'CHUVA'),
    82: ('Aguaceiro forte', 'TEMPESTADE'),
    85: ('Neve fraca', 'FRIO'),
    86: ('Neve forte', 'FRIO'),
    95: ('Trovoada', 'TEMPESTADE'),
    96: ('Trovoada com granizo fraco', 'TEMPESTADE'),
    99: ('Trovoada com granizo forte', 'TEMPESTADE'),
}


def obter_descricao_wmo(codigo: int) -> tuple[str, str]:
    """Retorna a descrição e categoria para um código WMO."""
    return WMO_DESCRICOES.get(codigo, ('Indeterminado', 'GERAL'))


@st.cache_data(ttl=900, show_spinner=False)
def buscar_dados_clima(latitude: float, longitude: float) -> dict | None:
    """
    Obtém dados meteorológicos da API Open-Meteo.
    Retorna dicionário com dados actuais, horários e diários, ou None se falhar.
    """
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        'latitude': latitude,
        'longitude': longitude,
        'current': ','.join([
            'temperature_2m', 'relative_humidity_2m', 'apparent_temperature',
            'precipitation', 'wind_speed_10m', 'weather_code'
        ]),
        'daily': ','.join([
            'temperature_2m_max', 'temperature_2m_min', 'precipitation_sum',
            'precipitation_probability_max', 'wind_speed_10m_max',
            'weather_code', 'uv_index_max', 'et0_fao_evapotranspiration'
        ]),
        'hourly': ','.join([
            'temperature_2m', 'relative_humidity_2m', 'precipitation_probability',
            'soil_temperature_6cm', 'soil_moisture_3_to_9cm'
        ]),
        'timezone': 'Africa/Maputo',
        'forecast_days': 5
    }

    try:
        resposta = requests.get(url, params=params, timeout=15)
        resposta.raise_for_status()
        return resposta.json()
    except requests.RequestException:
        return None


def processar_dados_actuais(dados_api: dict) -> dict:
    """Extrai e formata os dados meteorológicos actuais."""
    current = dados_api.get('current', {})
    daily = dados_api.get('daily', {})

    codigo_wmo = current.get('weather_code', 0)
    descricao, emoji = obter_descricao_wmo(codigo_wmo)

    # ET0 do dia actual
    et0_hoje = daily.get('et0_fao_evapotranspiration', [0])[0] if daily.get('et0_fao_evapotranspiration') else 0

    return {
        'temperatura': current.get('temperature_2m', 0),
        'humidade_relativa': current.get('relative_humidity_2m', 0),
        'sensacao_termica': current.get('apparent_temperature', 0),
        'precipitacao': current.get('precipitation', 0),
        'vento': current.get('wind_speed_10m', 0),
        'codigo_wmo': codigo_wmo,
        'descricao': descricao,
        'emoji': emoji,
        'et0_hoje': et0_hoje,
        'hora_medicao': current.get('time', ''),
    }


def processar_previsao_5dias(dados_api: dict) -> pd.DataFrame:
    """Converte a previsão diária de 5 dias num DataFrame do Pandas."""
    daily = dados_api.get('daily', {})

    registos = []
    datas = daily.get('time', [])

    for i, data_str in enumerate(datas):
        data_obj = datetime.strptime(data_str, '%Y-%m-%d')
        dia_semana_en = data_obj.strftime('%A')
        dia_semana = traduzir_dia_semana(dia_semana_en)
        data_fmt = data_obj.strftime('%d/%m')

        codigo_wmo = daily.get('weather_code', [0])[i] if i < len(daily.get('weather_code', [])) else 0
        desc, emoji = obter_descricao_wmo(codigo_wmo)

        registos.append({
            'Data': f"{dia_semana} {data_fmt}",
            'data_raw': data_str,
            'Condição': desc,
            'Temp. Máx (°C)': daily.get('temperature_2m_max', [0])[i],
            'Temp. Mín (°C)': daily.get('temperature_2m_min', [0])[i],
            'Precipitação (mm)': daily.get('precipitation_sum', [0])[i],
            'Prob. Chuva (%)': daily.get('precipitation_probability_max', [0])[i],
            'Vento Máx (km/h)': daily.get('wind_speed_10m_max', [0])[i],
            'UV Máx': daily.get('uv_index_max', [0])[i],
            'ET0 (mm/dia)': daily.get('et0_fao_evapotranspiration', [0])[i],
        })

    return pd.DataFrame(registos)


def processar_dados_horarios(dados_api: dict, horas: int = 48) -> pd.DataFrame:
    """Converte dados horários num DataFrame para gráficos (primeiras N horas)."""
    hourly = dados_api.get('hourly', {})

    registos = []
    tempos = hourly.get('time', [])[:horas]

    for i, tempo_str in enumerate(tempos):
        dt = datetime.strptime(tempo_str, '%Y-%m-%dT%H:%M')

        registos.append({
            'Hora': dt,
            'hora_label': dt.strftime('%d/%m %Hh'),
            'Temperatura (°C)': hourly.get('temperature_2m', [0])[i],
            'Humidade Rel. (%)': hourly.get('relative_humidity_2m', [0])[i],
            'Prob. Chuva (%)': hourly.get('precipitation_probability', [0])[i],
            'Temp. Solo 6cm (°C)': hourly.get('soil_temperature_6cm', [0])[i] if hourly.get('soil_temperature_6cm') else None,
            'Humidade Solo (m³/m³)': hourly.get('soil_moisture_3_to_9cm', [0])[i] if hourly.get('soil_moisture_3_to_9cm') else None,
        })

    return pd.DataFrame(registos)
