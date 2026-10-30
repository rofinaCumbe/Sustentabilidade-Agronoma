"""
Sustentabilidade Agrónoma — Perfil do Agricultor
Visualização e edição dos dados pessoais e da machamba.
"""

import streamlit as st
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from utils.database import (
    inicializar_bd, obter_agricultor, actualizar_agricultor,
    calcular_agua_total, calcular_streak_irrigacao, hash_senha
)

# ─── Configuração ───
st.set_page_config(
    page_title="Perfil — Sustentabilidade Agrónoma",
    page_icon=":material/person:",
    layout="wide",
    initial_sidebar_state="collapsed"
)

inicializar_bd()

# ─── Protecção ───
if not st.session_state.get('autenticado'):
    st.switch_page("app.py")
    st.stop()

agricultor = obter_agricultor(st.session_state['agricultor_id'])
if not agricultor:
    st.error("Erro ao carregar perfil.")
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
        max-width: 1050px !important;
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
    .icon-lg { width: 48px; height: 48px; }
    .icon-xl { width: 64px; height: 64px; }

    .perfil-header {
        text-align: center;
        padding: 1.75rem;
        background: #FFFFFF;
        border: 1.5px solid #2E7D32;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.05);
    }
    .perfil-header .avatar {
        margin-bottom: 0.5rem;
    }
    .perfil-header h2 {
        color: #1B5E20;
        margin: 0;
        font-size: 1.75rem;
    }
    .perfil-header p {
        color: #616161;
        margin: 0.2rem 0 0;
    }

    .stat-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
        margin: 1rem 0;
    }
    .stat-box {
        background: white;
        border: 1px solid #C8E6C9;
        border-top: 3px solid #2E7D32;
        border-radius: 10px;
        padding: 1.25rem;
        text-align: center;
    }
    .stat-box .num {
        font-size: 1.4rem;
        font-weight: 700;
        color: #2E7D32;
    }
    .stat-box .lbl {
        font-size: 0.78rem;
        color: #757575;
    }

    @media (max-width: 992px) {
        [data-testid="stHorizontalBlock"] {
            flex-wrap: wrap !important;
        }
        [data-testid="column"] {
            flex: 1 1 calc(50% - 1rem) !important;
            min-width: 240px !important;
        }
    }
    @media (max-width: 640px) {
        .stat-grid {
            grid-template-columns: 1fr;
        }
        [data-testid="column"] {
            flex: 1 1 100% !important;
            min-width: 100% !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# ─── Navegação Rápida Limpa ───
nav_c1, nav_c2, nav_c3, nav_c4 = st.columns([1, 1, 1, 1])
with nav_c1:
    st.page_link("pages/1_Dashboard.py", label="Painel de Irrigação", icon=":material/dashboard:", use_container_width=True)
with nav_c2:
    st.page_link("pages/2_Actividades.py", label="Controlo de Actividades", icon=":material/task_alt:", use_container_width=True)
with nav_c3:
    st.page_link("pages/3_Perfil.py", label="Dados do Agricultor", icon=":material/person:", use_container_width=True)
with nav_c4:
    if st.button("Terminar Sessão", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.switch_page("app.py")

st.divider()

# ─── Cabeçalho do Perfil ───
agua_total = calcular_agua_total(agricultor['id'])
streak = calcular_streak_irrigacao(agricultor['id'])

st.markdown(f"""
<div class="perfil-header">
    <div class="avatar">
        <svg class="icon icon-xl" viewBox="0 0 24 24" style="color: #2E7D32;">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
            <circle cx="12" cy="7" r="4"/>
        </svg>
    </div>
    <h2>{agricultor['nome_completo']}</h2>
    <p>{agricultor['nome_machamba']} · {agricultor['provincia']}</p>
    <p style="font-size: 0.8rem; margin-top: 0.5rem;">ID: {agricultor['id']} · Registado em {agricultor.get('data_registo', 'N/D')[:10]}</p>
</div>
""", unsafe_allow_html=True)

# ─── Estatísticas ───
st.markdown(f"""
<div class="stat-grid">
    <div class="stat-box">
        <div class="num">{agricultor.get('area_hectares', 0):.1f} ha</div>
        <div class="lbl">Área da Machamba</div>
    </div>
    <div class="stat-box">
        <div class="num">{agua_total:,.0f} L</div>
        <div class="lbl">Água Total Registada</div>
    </div>
    <div class="stat-box">
        <div class="num">{streak}</div>
        <div class="lbl">Dias Consecutivos</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()

# ─── Formulário de Edição ───
st.markdown("### Editar Dados")

with st.form("form_perfil"):
    nome_edit = st.text_input("Nome Completo", value=agricultor['nome_completo'])
    machamba_edit = st.text_input("Nome da Machamba", value=agricultor['nome_machamba'])

    col1, col2 = st.columns(2)
    with col1:
        provincias = [
            'Cidade de Maputo', 'Província de Maputo', 'Gaza',
            'Inhambane', 'Sofala', 'Manica', 'Tete',
            'Zambézia', 'Nampula', 'Cabo Delgado', 'Niassa'
        ]
        idx_prov = provincias.index(agricultor['provincia']) if agricultor['provincia'] in provincias else 0
        provincia_edit = st.selectbox("Província", provincias, index=idx_prov)

    with col2:
        distrito_edit = st.text_input("Distrito", value=agricultor.get('distrito', ''))

    col3, col4 = st.columns(2)
    with col3:
        telefone_edit = st.text_input("Telefone", value=agricultor['telefone'], disabled=True,
                                       help="O telefone não pode ser alterado (é usado para login)")
    with col4:
        email_edit = st.text_input("Email", value=agricultor.get('email', ''))

    col5, col6 = st.columns(2)
    with col5:
        culturas = [
            'Milho', 'Arroz', 'Feijão', 'Mandioca', 'Hortícolas',
            'Fruteiras', 'Cana-de-Açúcar', 'Algodão', 'Tabaco',
            'Amendoim', 'Soja', 'Gergelim', 'Outros'
        ]
        idx_cult = culturas.index(agricultor.get('cultura_principal', 'Milho')) if agricultor.get('cultura_principal') in culturas else 0
        cultura_edit = st.selectbox("Cultura Principal", culturas, index=idx_cult)

    with col6:
        area_edit = st.number_input("Área (hectares)", value=float(agricultor.get('area_hectares', 1)),
                                     min_value=0.0, max_value=10000.0, step=0.5)

    st.divider()
    st.markdown("**Alterar Senha** (deixe em branco para manter a actual)")

    col7, col8 = st.columns(2)
    with col7:
        nova_senha = st.text_input("Nova Senha", type="password", key="nova_senha")
    with col8:
        confirmar_nova = st.text_input("Confirmar Nova Senha", type="password", key="confirmar_nova")

    btn_guardar = st.form_submit_button("Guardar Alterações", type="primary", use_container_width=True)

    if btn_guardar:
        dados_update = {
            'nome_completo': nome_edit.strip(),
            'nome_machamba': machamba_edit.strip(),
            'provincia': provincia_edit,
            'distrito': distrito_edit.strip(),
            'email': email_edit.strip(),
            'cultura_principal': cultura_edit,
            'area_hectares': area_edit,
        }

        # Senha
        if nova_senha:
            if len(nova_senha) < 6:
                st.error("A nova senha deve ter no mínimo 6 caracteres.")
                st.stop()
            if nova_senha != confirmar_nova:
                st.error("As senhas não coincidem.")
                st.stop()
            dados_update['senha_hash'] = hash_senha(nova_senha)

        sucesso = actualizar_agricultor(agricultor['id'], dados_update)
        if sucesso:
            st.session_state['agricultor_nome'] = nome_edit.strip()
            st.success("Perfil actualizado com sucesso!")
            st.rerun()
        else:
            st.error("Erro ao actualizar o perfil.")

# ─── Logout ───
st.divider()
if st.button("Sair da Conta", use_container_width=True):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.switch_page("app.py")

st.caption(f"Sustentabilidade Agrónoma · {datetime.now().strftime('%d/%m/%Y %H:%M')}")
