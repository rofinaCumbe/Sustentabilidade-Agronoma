"""
Sustentabilidade Agrónoma — Dashboard Principal
Painel de irrigação com dados meteorológicos em tempo real,
semáforo de rega, previsão de 5 dias e gráficos interactivos.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

import importlib
import utils.database as _db_mod
importlib.reload(_db_mod)
from utils.database import inicializar_bd, obter_agricultor, contar_irrigacoes_hoje, calcular_streak_irrigacao
from utils.weather import (
    CIDADES_MOCAMBIQUE, buscar_dados_clima,
    processar_dados_actuais, processar_previsao_5dias, processar_dados_horarios
)
from utils.irrigation import (
    avaliar_irrigacao_actual, avaliar_calendario_5dias,
    gerar_dicas_agronomicas, NIVEIS_IRRIGACAO
)
import importlib
import utils.i18n as _i18n_mod
importlib.reload(_i18n_mod)
from utils.i18n import (
    t, render_seletor_idioma, traduzir_cultura
)

# ─── Configuração da Página ───
st.set_page_config(
    page_title="Dashboard — Sustentabilidade Agrónoma",
    page_icon=":material/eco:",
    layout="wide",
    initial_sidebar_state="collapsed"
)

inicializar_bd()

# ─── Protecção de Rota ───
if not st.session_state.get('autenticado'):
    st.switch_page("app.py")
    st.stop()

# Dados do agricultor logado
agricultor = obter_agricultor(st.session_state['agricultor_id'])
if not agricultor:
    st.error("Erro ao carregar dados do agricultor.")
    st.stop()

# ─── CSS Personalizado (Sem Barras do Streamlit, Fundo Branco, Contraste Verde e Responsivo) ───
st.markdown("""
<style>
    /* Ocultar botão Implantar (Deploy), menu de 3 pontos, barra superior, sidebar e ícones de link de cabeçalho */
    #MainMenu { visibility: hidden !important; display: none !important; }
    header[data-testid="stHeader"] { visibility: hidden !important; display: none !important; }
    [data-testid="stToolbar"] { visibility: hidden !important; display: none !important; }
    [data-testid="stDecoration"] { visibility: hidden !important; display: none !important; }
    [data-testid="stStatusWidget"] { visibility: hidden !important; display: none !important; }
    .stDeployButton, [data-testid="stAppDeployButton"] { visibility: hidden !important; display: none !important; }
    footer { visibility: hidden !important; display: none !important; }
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="stSidebarCollapsedControl"] { display: none !important; }
    [data-testid="stHeaderActionElements"],
    .stMarkdown h1 a, .stMarkdown h2 a, .stMarkdown h3 a, .stMarkdown h4 a,
    a.header-anchor { display: none !important; visibility: hidden !important; pointer-events: none !important; }

    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2.5rem !important;
        max-width: 1220px !important;
    }

    /* Ícones SVG */
    .icon {
        width: 20px;
        height: 20px;
        stroke: currentColor;
        stroke-width: 2;
        stroke-linecap: round;
        stroke-linejoin: round;
        fill: none;
    }
    .icon-lg { width: 32px; height: 32px; }
    .icon-xl { width: 44px; height: 44px; }

    /* Cards de métricas */
    .metric-card {
        background: white;
        border: 1px solid #C8E6C9;
        border-top: 3px solid #2E7D32;
        border-radius: 12px;
        padding: 1.15rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        margin-bottom: 0.75rem;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    .metric-card .valor {
        font-size: 1.85rem;
        font-weight: 700;
        color: #1B5E20;
    }
    .metric-card .label {
        color: #616161;
        font-size: 0.82rem;
        margin-top: 0.3rem;
    }

    /* Semáforo */
    .semaforo-container {
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        margin: 0.5rem 0;
    }
    .semaforo-nivel {
        font-size: 1.35rem;
        font-weight: 700;
    }
    .semaforo-descricao {
        font-size: 0.9rem;
        margin-top: 0.5rem;
        opacity: 0.88;
    }

    /* Dicas */
    .dica-card {
        background: #F1F8E9;
        border-left: 4px solid #2E7D32;
        padding: 1rem 1.2rem;
        border-radius: 0 8px 8px 0;
        margin-bottom: 0.8rem;
    }
    .dica-card.alta {
        background: #FFF3E0;
        border-left-color: #F57C00;
    }
    .dica-card h4 {
        margin: 0 0 0.3rem 0;
        font-size: 0.95rem;
        color: #1B5E20;
    }
    .dica-card p {
        margin: 0;
        font-size: 0.85rem;
        color: #37474F;
    }

    /* Responsividade */
    @media (max-width: 992px) {
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        [data-testid="stHorizontalBlock"] {
            flex-wrap: wrap !important;
        }
        [data-testid="column"] {
            flex: 1 1 calc(50% - 1rem) !important;
            min-width: 240px !important;
        }
    }
    @media (max-width: 640px) {
        .block-container {
            padding-top: 0.75rem !important;
            padding-left: 0.65rem !important;
            padding-right: 0.65rem !important;
        }
        [data-testid="column"] {
            flex: 1 1 100% !important;
            min-width: 100% !important;
        }
        .metric-card .valor {
            font-size: 1.55rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# ─── Selector de Idioma ───
render_seletor_idioma("dashboard")

# ─── Navegação Rápida Limpa ───
nav_c1, nav_c2, nav_c3, nav_c4 = st.columns([1, 1, 1, 1])
with nav_c1:
    st.page_link("pages/1_Dashboard.py", label=t('nav_painel'), icon=":material/dashboard:", use_container_width=True)
with nav_c2:
    st.page_link("pages/2_Actividades.py", label=t('nav_actividades'), icon=":material/task_alt:", use_container_width=True)
with nav_c3:
    st.page_link("pages/3_Perfil.py", label=t('nav_perfil'), icon=":material/person:", use_container_width=True)
with nav_c4:
    if st.button(t('nav_sair'), use_container_width=True):
        idioma_guardado = st.session_state.get('idioma', 'pt')
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.session_state['idioma'] = idioma_guardado
        st.switch_page("app.py")

st.divider()


# ─── Saudação ───
hora_actual = datetime.now().hour
if hora_actual < 12:
    saudacao = t('saudacao_dia')
elif hora_actual < 18:
    saudacao = t('saudacao_tarde')
else:
    saudacao = t('saudacao_noite')

cultura_exibicao = traduzir_cultura(agricultor.get('cultura_principal', 'N/D'))

st.markdown(f"### {saudacao}, {agricultor['nome_completo'].split()[0]}!")
st.markdown(
    f"{t('lbl_machamba')} **{agricultor['nome_machamba']}** · "
    f"{agricultor['provincia']} · "
    f"{t('lbl_cultura')}: **{cultura_exibicao}** · "
    f"{t('lbl_area')}: **{agricultor.get('area_hectares', 0):.1f} ha**"
)

# ─── Selecção de Localização ───
col_cidade, col_refresh = st.columns([4, 1])

with col_cidade:
    cidade_sel = st.selectbox(
        t('sel_localizacao_clima'),
        list(CIDADES_MOCAMBIQUE.keys()),
        index=0,
        key="cidade_dashboard"
    )

with col_refresh:
    st.markdown("<br>", unsafe_allow_html=True)
    btn_refresh = st.button(t('btn_actualizar_dados'), use_container_width=True)

# ─── Obter Dados Meteorológicos ───
coords = CIDADES_MOCAMBIQUE[cidade_sel]

with st.spinner(t('spinner_clima', cidade=cidade_sel)):
    dados_api = buscar_dados_clima(coords['lat'], coords['lon'])

if not dados_api:
    st.error(t('err_clima_internet'))
    st.stop()

# Processar dados
dados_actuais = processar_dados_actuais(dados_api)
df_previsao = processar_previsao_5dias(dados_api)
df_horario = processar_dados_horarios(dados_api, horas=48)

# Avaliação de irrigação
avaliacao = avaliar_irrigacao_actual(dados_actuais, df_previsao)

# Guardar na sessão para o contexto em tempo real do Assistente IA no topo
st.session_state['ultimo_clima_actual'] = dados_actuais
st.session_state['ultima_avaliacao_irrigacao'] = avaliacao

st.divider()

# ─── Cards de Resumo Rápido ───
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div style="font-size: 2rem;">
            <svg class="icon icon-xl" viewBox="0 0 24 24" style="color: #F57C00;">
                <path d="M14 14.76V3.5a2.5 2.5 0 0 0-5 0v11.26a4.5 4.5 0 1 0 5 0z"/>
            </svg>
        </div>
        <div class="valor">{dados_actuais['temperatura']:.1f}°C</div>
        <div class="label">{t('card_temp_actual')}</div>
        <div class="label" style="font-size: 0.75rem;">{t('card_sensacao')}: {dados_actuais['sensacao_termica']:.1f}°C</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div style="font-size: 2rem;">
            <svg class="icon icon-xl" viewBox="0 0 24 24" style="color: #1976D2;">
                <path d="M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10z"/>
                <path d="M12 2v20"/>
                <path d="M2 12h20"/>
                <path d="m12 2 4 4"/>
                <path d="m12 2-4 4"/>
                <path d="m12 22 4-4"/>
                <path d="m12 22-4-4"/>
            </svg>
        </div>
        <div class="valor">{dados_actuais['humidade_relativa']}%</div>
        <div class="label">{t('card_humidade_ar')}</div>
        <div class="label" style="font-size: 0.75rem;">{t('card_vento')}: {dados_actuais['vento']:.0f} km/h</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div style="font-size: 2rem;">
            <svg class="icon icon-xl" viewBox="0 0 24 24" style="color: {avaliacao['cor']};">
                <circle cx="12" cy="12" r="10"/>
                <path d="M12 6v6l4 2"/>
            </svg>
        </div>
        <div class="valor" style="color: {avaliacao['cor']}; font-size: 1rem;">{avaliacao['rotulo'].split('—')[0].strip()}</div>
        <div class="label">{t('card_estado_irrigacao')}</div>
        <div class="label" style="font-size: 0.75rem;">{t('card_pontuacao')}: {avaliacao['pontuacao']}/100</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    irrigacoes_hoje = contar_irrigacoes_hoje(agricultor['id'])
    streak = calcular_streak_irrigacao(agricultor['id'])
    st.markdown(f"""
    <div class="metric-card">
        <div style="font-size: 2rem;">
            <svg class="icon icon-xl" viewBox="0 0 24 24" style="color: #2E7D32;">
                <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/>
                <polyline points="14 2 14 8 20 8"/>
                <line x1="16" x2="8" y1="13" y2="13"/>
                <line x1="16" x2="8" y1="17" y2="17"/>
                <line x1="10" x2="8" y1="9" y2="9"/>
            </svg>
        </div>
        <div class="valor">{irrigacoes_hoje}</div>
        <div class="label">{t('card_irrigacoes_hoje')}</div>
        <div class="label" style="font-size: 0.75rem;">{t('card_streak', streak=streak)}</div>
    </div>
    """, unsafe_allow_html=True)


# ─── Painel do Semáforo de Irrigação ───
st.divider()
st.markdown(f"### {t('sec_recomendacao_irrigacao')}")

col_semaforo, col_detalhes = st.columns([1, 1])

with col_semaforo:
    st.markdown(f"""
    <div class="semaforo-container" style="background-color: {avaliacao['cor_fundo']}; border: 2px solid {avaliacao['cor']};">
        <div style="font-size: 3.5rem;">
            <svg class="icon icon-xl" viewBox="0 0 24 24" style="color: {avaliacao['cor']}; width: 80px; height: 80px;">
                <circle cx="12" cy="12" r="10"/>
                <path d="M12 6v6l4 2"/>
            </svg>
        </div>
        <div class="semaforo-nivel" style="color: {avaliacao['cor']};">{avaliacao['rotulo']}</div>
        <div class="semaforo-descricao">{avaliacao['descricao']}</div>
    </div>
    """, unsafe_allow_html=True)

with col_detalhes:
    st.markdown(t('detalhes_avaliacao'))

    det_col1, det_col2 = st.columns(2)
    with det_col1:
        st.metric(t('met_lamina'), f"{avaliacao['lamina_mm']} mm")
        st.metric(t('met_temperatura'), f"{avaliacao['factores']['temperatura']:.1f} °C")
        st.metric(t('met_precipitacao'), f"{avaliacao['factores']['precipitacao']:.1f} mm")

    with det_col2:
        st.metric(t('met_horario_ideal'), avaliacao['horario_ideal'].split('(')[0].strip())
        st.metric(t('met_et0'), f"{avaliacao['factores']['et0']:.1f} mm/dia")
        st.metric(t('met_prob_chuva'), f"{avaliacao['factores']['prob_chuva']:.0f}%")

    # Volume total para a área da machamba
    area_ha = agricultor.get('area_hectares', 1) or 1
    volume_total = avaliacao['lamina_mm'] * area_ha * 10  # mm * ha * 10 = m³
    if volume_total > 0:
        st.info(t('info_volume_estimado', area=area_ha, litros=volume_total, m3=volume_total / 1000))


# ─── Previsão de 5 Dias ───
st.divider()
st.markdown(f"### {t('sec_previsao_5dias')}")

# Enriquecer com recomendações de irrigação
df_calendario = avaliar_calendario_5dias(df_previsao)

# Mostrar como cards horizontais
cols_prev = st.columns(len(df_calendario))
for i, (_, row) in enumerate(df_calendario.iterrows()):
    with cols_prev[i]:
        cor_badge = "#2E7D32" if row['Lâmina (mm)'] > 0 else "#616161"
        st.markdown(f"""
        <div class="metric-card" style="padding: 1rem;">
            <div style="font-weight: 700; color: #1B5E20; margin-bottom: 0.4rem;">{row['Data']}</div>
            <div style="font-size: 0.85rem; color: #424242; margin-bottom: 0.4rem;">{row['Condição']}</div>
            <div style="font-size: 1.2rem; font-weight: 700; color: #212121;">{row['Temp. Máx (°C)']:.0f}°C / {row['Temp. Mín (°C)']:.0f}°C</div>
            <div style="font-size: 0.8rem; color: #616161; margin-top: 0.3rem;">{t('met_precipitacao')}: {row['Precipitação (mm)']:.1f} mm</div>
            <div style="font-size: 0.8rem; color: #616161;">ET0: {row['ET0 (mm/dia)']:.1f} mm/dia</div>
            <div style="margin-top: 0.6rem; padding: 0.3rem 0.5rem; background: #E8F5E9; border-radius: 6px; font-weight: 600; font-size: 0.82rem; color: {cor_badge};">
                {row['Recomendação']}
            </div>
        </div>
        """, unsafe_allow_html=True)


# ─── Calendário de Irrigação (Tabela) ───
st.divider()
st.markdown(f"### {t('sec_calendario_irrigacao')}")

# Seleccionar colunas relevantes para a tabela
df_tabela = df_calendario[['Data', 'Condição', 'Temp. Máx (°C)', 'Temp. Mín (°C)',
                            'Precipitação (mm)', 'ET0 (mm/dia)', 'Status',
                            'Recomendação', 'Lâmina (mm)', 'Observações']].copy()

st.dataframe(
    df_tabela,
    use_container_width=True,
    hide_index=True,
    column_config={
        'Data': st.column_config.TextColumn(t('col_data'), width='medium'),
        'Condição': st.column_config.TextColumn(t('col_condicao'), width='medium'),
        'Temp. Máx (°C)': st.column_config.NumberColumn(t('col_max'), format="%.1f°C"),
        'Temp. Mín (°C)': st.column_config.NumberColumn(t('col_min'), format="%.1f°C"),
        'Precipitação (mm)': st.column_config.NumberColumn(t('col_chuva'), format="%.1f mm"),
        'ET0 (mm/dia)': st.column_config.NumberColumn('ET0', format="%.1f"),
        'Status': st.column_config.TextColumn(t('col_status'), width='small'),
        'Recomendação': st.column_config.TextColumn(t('col_recomendacao'), width='medium'),
        'Lâmina (mm)': st.column_config.NumberColumn(t('col_lamina'), format="%.1f mm"),
        'Observações': st.column_config.TextColumn(t('col_observacoes'), width='large'),
    }
)


# ─── Gráficos ───
st.divider()
st.markdown(f"### {t('sec_graficos')}")

tab_temp, tab_solo = st.tabs([t('tab_temp_48h'), t('tab_humidade_solo')])

with tab_temp:
    if not df_horario.empty and 'Temperatura (°C)' in df_horario.columns:
        fig_temp = go.Figure()
        fig_temp.add_trace(go.Scatter(
            x=df_horario['Hora'],
            y=df_horario['Temperatura (°C)'],
            mode='lines+markers',
            name=t('met_temperatura'),
            line=dict(color='#2E7D32', width=2),
            marker=dict(size=3),
            fill='tozeroy',
            fillcolor='rgba(46, 125, 50, 0.08)'
        ))

        # Linha de referência de 30°C
        fig_temp.add_hline(
            y=30, line_dash="dash", line_color="#F57C00",
            annotation_text=t('graf_limiar_30'),
            annotation_position="top right"
        )

        fig_temp.update_layout(
            title=t('graf_titulo_temp'),
            xaxis_title=t('graf_eixo_hora'),
            yaxis_title=f"{t('met_temperatura')} (°C)",
            template="plotly_white",
            height=400,
            margin=dict(l=40, r=20, t=50, b=40),
            font=dict(family="Inter, sans-serif")
        )
        st.plotly_chart(fig_temp, use_container_width=True)
    else:
        st.info("Dados horários de temperatura não disponíveis.")

with tab_solo:
    if not df_horario.empty and 'Humidade Solo (m³/m³)' in df_horario.columns:
        # Converter para percentual
        df_solo_plot = df_horario.dropna(subset=['Humidade Solo (m³/m³)'])

        if not df_solo_plot.empty:
            fig_solo = go.Figure()

            fig_solo.add_trace(go.Scatter(
                x=df_solo_plot['Hora'],
                y=df_solo_plot['Humidade Solo (m³/m³)'],
                mode='lines',
                name=f"{t('tab_humidade_solo')} (3-9cm)",
                line=dict(color='#1565C0', width=2),
                fill='tozeroy',
                fillcolor='rgba(21, 101, 192, 0.1)'
            ))

            # Barras de probabilidade de chuva
            fig_solo.add_trace(go.Bar(
                x=df_solo_plot['Hora'],
                y=df_solo_plot['Prob. Chuva (%)'].apply(lambda x: x / 100 * 0.5),
                name=t('met_prob_chuva'),
                marker_color='rgba(76, 175, 80, 0.3)',
                yaxis='y'
            ))

            fig_solo.update_layout(
                title=t('graf_titulo_solo'),
                xaxis_title=t('graf_eixo_hora'),
                yaxis_title="Humidade (m³/m³)",
                template="plotly_white",
                height=400,
                margin=dict(l=40, r=20, t=50, b=40),
                font=dict(family="Inter, sans-serif"),
                barmode='overlay'
            )
            st.plotly_chart(fig_solo, use_container_width=True)
        else:
            st.info("Dados de humidade do solo não disponíveis para esta localização.")
    else:
        st.info("Dados de humidade do solo não disponíveis.")


# ─── Dicas Agronómicas ───
st.divider()
st.markdown(f"### {t('sec_dicas')}")

dicas = gerar_dicas_agronomicas(dados_actuais, agricultor.get('cultura_principal', ''))

for dica in dicas:
    classe = 'alta' if dica['prioridade'] == 'alta' else ''
    st.markdown(f"""
    <div class="dica-card {classe}">
        <div style="font-weight: 700; margin: 0 0 0.3rem 0; font-size: 0.95rem; color: #1B5E20;">{dica['titulo']}</div>
        <p>{dica['texto']}</p>
    </div>
    """, unsafe_allow_html=True)


# ─── Rodapé ───
st.divider()
st.caption(
    t(
        'rodape_actualizado',
        data=datetime.now().strftime('%d/%m/%Y às %H:%M'),
        cidade=cidade_sel,
        lat=coords['lat'],
        lon=coords['lon']
    )
)
