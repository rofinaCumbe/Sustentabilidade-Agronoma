"""
Sustentabilidade Agrónoma — Painel de Controlo de Actividades
Registo, visualização e verificação de cumprimento de actividades agrícolas.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

import importlib
import utils.database as _db_mod
importlib.reload(_db_mod)
from utils.database import (
    inicializar_bd, obter_agricultor, registar_actividade,
    obter_actividades, actualizar_actividade, apagar_actividade,
    contar_irrigacoes_hoje, calcular_agua_total, calcular_streak_irrigacao
)
import importlib
import utils.i18n as _i18n_mod
importlib.reload(_i18n_mod)
from utils.i18n import (
    t, render_seletor_idioma, traduzir_tipo_actividade, traduzir_estado
)

# ─── Configuração da Página ───
st.set_page_config(
    page_title="Actividades — Sustentabilidade Agrónoma",
    page_icon=":material/task_alt:",
    layout="wide",
    initial_sidebar_state="collapsed"
)

inicializar_bd()

# ─── Protecção de Rota ───
if not st.session_state.get('autenticado'):
    st.switch_page("app.py")
    st.stop()

agricultor = obter_agricultor(st.session_state['agricultor_id'])
if not agricultor:
    st.error("Erro ao carregar dados do agricultor.")
    st.stop()

# ─── CSS ───
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

    .icon {
        width: 20px;
        height: 20px;
        stroke: currentColor;
        stroke-width: 2;
        stroke-linecap: round;
        stroke-linejoin: round;
        fill: none;
    }
    .icon-lg {
        width: 32px;
        height: 32px;
    }

    .resumo-card {
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
    .resumo-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    .resumo-card .valor {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1B5E20;
    }
    .resumo-card .label {
        color: #616161;
        font-size: 0.82rem;
        margin-top: 0.3rem;
    }

    .cumprimento-ok {
        background: #E8F5E9;
        border: 1px solid #2E7D32;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        margin: 1rem 0;
        color: #1B5E20;
    }
    .cumprimento-alerta {
        background: #FFF3E0;
        border: 1px solid #F57C00;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        margin: 1rem 0;
        color: #E65100;
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
    }
</style>
""", unsafe_allow_html=True)

# ─── Selector de Idioma ───
render_seletor_idioma("actividades")

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

st.markdown(f"### {t('act_titulo')}")
st.markdown(f"{t('lbl_machamba')} **{agricultor['nome_machamba']}** · {t('act_subtitulo')}")

st.divider()

# ─── Resumo do Dia ───
hoje_str = date.today().strftime('%Y-%m-%d')
actividades_hoje = obter_actividades(agricultor['id'], {'data_inicio': hoje_str, 'data_fim': hoje_str})
irrigacoes_hoje = contar_irrigacoes_hoje(agricultor['id'])
agua_total = calcular_agua_total(agricultor['id'])
streak = calcular_streak_irrigacao(agricultor['id'])

# Calcular horas trabalhadas hoje
horas_trabalhadas = 0.0
for act in actividades_hoje:
    if act.get('hora_inicio') and act.get('hora_fim') and act['estado'] == 'Concluída':
        try:
            inicio = datetime.strptime(act['hora_inicio'], '%H:%M')
            fim = datetime.strptime(act['hora_fim'], '%H:%M')
            diff = (fim - inicio).total_seconds() / 3600
            if diff > 0:
                horas_trabalhadas += diff
        except ValueError:
            pass

pendentes = sum(1 for a in actividades_hoje if a['estado'] == 'Pendente')

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div class="resumo-card">
        <div class="valor">{len(actividades_hoje)}</div>
        <div class="label">{t('card_act_hoje')}</div>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="resumo-card">
        <div class="valor">{irrigacoes_hoje}</div>
        <div class="label">{t('card_irrigacoes_hoje')}</div>
    </div>""", unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="resumo-card">
        <div class="valor">{horas_trabalhadas:.1f}h</div>
        <div class="label">{t('card_horas_trab')}</div>
    </div>""", unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="resumo-card">
        <div class="valor">{pendentes}</div>
        <div class="label">{t('card_pendentes')}</div>
    </div>""", unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="resumo-card">
        <div class="valor">{streak}</div>
        <div class="label">{t('card_dias_consecutivos')}</div>
    </div>""", unsafe_allow_html=True)


# ─── Verificação de Cumprimento ───
st.divider()

if irrigacoes_hoje > 0:
    st.markdown(f"""
    <div class="cumprimento-ok">
        {t('cumprimento_ok', n=irrigacoes_hoje, agua=agua_total)}
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class="cumprimento-alerta">
        {t('cumprimento_alerta')}
    </div>
    """, unsafe_allow_html=True)


# ─── Formulário de Registo de Actividade ───
st.divider()
st.markdown(f"### {t('sec_registar_act')}")

with st.form("form_actividade", clear_on_submit=True):
    col_f1, col_f2, col_f3 = st.columns(3)

    with col_f1:
        tipos = ['Irrigação', 'Adubação', 'Pulverização', 'Capina',
                 'Sementeira', 'Colheita', 'Poda', 'Outros']
        tipo = st.selectbox(t('lbl_tipo_act'), tipos, format_func=traduzir_tipo_actividade)

    with col_f2:
        data_act = st.date_input(t('lbl_data_obrig'), value=date.today())

    with col_f3:
        parcela = st.text_input(t('lbl_parcela'), placeholder=t('ph_parcela'))

    col_f4, col_f5, col_f6 = st.columns(3)

    with col_f4:
        hora_inicio = st.time_input(t('lbl_hora_inicio'), value=datetime.now().replace(minute=0, second=0))

    with col_f5:
        hora_fim = st.time_input(t('lbl_hora_fim'), value=datetime.now().replace(minute=0, second=0))

    with col_f6:
        agua_litros = st.number_input(
            t('lbl_qtd_agua'),
            min_value=0.0, max_value=100000.0,
            value=0.0, step=50.0,
            help=t('help_qtd_agua')
        )

    observacoes = st.text_area(
        t('col_observacoes'),
        placeholder=t('ph_observacoes'),
        height=80
    )

    col_btn1, col_btn2 = st.columns([1, 3])
    with col_btn1:
        btn_registar = st.form_submit_button(t('btn_registar_act'), type="primary", use_container_width=True)

    if btn_registar:
        sucesso, msg = registar_actividade({
            'agricultor_id': agricultor['id'],
            'tipo': tipo,
            'data': data_act.strftime('%Y-%m-%d'),
            'hora_inicio': hora_inicio.strftime('%H:%M'),
            'hora_fim': hora_fim.strftime('%H:%M'),
            'parcela': parcela,
            'quantidade_agua_litros': agua_litros,
            'observacoes': observacoes,
            'estado': 'Concluída'
        })
        if sucesso:
            st.success(f"{msg}")
            st.rerun()
        else:
            st.error(msg)


# ─── Filtros e Tabela de Actividades ───
st.divider()
st.markdown(f"### {t('sec_historico_act')}")

col_fil1, col_fil2, col_fil3, col_fil4 = st.columns(4)

with col_fil1:
    filtro_tipo = st.selectbox(
        t('lbl_filtrar_tipo'),
        ['Todos'] + tipos,
        format_func=traduzir_tipo_actividade,
        key="filtro_tipo"
    )

with col_fil2:
    filtro_estado = st.selectbox(
        t('lbl_filtrar_estado'),
        ['Todos', 'Concluída', 'Pendente'],
        format_func=traduzir_estado,
        key="filtro_estado"
    )

with col_fil3:
    filtro_data_inicio = st.date_input(t('lbl_de'), value=date.today() - timedelta(days=30), key="filtro_di")

with col_fil4:
    filtro_data_fim = st.date_input(t('lbl_ate'), value=date.today(), key="filtro_df")

# Buscar actividades com filtros
filtros = {
    'tipo': filtro_tipo,
    'estado': filtro_estado,
    'data_inicio': filtro_data_inicio.strftime('%Y-%m-%d'),
    'data_fim': filtro_data_fim.strftime('%Y-%m-%d'),
}

actividades = obter_actividades(agricultor['id'], filtros)

if actividades:
    df_act = pd.DataFrame(actividades)

    # Formatar para exibição traduzindo tipo e estado
    df_display = df_act[['data', 'hora_inicio', 'hora_fim', 'tipo', 'parcela',
                          'quantidade_agua_litros', 'estado', 'observacoes']].copy()
    df_display['tipo'] = df_display['tipo'].apply(traduzir_tipo_actividade)
    df_display['estado'] = df_display['estado'].apply(traduzir_estado)

    df_display.columns = [
        t('col_data'), 'Início', 'Fim', 'Tipo', t('lbl_parcela'),
        'Água (L)', t('col_status'), t('col_observacoes')
    ]

    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True,
        column_config={
            'Água (L)': st.column_config.NumberColumn(format="%.0f L"),
        }
    )

    # Estatísticas resumo
    st.markdown(t('msg_act_encontradas', n=len(actividades)))

    # Exportar para CSV
    col_exp1, col_exp2 = st.columns([1, 4])
    with col_exp1:
        csv_data = df_display.to_csv(index=False).encode('utf-8')
        st.download_button(
            t('btn_exportar_csv'),
            data=csv_data,
            file_name=f"actividades_{agricultor['nome_machamba']}_{date.today()}.csv",
            mime="text/csv",
            use_container_width=True
        )

    # ─── Gestão Individual (marcar/apagar) ───
    st.divider()
    st.markdown(f"### {t('sec_gerir_act')}")

    for act in actividades[:20]:  # Limitar a 20 mais recentes
        tipo_lbl = traduzir_tipo_actividade(act['tipo'])
        estado_lbl = traduzir_estado(act['estado'])
        with st.expander(f"{tipo_lbl} — {act['data']} ({act['hora_inicio']} - {act['hora_fim']}) · {estado_lbl}"):
            st.markdown(f"**{t('lbl_parcela')}:** {act.get('parcela', 'N/D')}")
            st.markdown(f"**Água:** {act.get('quantidade_agua_litros', 0):.0f} litros")
            st.markdown(f"**{t('col_observacoes')}:** {act.get('observacoes', '-')}")

            col_g1, col_g2, col_g3 = st.columns(3)

            with col_g1:
                novo_estado = 'Concluída' if act['estado'] == 'Pendente' else 'Pendente'
                if st.button(
                    t('btn_marcar_concluida') if act['estado'] == 'Pendente' else t('btn_marcar_pendente'),
                    key=f"estado_{act['id']}",
                    use_container_width=True
                ):
                    actualizar_actividade(act['id'], {'estado': novo_estado})
                    st.rerun()

            with col_g3:
                if st.button(t('btn_apagar'), key=f"apagar_{act['id']}", use_container_width=True):
                    apagar_actividade(act['id'])
                    st.success(t('msg_act_removida'))
                    st.rerun()

else:
    st.info(t('info_sem_act'))


# ─── Mini Calendário Semanal ───
st.divider()
st.markdown(f"### {t('sec_resumo_semanal')}")

dias_semana = []
for i in range(6, -1, -1):
    dia = date.today() - timedelta(days=i)
    acts_dia = obter_actividades(agricultor['id'], {
        'data_inicio': dia.strftime('%Y-%m-%d'),
        'data_fim': dia.strftime('%Y-%m-%d')
    })
    irrigou = any(a['tipo'] == 'Irrigação' and a['estado'] == 'Concluída' for a in acts_dia)
    dias_semana.append({
        t('col_data'): dia.strftime('%a %d/%m'),
        'Total': len(acts_dia),
        'Irrigou': t('sem_cumprido') if irrigou else t('sem_nao_registado'),
        'Tipos': ', '.join(set(traduzir_tipo_actividade(a['tipo']) for a in acts_dia)) if acts_dia else '—'
    })

df_semana = pd.DataFrame(dias_semana)
st.dataframe(df_semana, use_container_width=True, hide_index=True)

# ─── Rodapé ───
st.divider()
st.caption(f"{t('app_titulo')} · {datetime.now().strftime('%d/%m/%Y %H:%M')}")
