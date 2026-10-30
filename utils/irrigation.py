"""
Sustentabilidade Agrónoma — Módulo do Algoritmo de Irrigação
Avaliação inteligente baseada em temperatura, precipitação, ET0 e humidade do solo.
"""

import pandas as pd
from datetime import datetime
from utils.i18n import traduzir_nivel_irrigacao, traduzir_recomendacao_5dias


# Níveis de recomendação de irrigação
NIVEIS_IRRIGACAO = {
    'URGENTE': {
        'cor': '#D32F2F',
        'cor_fundo': '#FFEBEE',
        'icone': 'URGENTE',
        'rotulo': 'URGENTE — Irrigar Imediatamente',
        'descricao': 'Condições críticas de calor e alta perda de água. Risco elevado de stress hídrico.'
    },
    'ALTO': {
        'cor': '#F57C00',
        'cor_fundo': '#FFF3E0',
        'icone': 'ALTO',
        'rotulo': 'ALTO — Irrigar Hoje',
        'descricao': 'Temperaturas elevadas e solo a secar. Irrigar nas horas mais frescas.'
    },
    'MODERADO': {
        'cor': '#F9A825',
        'cor_fundo': '#FFFDE7',
        'icone': 'MODERADO',
        'rotulo': 'MODERADO — Irrigar se Possível',
        'descricao': 'Clima ameno sem chuva prevista. Monitorar humidade do solo.'
    },
    'BAIXO': {
        'cor': '#2E7D32',
        'cor_fundo': '#E8F5E9',
        'icone': 'BAIXO',
        'rotulo': 'BAIXO — Não é Necessário Irrigar',
        'descricao': 'Chuva prevista ou temperaturas frescas. Poupança de água recomendada.'
    },
    'DESNECESSARIO': {
        'cor': '#1565C0',
        'cor_fundo': '#E3F2FD',
        'icone': 'DISPENSÁVEL',
        'rotulo': 'DESNECESSÁRIO — Solo com Humidade Suficiente',
        'descricao': 'Solo húmido ou chuva recente abundante. Evitar encharcamento.'
    }
}


def avaliar_irrigacao_actual(dados_actuais: dict, df_previsao: pd.DataFrame) -> dict:
    """
    Avalia as condições actuais e retorna a recomendação de irrigação.

    Parâmetros:
        dados_actuais: dicionário com dados meteorológicos actuais
        df_previsao: DataFrame com previsão de 5 dias

    Retorna:
        dicionário com nível, detalhes e recomendações
    """
    temp = dados_actuais.get('temperatura', 25)
    humidade = dados_actuais.get('humidade_relativa', 50)
    precipitacao = dados_actuais.get('precipitacao', 0)
    vento = dados_actuais.get('vento', 0)
    et0 = dados_actuais.get('et0_hoje', 0)

    # Precipitação prevista nas próximas 24h (primeiro dia da previsão)
    precip_prevista = df_previsao['Precipitação (mm)'].iloc[0] if len(df_previsao) > 0 else 0
    prob_chuva = df_previsao['Prob. Chuva (%)'].iloc[0] if len(df_previsao) > 0 else 0

    # Pontuação de necessidade de irrigação (0 a 100)
    pontuacao = 0

    # Factor: Temperatura (maior peso)
    if temp > 35:
        pontuacao += 35
    elif temp > 30:
        pontuacao += 25
    elif temp > 25:
        pontuacao += 15
    elif temp > 20:
        pontuacao += 5

    # Factor: Evapotranspiração ET0
    if et0 > 6:
        pontuacao += 25
    elif et0 > 4:
        pontuacao += 15
    elif et0 > 2:
        pontuacao += 8

    # Factor: Humidade relativa (inverso — ar seco = mais irrigação)
    if humidade < 30:
        pontuacao += 20
    elif humidade < 50:
        pontuacao += 10
    elif humidade > 80:
        pontuacao -= 10

    # Factor: Vento (aumenta evaporação)
    if vento > 30:
        pontuacao += 10
    elif vento > 15:
        pontuacao += 5

    # Factor negativo: Precipitação actual
    if precipitacao > 10:
        pontuacao -= 30
    elif precipitacao > 5:
        pontuacao -= 20
    elif precipitacao > 1:
        pontuacao -= 10

    # Factor negativo: Chuva prevista
    if prob_chuva > 70 and precip_prevista > 5:
        pontuacao -= 25
    elif prob_chuva > 50:
        pontuacao -= 10

    # Limitar entre 0 e 100
    pontuacao = max(0, min(100, pontuacao))

    # Determinar nível
    if pontuacao >= 70:
        nivel = 'URGENTE'
    elif pontuacao >= 50:
        nivel = 'ALTO'
    elif pontuacao >= 30:
        nivel = 'MODERADO'
    elif pontuacao >= 15:
        nivel = 'BAIXO'
    else:
        nivel = 'DESNECESSARIO'

    # Calcular lâmina de água sugerida (mm/m²)
    lamina = calcular_lamina_agua(temp, et0, humidade, precipitacao)

    # Horário ideal de rega
    horario = definir_horario_ideal(temp)

    info_nivel = NIVEIS_IRRIGACAO[nivel]
    rotulo_trad, descricao_trad = traduzir_nivel_irrigacao(nivel)

    return {
        'nivel': nivel,
        'pontuacao': pontuacao,
        'cor': info_nivel['cor'],
        'cor_fundo': info_nivel['cor_fundo'],
        'icone': info_nivel['icone'],
        'rotulo': rotulo_trad,
        'descricao': descricao_trad,
        'lamina_mm': lamina,
        'horario_ideal': horario,
        'factores': {
            'temperatura': temp,
            'humidade': humidade,
            'et0': et0,
            'precipitacao': precipitacao,
            'vento': vento,
            'precip_prevista': precip_prevista,
            'prob_chuva': prob_chuva
        }
    }


def calcular_lamina_agua(temp: float, et0: float, humidade: float, precip: float) -> float:
    """
    Calcula a lâmina de água sugerida em mm (equivalente a L/m²).
    Baseado na evapotranspiração e factores ambientais.
    """
    if precip > 10:
        return 0

    # Base: repor a ET0 do dia
    lamina = et0

    # Ajuste por temperatura
    if temp > 35:
        lamina *= 1.3
    elif temp > 30:
        lamina *= 1.15

    # Ajuste por humidade (ar seco precisa de mais água)
    if humidade < 40:
        lamina *= 1.15

    # Descontar precipitação recente
    lamina = max(0, lamina - precip * 0.8)

    return round(lamina, 1)


def definir_horario_ideal(temp: float) -> str:
    """Define o melhor horário de irrigação com base na temperatura."""
    if temp > 35:
        return "05:00 — 07:00 (madrugada, antes do calor extremo)"
    elif temp > 30:
        return "06:00 — 08:00 (manhã cedo)"
    elif temp > 25:
        return "06:00 — 09:00 ou 17:00 — 19:00"
    else:
        return "07:00 — 10:00 (qualquer hora fresca)"


def avaliar_calendario_5dias(df_previsao: pd.DataFrame) -> pd.DataFrame:
    """
    Avalia cada dia da previsão e adiciona colunas de recomendação de irrigação.
    Retorna o DataFrame enriquecido.
    """
    recomendacoes = []
    icones = []
    observacoes = []
    laminas = []

    for _, row in df_previsao.iterrows():
        temp_max = row['Temp. Máx (°C)']
        temp_min = row['Temp. Mín (°C)']
        temp_media = (temp_max + temp_min) / 2
        precip = row['Precipitação (mm)']
        et0 = row['ET0 (mm/dia)']
        prob_chuva = row['Prob. Chuva (%)']

        # Lógica de decisão
        if precip > 5 or prob_chuva > 70:
            recomendacoes.append(traduzir_recomendacao_5dias('Não Irrigar'))
            icones.append('BAIXO')
            observacoes.append('Chuva prevista suficiente para suprir necessidades hídricas.')
            laminas.append(0)
        elif temp_max > 35 and precip < 2:
            recomendacoes.append(traduzir_recomendacao_5dias('Irrigar (Urgente)'))
            icones.append('URGENTE')
            observacoes.append(f'Calor extremo ({temp_max:.0f}°C). Irrigar de madrugada. ET0: {et0:.1f} mm.')
            laminas.append(round(et0 * 1.3, 1))
        elif temp_max > 30 and precip < 2:
            recomendacoes.append(traduzir_recomendacao_5dias('Irrigar'))
            icones.append('IDEAL')
            observacoes.append(f'Temperaturas altas ({temp_max:.0f}°C). Dia ideal para irrigar pela manhã cedo.')
            laminas.append(round(et0 * 1.1, 1))
        elif temp_media > 25 and precip < 3:
            recomendacoes.append(traduzir_recomendacao_5dias('Irrigar se Possível'))
            icones.append('MODERADO')
            observacoes.append('Clima ameno-quente. Monitorar o solo.')
            laminas.append(round(et0, 1))
        elif temp_media < 20:
            recomendacoes.append(traduzir_recomendacao_5dias('Não Irrigar'))
            icones.append('BAIXO')
            observacoes.append('Temperaturas frescas. Baixa evapotranspiração.')
            laminas.append(0)
        else:
            recomendacoes.append(traduzir_recomendacao_5dias('Opcional'))
            icones.append('OPCIONAL')
            observacoes.append('Condições estáveis. Verificar humidade do solo.')
            laminas.append(round(et0 * 0.7, 1))

    df_resultado = df_previsao.copy()
    df_resultado['Status'] = icones
    df_resultado['Recomendação'] = recomendacoes
    df_resultado['Lâmina (mm)'] = laminas
    df_resultado['Observações'] = observacoes

    return df_resultado


def gerar_dicas_agronomicas(dados_actuais: dict, cultura: str = '') -> list[dict]:
    """
    Gera dicas contextualizadas para o agricultor com base no clima actual.
    """
    temp = dados_actuais.get('temperatura', 25)
    humidade = dados_actuais.get('humidade_relativa', 50)
    vento = dados_actuais.get('vento', 0)
    precipitacao = dados_actuais.get('precipitacao', 0)
    et0 = dados_actuais.get('et0_hoje', 0)

    dicas = []

    # Dica de temperatura
    if temp > 35:
        dicas.append({
            'titulo': 'Alerta de Calor Extremo',
            'texto': f'Temperatura de {temp:.1f}°C. Aplique cobertura morta (mulching) para reduzir a evaporação do solo. Evite trabalho de campo entre 11h-15h.',
            'prioridade': 'alta'
        })
    elif temp > 30:
        dicas.append({
            'titulo': 'Temperaturas Elevadas',
            'texto': f'Com {temp:.1f}°C, a rega é mais eficiente antes das 9h ou depois das 17h para minimizar perdas por evaporação.',
            'prioridade': 'media'
        })

    # Dica de vento
    if vento > 25:
        dicas.append({
            'titulo': 'Vento Forte Registado',
            'texto': f'Vento de {vento:.0f} km/h. Evite irrigação por aspersão — a água dispersa-se. Prefira rega gota-a-gota ou por sulcos.',
            'prioridade': 'alta'
        })

    # Dica de humidade
    if humidade < 35:
        dicas.append({
            'titulo': 'Baixa Humidade Relativa',
            'texto': f'Humidade relativa de {humidade:.0f}%. As plantas perdem mais água por transpiração. Aumente ligeiramente o volume de rega.',
            'prioridade': 'media'
        })
    elif humidade > 85:
        dicas.append({
            'titulo': 'Humidade Atmosférica Elevada',
            'texto': f'Humidade de {humidade:.0f}%. Risco de doenças fúngicas. Garanta boa circulação de ar entre as plantas.',
            'prioridade': 'media'
        })

    # Dica de ET0
    if et0 > 5:
        dicas.append({
            'titulo': 'Alta Demanda Evapotranspirativa (ET0)',
            'texto': f'ET0 de {et0:.1f} mm/dia indica elevada demanda atmosférica. As culturas necessitam de reposição hídrica proporcional.',
            'prioridade': 'alta'
        })

    # Dica de precipitação
    if precipitacao > 5:
        dicas.append({
            'titulo': 'Precipitação Recente',
            'texto': f'Precipitação de {precipitacao:.1f} mm. Suspender irrigação e verificar drenagem dos talhões.',
            'prioridade': 'baixa'
        })

    # Dica geral por cultura
    if cultura:
        dica_cultura = _dica_por_cultura(cultura, temp)
        if dica_cultura:
            dicas.append(dica_cultura)

    # Dica fixa de boas práticas
    dicas.append({
        'titulo': 'Boas Práticas de Eficiência Hídrica',
        'texto': 'Regue sempre nas horas mais frescas do dia. A irrigação gota-a-gota pode reduzir o consumo de água em até 50% em comparação com a aspersão.',
        'prioridade': 'info'
    })

    return dicas


def _dica_por_cultura(cultura: str, temp: float) -> dict | None:
    """Retorna uma dica específica para o tipo de cultura."""
    cultura_lower = cultura.lower()

    culturas_info = {
        'milho': {
            'titulo': 'Manejo Hídrico — Milho',
            'texto': 'O milho é mais sensível ao défice hídrico durante a floração e enchimento do grão. Garanta irrigação regular nessas fases.',
        },
        'arroz': {
            'titulo': 'Manejo Hídrico — Arroz',
            'texto': 'O arroz necessita de lâmina de água permanente no período vegetativo. Mantenha 5-10 cm de água nos talhões alagados.',
        },
        'feijão': {
            'titulo': 'Manejo Hídrico — Feijão',
            'texto': 'O feijoeiro é sensível ao excesso de água. Evite encharcamento e garanta boa drenagem nos canteiros.',
        },
        'hortícolas': {
            'titulo': 'Manejo Hídrico — Hortícolas',
            'texto': 'Hortícolas precisam de regas frequentes mas em menor volume. A cobertura morta ajuda a reter humidade no solo.',
        },
        'mandioca': {
            'titulo': 'Manejo Hídrico — Mandioca',
            'texto': 'A mandioca é tolerante à seca após o estabelecimento, mas beneficia de irrigação nos primeiros 3 meses de plantio.',
        },
        'cana-de-açúcar': {
            'titulo': 'Manejo Hídrico — Cana-de-Açúcar',
            'texto': 'A cana exige grandes volumes de água durante o crescimento. Suspenda a irrigação 4-6 semanas antes da colheita para aumentar o teor de açúcar.',
        },
    }

    for chave, info in culturas_info.items():
        if chave in cultura_lower:
            return {**info, 'prioridade': 'info'}

    return None
