"""
Sustentabilidade Agrónoma — Página Inicial, Login, Cadastro e Recuperação de Senha
Sistema de gestão de irrigação agrícola para Moçambique.
Desenvolvido em Python com Streamlit.
"""

import streamlit as st
import sys
import os
import importlib

# Adicionar o directório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import utils.database as db
import utils.i18n as _i18n_mod
importlib.reload(db)
importlib.reload(_i18n_mod)
from utils.database import inicializar_bd, registar_agricultor, autenticar, redefinir_senha
from utils.i18n import (
    IDIOMAS, t, obter_idioma, definir_idioma,
    render_seletor_idioma, traduzir_cultura
)

# ─── Configuração da Página ───
st.set_page_config(
    page_title="Sustentabilidade Agrónoma",
    page_icon=":material/eco:",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inicializar a base de dados
inicializar_bd()

# Redireccionar se já autenticado
if st.session_state.get('autenticado'):
    st.switch_page("pages/1_Dashboard.py")

# Estado da vista inicial ('landing', 'auth' ou 'recover')
if 'vista_actual' not in st.session_state:
    st.session_state['vista_actual'] = 'landing'

# ─── CSS Personalizado (Fundo Branco, Contraste Verde, Sem Âncoras de Link e Responsivo) ───
st.markdown("""
<style>
    /* Ocultar botão Implantar (Deploy), menu de 3 pontos, barra superior e sidebar na página pública */
    #MainMenu { visibility: hidden !important; display: none !important; }
    header[data-testid="stHeader"] { visibility: hidden !important; display: none !important; }
    [data-testid="stToolbar"] { visibility: hidden !important; display: none !important; }
    [data-testid="stDecoration"] { visibility: hidden !important; display: none !important; }
    [data-testid="stStatusWidget"] { visibility: hidden !important; display: none !important; }
    .stDeployButton, [data-testid="stAppDeployButton"] { visibility: hidden !important; display: none !important; }
    footer { visibility: hidden !important; display: none !important; }
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="stSidebarCollapsedControl"] { display: none !important; }

    /* Remover sinais de link / âncoras de URL automáticas e links externos de excepção */
    [data-testid="stHeaderActionElements"],
    [data-testid="stException"] a,
    .stMarkdown h1 a,
    .stMarkdown h2 a,
    .stMarkdown h3 a,
    .stMarkdown h4 a,
    .stMarkdown h5 a,
    .stMarkdown h6 a,
    a.header-anchor,
    svg.header-anchor {
        display: none !important;
        visibility: hidden !important;
        pointer-events: none !important;
        width: 0 !important;
        height: 0 !important;
    }

    /* Espaçamento principal responsivo */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2.5rem !important;
        max-width: 1180px !important;
    }

    /* Secção de Apresentação Limpa (Fundo Branco com Contraste Verde) */
    .intro-box {
        background: #FFFFFF;
        border: 2px solid #2E7D32;
        border-radius: 16px;
        padding: 2.5rem 2rem;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(46, 125, 50, 0.08);
    }
    .intro-icon {
        width: 56px;
        height: 56px;
        color: #1B5E20;
        stroke: currentColor;
        stroke-width: 2;
        stroke-linecap: round;
        stroke-linejoin: round;
        fill: none;
        margin-bottom: 0.75rem;
    }
    .intro-title {
        color: #1B5E20;
        font-size: 2.3rem;
        font-weight: 700;
        margin: 0 0 0.75rem 0;
        line-height: 1.2;
    }
    .intro-text {
        color: #37474F;
        font-size: 1.05rem;
        line-height: 1.7;
        max-width: 820px;
        margin: 0 auto;
    }

    /* Cards de Funcionalidades (usando divs puras sem tags h1/h3 para evitar âncoras de URL) */
    .feature-card {
        background: #FFFFFF;
        border: 1px solid #C8E6C9;
        border-top: 4px solid #2E7D32;
        border-radius: 12px;
        padding: 1.5rem 1.25rem;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.04);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        height: 100%;
        margin-bottom: 1rem;
    }
    .feature-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 18px rgba(27, 94, 32, 0.12);
    }
    .feature-icon {
        width: 44px;
        height: 44px;
        margin-bottom: 0.85rem;
        color: #2E7D32;
        stroke: currentColor;
        stroke-width: 1.8;
        stroke-linecap: round;
        stroke-linejoin: round;
        fill: none;
    }
    .feature-title {
        color: #1B5E20;
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .feature-description {
        color: #546E7A;
        font-size: 0.9rem;
        line-height: 1.55;
        margin: 0;
    }

    /* Secção de Passos */
    .section-heading {
        color: #1B5E20;
        font-size: 1.4rem;
        font-weight: 700;
        margin: 1.5rem 0 1rem 0;
        border-left: 4px solid #2E7D32;
        padding-left: 0.75rem;
    }

    /* Botão primário */
    .stButton > button[kind="primary"] {
        background-color: #2E7D32 !important;
        color: #FFFFFF !important;
        border: 1px solid #1B5E20 !important;
        border-radius: 8px !important;
        padding: 0.65rem 1.5rem !important;
        font-weight: 600 !important;
    }
    .stButton > button[kind="primary"]:hover {
        background-color: #1B5E20 !important;
        box-shadow: 0 4px 12px rgba(27, 94, 32, 0.25) !important;
    }
    .stButton > button[kind="secondary"] {
        background-color: #FFFFFF !important;
        color: #1B5E20 !important;
        border: 1.5px solid #2E7D32 !important;
        border-radius: 8px !important;
        padding: 0.65rem 1.5rem !important;
        font-weight: 600 !important;
    }
    .stButton > button[kind="secondary"]:hover {
        background-color: #F1F8E9 !important;
    }

    /* Formulário de Autenticação */
    .auth-title {
        color: #1B5E20;
        font-size: 1.6rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.25rem;
    }
    .auth-subtitle {
        color: #616161;
        font-size: 0.95rem;
        text-align: center;
        margin-bottom: 1.5rem;
    }

    /* Responsividade para Tablets e Telemóveis */
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
            min-width: 260px !important;
        }
    }

    @media (max-width: 640px) {
        .block-container {
            padding-top: 1rem !important;
            padding-left: 0.75rem !important;
            padding-right: 0.75rem !important;
        }
        .intro-box {
            padding: 1.5rem 1rem;
        }
        .intro-title {
            font-size: 1.65rem;
        }
        .intro-text {
            font-size: 0.95rem;
        }
        [data-testid="column"] {
            flex: 1 1 100% !important;
            min-width: 100% !important;
        }
        .feature-card {
            padding: 1.25rem 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# ─── Selector de Idioma no Topo ───
render_seletor_idioma("app")


def render_landing_page():
    """Renderiza a página inicial informativa para o agricultor (sem tags de cabeçalho que geram links)."""
    st.markdown(f"""
    <div class="intro-box">
        <svg class="intro-icon" viewBox="0 0 24 24">
            <path d="M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10z"/>
            <path d="M12 22v-8.5"/>
            <path d="M12 13.5a4.5 4.5 0 0 1 0-9 4.5 4.5 0 0 1 0 9z"/>
            <path d="M12 4.5v-2.5"/>
            <path d="M12 16.5c-2.5 0-4.5-2-4.5-4.5"/>
            <path d="M12 16.5c2.5 0 4.5-2 4.5-4.5"/>
        </svg>
        <div class="intro-title">{t('app_titulo')}</div>
        <p class="intro-text">
            {t('landing_subtitulo')}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Botões de acção principais
    _, col_cta1, col_cta2, _ = st.columns([1.5, 2, 2, 1.5])
    with col_cta1:
        if st.button(t('btn_entrar_conta'), use_container_width=True, type="primary"):
            st.session_state['vista_actual'] = 'auth'
            st.rerun()
    with col_cta2:
        if st.button(t('btn_cadastrar_agricultor'), use_container_width=True, type="secondary"):
            st.session_state['vista_actual'] = 'auth'
            st.rerun()

    # Funcionalidades Principais (usando <div class="feature-title"> em vez de <h3> para não criar âncoras de URL)
    st.markdown(f'<div class="section-heading">{t("sec_recursos")}</div>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="feature-card">
            <svg class="feature-icon" viewBox="0 0 24 24">
                <path d="M14 14.76V3.5a2.5 2.5 0 0 0-5 0v11.26a4.5 4.5 0 1 0 5 0z"/>
            </svg>
            <div class="feature-title">{t('feat1_titulo')}</div>
            <p class="feature-description">
                {t('feat1_desc')}
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="feature-card">
            <svg class="feature-icon" viewBox="0 0 24 24">
                <path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/>
            </svg>
            <div class="feature-title">{t('feat2_titulo')}</div>
            <p class="feature-description">
                {t('feat2_desc')}
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="feature-card">
            <svg class="feature-icon" viewBox="0 0 24 24">
                <path d="M3 3v18h18"/>
                <path d="M18.7 8l-5.1 5.2-2.8-2.7L7 14.3"/>
            </svg>
            <div class="feature-title">{t('feat3_titulo')}</div>
            <p class="feature-description">
                {t('feat3_desc')}
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="feature-card">
            <svg class="feature-icon" viewBox="0 0 24 24">
                <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
                <polyline points="22 4 12 14.01 9 11.01"/>
            </svg>
            <div class="feature-title">{t('feat4_titulo')}</div>
            <p class="feature-description">
                {t('feat4_desc')}
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Como funciona passo a passo
    st.markdown(f'<div class="section-heading">{t("sec_fluxo")}</div>', unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.markdown(f"""
        <div class="feature-card">
            <svg class="feature-icon" viewBox="0 0 24 24">
                <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                <circle cx="8.5" cy="7" r="4"/>
                <line x1="20" x2="20" y1="8" y2="14"/>
                <line x1="23" x2="17" y1="11" y2="11"/>
            </svg>
            <div class="feature-title">{t('step1_titulo')}</div>
            <p class="feature-description">
                {t('step1_desc')}
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown(f"""
        <div class="feature-card">
            <svg class="feature-icon" viewBox="0 0 24 24">
                <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                <line x1="16" y1="2" x2="16" y2="6"/>
                <line x1="8" y1="2" x2="8" y2="6"/>
                <line x1="3" y1="10" x2="21" y2="10"/>
            </svg>
            <div class="feature-title">{t('step2_titulo')}</div>
            <p class="feature-description">
                {t('step2_desc')}
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_c:
        st.markdown(f"""
        <div class="feature-card">
            <svg class="feature-icon" viewBox="0 0 24 24">
                <circle cx="12" cy="12" r="10"/>
                <polyline points="12 6 12 12 16 14"/>
            </svg>
            <div class="feature-title">{t('step3_titulo')}</div>
            <p class="feature-description">
                {t('step3_desc')}
            </p>
        </div>
        """, unsafe_allow_html=True)


def render_auth_page():
    """Renderiza a vista de Login, Cadastro e Recuperação de Senha do agricultor."""
    col_left, col_center, col_right = st.columns([1, 2.2, 1])

    with col_center:
        if st.button(t('btn_voltar_inicio'), type="secondary"):
            st.session_state['vista_actual'] = 'landing'
            st.rerun()

        st.markdown(f"""
        <div class="auth-title">{t('auth_titulo')}</div>
        <div class="auth-subtitle">{t('auth_subtitulo')}</div>
        """, unsafe_allow_html=True)

        tab_login, tab_cadastro, tab_recuperar = st.tabs([
            t('btn_entrar_conta'),
            t('btn_cadastrar_agricultor'),
            t('tab_recuperar')
        ])

        # ─── Aba de Login ───
        with tab_login:
            with st.form("form_login", clear_on_submit=False):
                telefone = st.text_input(
                    t('lbl_telefone'),
                    placeholder="Ex: 841234567",
                    help=t('help_telefone_login')
                )
                senha = st.text_input(
                    t('lbl_senha'),
                    type="password",
                    placeholder=t('ph_senha')
                )

                btn_login = st.form_submit_button(
                    t('btn_entrar'),
                    use_container_width=True,
                    type="primary"
                )

                if btn_login:
                    if not telefone or not senha:
                        st.error(t('err_login_vazio'))
                    else:
                        usuario = autenticar(telefone.strip(), senha)
                        if usuario:
                            st.session_state['autenticado'] = True
                            st.session_state['agricultor_id'] = usuario['id']
                            st.session_state['agricultor_nome'] = usuario['nome_completo']
                            st.session_state['agricultor_dados'] = usuario
                            # Usar o idioma seleccionado na sessão ou o idioma guardado do agricultor
                            if usuario.get('idioma') and st.session_state.get('idioma', 'pt') == 'pt':
                                definir_idioma(usuario['idioma'])
                            st.switch_page("pages/1_Dashboard.py")
                        else:
                            st.error(t('err_login_invalido'))

        # ─── Aba de Cadastro ───
        with tab_cadastro:
            with st.form("form_cadastro", clear_on_submit=True):
                nome_completo = st.text_input(
                    t('lbl_nome_completo'),
                    placeholder=t('ph_nome_completo')
                )

                nome_machamba = st.text_input(
                    t('lbl_nome_machamba'),
                    placeholder=t('ph_nome_machamba')
                )

                col1, col2 = st.columns(2)
                with col1:
                    provincias = [
                        'Cidade de Maputo', 'Província de Maputo', 'Gaza',
                        'Inhambane', 'Sofala', 'Manica', 'Tete',
                        'Zambézia', 'Nampula', 'Cabo Delgado', 'Niassa'
                    ]
                    provincia = st.selectbox(t('lbl_provincia'), provincias)

                with col2:
                    distrito = st.text_input(
                        t('lbl_distrito'),
                        placeholder="Ex: Boane, Manhiça, Chókwè"
                    )

                col3, col4 = st.columns(2)
                with col3:
                    telefone_reg = st.text_input(
                        t('lbl_telefone_obrig'),
                        placeholder="Ex: 841234567"
                    )
                with col4:
                    email_reg = st.text_input(
                        t('lbl_email_opc'),
                        placeholder="exemplo@dominio.com"
                    )

                col5, col6 = st.columns(2)
                with col5:
                    senha_reg = st.text_input(
                        t('lbl_senha_min'),
                        type="password"
                    )
                with col6:
                    senha_confirmar = st.text_input(
                        t('lbl_confirmar_senha'),
                        type="password"
                    )

                st.divider()
                st.markdown(t('sec_dados_agronomicos'))

                col7, col8 = st.columns(2)
                with col7:
                    culturas = [
                        'Milho', 'Arroz', 'Feijão', 'Mandioca', 'Hortícolas',
                        'Fruteiras', 'Cana-de-Açúcar', 'Algodão', 'Tabaco',
                        'Amendoim', 'Soja', 'Gergelim', 'Outros'
                    ]
                    cultura = st.selectbox(
                        t('lbl_cultura_principal'),
                        culturas,
                        format_func=traduzir_cultura
                    )

                with col8:
                    area = st.number_input(
                        t('lbl_area_ha'),
                        min_value=0.1, max_value=10000.0,
                        value=1.0, step=0.5,
                        format="%.1f"
                    )

                btn_cadastro = st.form_submit_button(
                    t('btn_concluir_cadastro'),
                    use_container_width=True,
                    type="primary"
                )

                if btn_cadastro:
                    erros = []
                    if not nome_completo or len(nome_completo.strip()) < 3:
                        erros.append(t('err_nome_curto'))
                    if not nome_machamba:
                        erros.append(t('err_machamba_obrig'))
                    if not telefone_reg or len(telefone_reg.strip()) < 8:
                        erros.append(t('err_telefone_curto'))
                    if not senha_reg or len(senha_reg) < 6:
                        erros.append(t('err_senha_curta'))
                    if senha_reg != senha_confirmar:
                        erros.append(t('err_senhas_diferentes'))

                    if erros:
                        for erro in erros:
                            st.error(erro)
                    else:
                        sucesso, msg = registar_agricultor({
                            'nome_completo': nome_completo.strip(),
                            'nome_machamba': nome_machamba.strip(),
                            'provincia': provincia,
                            'distrito': distrito.strip(),
                            'telefone': telefone_reg.strip(),
                            'email': email_reg.strip(),
                            'senha': senha_reg,
                            'cultura_principal': cultura,
                            'area_hectares': area,
                            'idioma': obter_idioma(),
                        })

                        if sucesso:
                            st.success(msg)
                            st.info(t('msg_conta_criada'))
                        else:
                            st.error(msg)

        # ─── Aba de Recuperar Senha ───
        with tab_recuperar:
            st.markdown(t('rec_instrucoes'))
            with st.form("form_recuperar_senha", clear_on_submit=True):
                tel_rec = st.text_input(
                    t('lbl_tel_registado'),
                    placeholder="Ex: 841234567"
                )
                machamba_rec = st.text_input(
                    t('lbl_machamba_registada'),
                    placeholder=t('ph_nome_machamba')
                )
                col_r1, col_r2 = st.columns(2)
                with col_r1:
                    nova_senha_rec = st.text_input(
                        t('lbl_nova_senha_min'),
                        type="password"
                    )
                with col_r2:
                    conf_senha_rec = st.text_input(
                        t('lbl_conf_nova_senha'),
                        type="password"
                    )

                btn_recuperar = st.form_submit_button(
                    t('btn_redefinir_senha'),
                    use_container_width=True,
                    type="primary"
                )

                if btn_recuperar:
                    if not tel_rec or not machamba_rec:
                        st.error(t('err_rec_campos'))
                    elif not nova_senha_rec or len(nova_senha_rec) < 6:
                        st.error(t('err_senha_curta'))
                    elif nova_senha_rec != conf_senha_rec:
                        st.error(t('err_senhas_diferentes'))
                    else:
                        ok, mensagem = redefinir_senha(tel_rec, machamba_rec, nova_senha_rec)
                        if ok:
                            st.success(mensagem)
                        else:
                            st.error(mensagem)


# ─── Executar Vista Correspondente ───
if st.session_state.get('vista_actual') == 'auth':
    render_auth_page()
else:
    render_landing_page()
