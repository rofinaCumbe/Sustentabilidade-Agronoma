"""
Sustentabilidade Agrónoma — Chatbot com IA (Botão no Topo da Página)
Implementa um assistente conversacional moderno e interactivo para:
1. Responder dúvidas frequentes (FAQ)
2. Guiar o utilizador no onboarding passo a passo
3. Explicar termos técnicos agronómicos (ET0, lâmina de água, humidade volumétrica, mulching, etc.)
4. Sugerir acções baseadas no contexto em tempo real (página actual, clima, machamba e regas do dia)
Suporta Ollama local (http://localhost:11434), API Gemini e Motor Especialista Agronómico integrado,
nos 5 idiomas do sistema (Português, Changana, Ronga, Makhuwa e Sena).
"""

import os
import re
import unicodedata
import requests
import streamlit as st

from utils.i18n import obter_idioma, t, IDIOMAS, traduzir_cultura
from utils.database import (
    obter_agricultor, contar_irrigacoes_hoje,
    calcular_agua_total, calcular_streak_irrigacao, obter_actividades
)
from utils.weather import CIDADES_MOCAMBIQUE, buscar_dados_clima, processar_dados_actuais, processar_previsao_5dias
from utils.irrigation import avaliar_irrigacao_actual


# ─── Textos Multi-Idioma da Interface do Chatbot ───

UI_CHAT = {
    'btn_abrir': {
        'pt': '🤖 Assistente IA',
        'changana': '🤖 Mupfuni wa IA',
        'ronga': '🤖 Mupfuni wa IA',
        'makhuwa': '🤖 Namakhaliherya IA',
        'sena': '🤖 Mphedzi wa IA',
    },
    'btn_fechar': {
        'pt': '✖ Fechar Assistente IA',
        'changana': '✖ Pfala Mupfuni wa IA',
        'ronga': '✖ Pfala Mupfuni wa IA',
        'makhuwa': '✖ Owalela Namakhaliherya IA',
        'sena': '✖ kufunga Mphedzi wa IA',
    },
    'titulo_modal': {
        'pt': 'Assistente IA — Sustentabilidade Agrónoma',
        'changana': 'Mupfuni wa IA — Vuhlayisi bya Vurimi',
        'ronga': 'Mupfuni wa IA — Vuhlayisi bya Vurimi',
        'makhuwa': 'Namakhaliherya IA — Okhapelela wa Olima',
        'sena': 'Mphedzi wa IA — Kukoya Ulimi',
    },
    'subtitulo_modal': {
        'pt': 'Onboarding · Termos Técnicos · Dúvidas Frequentes · Acções Contextuais',
        'changana': 'KuSungula · Marito ya Vurimi · Swivutiso · Switsundzuxo',
        'ronga': 'KuSungula · Marito ya Vurimi · Swivutiso · Switsundzuxo',
        'makhuwa': 'Opacerya · Masu a Olima · Makoho · Miruku',
        'sena': 'Kutoma · Mafala a Ulimi · Mibvundzo · Upungu',
    },
    'chip_onboarding': {
        'pt': '🚀 Guia de Onboarding',
        'changana': '🚀 Ndlela yo Sungula',
        'ronga': '🚀 Ndlela yo Sungula',
        'makhuwa': '🚀 Mweettelo Woopacerya',
        'sena': '🚀 Ndandanda Yakutoma',
    },
    'chip_termos': {
        'pt': '📖 Termos Técnicos',
        'changana': '📖 Marito ya Vurimi',
        'ronga': '📖 Marito ya Vurimi',
        'makhuwa': '📖 Masu a Olima',
        'sena': '📖 Mafala a Ulimi',
    },
    'chip_accao': {
        'pt': '🎯 Sugerir Acções para Mim',
        'changana': '🎯 Xitsundzuxo xa Mina',
        'ronga': '🎯 Xitsundzuxo xa Mina',
        'makhuwa': '🎯 Miruku sa Ematta Aka',
        'sena': '🎯 Upungu wa Munda Wanga',
    },
    'chip_faq': {
        'pt': '❓ Dúvidas Frequentes',
        'changana': '❓ Swivutiso swo Toloveleka',
        'ronga': '❓ Swivutiso swo Toloveleka',
        'makhuwa': '❓ Makoho Oolimaleliwa',
        'sena': '❓ Mibvundzo Yakudzoloereka',
    },
    'placeholder_prompt': {
        'pt': 'Coloque aqui a sua questão (ex: O que é ET0? Como começar? Clima em Nampula?)...',
        'changana': 'Tsala xivutiso xa wena laha (xik: I yini ET0? Ndzi sungula njhani?)...',
        'ronga': 'Tsala xivutiso xa wena laha (xik: I yini ET0? Ndzi sungula njhani?)...',
        'makhuwa': 'Mulepe nikoho nanyu va (nthoo: Exeeni ET0? Kinpacerya sai?)...',
        'sena': 'Lembani m\'bvundzo wanu pano (cits: Ninji ET0? Ndinatoma tani?)...',
    },
    'btn_enviar': {
        'pt': 'Enviar ➤',
        'changana': 'Rhumela ➤',
        'ronga': 'Rhumela ➤',
        'makhuwa': 'Orumiha ➤',
        'sena': 'Kutumiza ➤',
    },
    'btn_limpar': {
        'pt': '🗑️ Limpar conversa',
        'changana': '🗑️ Sula mabulo',
        'ronga': '🗑️ Sula mabulo',
        'makhuwa': '🗑️ Ofuta mwaha',
        'sena': '🗑️ Kufudza makani',
    },
}


def _ui(chave: str) -> str:
    idioma = obter_idioma()
    return UI_CHAT.get(chave, {}).get(idioma) or UI_CHAT.get(chave, {}).get('pt', chave)


def _normalizar(texto: str) -> str:
    """Remove acentos e converte para minúsculas."""
    texto_nfkd = unicodedata.normalize('NFKD', texto.lower())
    return ''.join(c for c in texto_nfkd if not unicodedata.combining(c))


def _obter_contexto_completo(pagina_actual: str = "geral") -> dict:
    """
    Recolhe todo o contexto actual do utilizador, da página onde se encontra,
    da sua machamba, das actividades do dia e dos dados meteorológicos em memória.
    """
    ctx = {
        'pagina': pagina_actual,
        'autenticado': bool(st.session_state.get('autenticado')),
        'idioma': obter_idioma(),
        'cidade_dashboard': st.session_state.get('cidade_dashboard', 'Maputo'),
        'clima_actual': st.session_state.get('ultimo_clima_actual'),
        'avaliacao_irrigacao': st.session_state.get('ultima_avaliacao_irrigacao'),
        'agricultor': None,
        'irrigacoes_hoje': 0,
        'agua_total': 0.0,
        'streak': 0,
        'total_actividades': 0,
    }

    if ctx['autenticado'] and st.session_state.get('agricultor_id'):
        agr_id = st.session_state['agricultor_id']
        agr = obter_agricultor(agr_id)
        if agr:
            ctx['agricultor'] = agr
            ctx['irrigacoes_hoje'] = contar_irrigacoes_hoje(agr_id)
            ctx['agua_total'] = calcular_agua_total(agr_id)
            ctx['streak'] = calcular_streak_irrigacao(agr_id)
            ctx['total_actividades'] = len(obter_actividades(agr_id))

    return ctx


def _gerar_dica_contextual_automatica(ctx: dict) -> str:
    """Gera uma recomendação proactiva com base no contexto actual do utilizador."""
    idioma = ctx['idioma']
    if not ctx['autenticado']:
        textos = {
            'pt': "💡 **Contexto Actual (Visitante):** Ainda não iniciou sessão. Clique em **Cadastrar Agricultor** para registar a sua machamba ou clique em **🚀 Guia de Onboarding** abaixo!",
            'changana': "💡 **Xitsundzuxo:** A wu se nghena. Tlilika **Tsarisa Murimi** ku tsarisa nsimu ya wena kumbe **🚀 Ndlela yo Sungula**!",
            'ronga': "💡 **Xitsundzuxo:** A wu se nghena. Tlilika **Tsarisa Murimi** ku tsarisa nsimu ya wena kumbe **🚀 Ndlela yo Sungula**!",
            'makhuwa': "💡 **Miruku:** Nlelo khamukenle. Muthanle **Olepiha Namalima** wiira mulepihe ematta anyu.",
            'sena': "💡 **Upungu:** Mudzati kupita. Dingani **Kulembesa Mulimi** toera kulembesa munda wanu.",
        }
        return textos.get(idioma, textos['pt'])

    agr = ctx['agricultor']
    nome = agr['nome_completo'].split()[0] if agr else 'Agricultor'
    aval = ctx.get('avaliacao_irrigacao')

    if aval and aval.get('nivel') in ('URGENTE', 'ALTO') and ctx['irrigacoes_hoje'] == 0:
        area = agr.get('area_hectares', 1.0) or 1.0
        litros = aval.get('lamina_mm', 0) * area * 10000
        return (
            f"⚠️ **Acção Sugerida para {nome}:** O nível de irrigação em **{ctx['cidade_dashboard']}** está **{aval['nivel']}** "
            f"({aval['lamina_mm']} mm ≈ **{litros:,.0f} L** para os seus {area:.1f} ha) e ainda não registou rega hoje. "
            f"Horário recomendado: **{aval['horario_ideal']}**."
        )

    if ctx['irrigacoes_hoje'] == 0:
        return (
            f"🎯 **Contexto de {nome} ({agr['nome_machamba']}):** Ainda não registou actividades de irrigação hoje "
            f"(Streak actual: **{ctx['streak']} dias**). Verifique o semáforo no **Painel de Irrigação** e registe em **Controlo de Actividades**."
        )

    return (
        f"✅ **Bom trabalho, {nome}!** Já concluiu **{ctx['irrigacoes_hoje']} irrigação(ões)** hoje na machamba **{agr['nome_machamba']}** "
        f"e mantém uma sequência de **{ctx['streak']} dia(s)** consecutivos!"
    )


def _construir_prompt_sistema(ctx: dict) -> str:
    """Constrói o system prompt rico em contexto para Ollama ou Gemini."""
    nome_idioma = IDIOMAS.get(ctx['idioma'], 'Português')
    info_user = "Utilizador visitante (ainda não autenticado)."
    if ctx['agricultor']:
        a = ctx['agricultor']
        info_user = (
            f"Agricultor autenticado: {a['nome_completo']} (ID: {a['id']}), "
            f"Machamba: {a['nome_machamba']}, Província: {a['provincia']}, "
            f"Cultura principal: {a.get('cultura_principal')}, Área: {a.get('area_hectares')} ha, "
            f"Irrigações concluídas hoje: {ctx['irrigacoes_hoje']}, "
            f"Água total acumulada: {ctx['agua_total']:,.0f} L, Streak: {ctx['streak']} dias."
        )

    info_clima = ""
    if ctx.get('clima_actual') and ctx.get('avaliacao_irrigacao'):
        c = ctx['clima_actual']
        av = ctx['avaliacao_irrigacao']
        info_clima = (
            f"Clima actual em {ctx['cidade_dashboard']}: {c['temperatura']}°C, Humidade {c['humidade_relativa']}%, "
            f"Vento {c['vento']} km/h, Chuva {c['precipitacao']} mm, ET0 {c['et0_hoje']} mm/dia. "
            f"Semáforo: {av['rotulo']} ({av['pontuacao']}/100), Lâmina sugerida: {av['lamina_mm']} mm, "
            f"Horário ideal: {av['horario_ideal']}."
        )

    return (
        "És o Assistente IA oficial da plataforma 'Sustentabilidade Agrónoma' em Moçambique.\n"
        f"Responde SEMPRE no idioma: {nome_idioma} (código: {ctx['idioma']}), de forma clara, empática, estruturada e concisa.\n"
        "Os teus 4 objectivos principais são:\n"
        "1. Responder dúvidas frequentes sobre o sistema (login, recuperação de senha com telefone + nome da machamba, exportação CSV, troca de idioma).\n"
        "2. Guiar o utilizador no onboarding passo a passo (1. Cadastrar machamba -> 2. Ver Semáforo e Previsão de 5 dias no Dashboard -> 3. Registar tarefas e litros em Actividades -> 4. Gerir Perfil).\n"
        "3. Explicar termos técnicos agronómicos de forma simples (ET0 Evapotranspiração FAO, Lâmina de água em mm = L/m², Humidade volumétrica do solo m³/m³, Stress hídrico, Mulching/cobertura morta, rega gota-a-gota vs aspersão).\n"
        "4. Sugerir acções práticas baseadas no contexto actual do agricultor:\n"
        f"   - Página actual: {ctx['pagina']}\n"
        f"   - {info_user}\n"
        f"   - {info_clima}\n"
    )


_ollama_disponivel = None if not os.environ.get("VERCEL") else False

def _tentar_ollama_ou_gemini(pergunta: str, ctx: dict, historico: list[dict]) -> tuple[str | None, str]:
    """
    1º Tenta usar Ollama local em http://localhost:11434 (auto-detectando o modelo instalado).
    2º Tenta usar a API Gemini se GEMINI_API_KEY estiver definida.
    Retorna (resposta, nome_motor) ou (None, 'AgroIA Contextual').
    """
    global _ollama_disponivel
    prompt_sistema = _construir_prompt_sistema(ctx)

    # 1. Tentar Ollama Local (se disponível)
    if _ollama_disponivel is not False:
        ollama_url = os.environ.get("OLLAMA_HOST", "http://localhost:11434").rstrip("/")
        try:
            tags_resp = requests.get(f"{ollama_url}/api/tags", timeout=0.5)
            if tags_resp.status_code == 200:
                _ollama_disponivel = True
                modelos = tags_resp.json().get("models", [])
                if modelos:
                    modelo_nome = modelos[0].get("name", "llama3")
                    mensagens_ollama = [{"role": "system", "content": prompt_sistema}]
                    for m in historico[-6:]:
                        mensagens_ollama.append({"role": m["role"], "content": m["content"]})
                    mensagens_ollama.append({"role": "user", "content": pergunta})

                    chat_resp = requests.post(
                        f"{ollama_url}/api/chat",
                        json={"model": modelo_nome, "messages": mensagens_ollama, "stream": False},
                        timeout=15,
                    )
                    if chat_resp.status_code == 200:
                        conteudo = chat_resp.json().get("message", {}).get("content", "").strip()
                        if conteudo:
                            return conteudo, f"Ollama ({modelo_nome})"
            else:
                _ollama_disponivel = False
        except Exception:
            _ollama_disponivel = False

    # 2. Tentar Gemini API
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if api_key:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
            payload = {
                "system_instruction": {"parts": [{"text": prompt_sistema}]},
                "contents": [{"parts": [{"text": pergunta}]}],
            }
            resp = requests.post(url, json=payload, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                texto = data["candidates"][0]["content"]["parts"][0]["text"]
                return texto, "Gemini AI"
        except Exception:
            pass

    return None, "AgroIA Contextual"


def _consultar_clima_cidade_na_pergunta(q_norm: str, ctx: dict) -> str | None:
    """Consulta em tempo real a API Open-Meteo caso o utilizador mencione uma cidade/província."""
    mapa_busca = {
        'maputo': 'Maputo', 'beira': 'Beira', 'sofala': 'Beira',
        'nampula': 'Nampula', 'quelimane': 'Quelimane', 'zambezia': 'Quelimane',
        'tete': 'Tete', 'chimoio': 'Chimoio', 'manica': 'Chimoio',
        'lichinga': 'Lichinga', 'niassa': 'Lichinga', 'pemba': 'Pemba',
        'cabo delgado': 'Pemba', 'maxixe': 'Maxixe', 'inhambane': 'Maxixe',
        'xai-xai': 'Xai-Xai', 'xai xai': 'Xai-Xai', 'gaza': 'Xai-Xai',
    }

    cidade_detectada = None
    for chave, nome_cidade in mapa_busca.items():
        if chave in q_norm:
            cidade_detectada = nome_cidade
            break

    if not cidade_detectada:
        return None

    coords = CIDADES_MOCAMBIQUE[cidade_detectada]
    dados_api = buscar_dados_clima(coords['lat'], coords['lon'])
    if not dados_api:
        return None

    actuais = processar_dados_actuais(dados_api)
    df_prev = processar_previsao_5dias(dados_api)
    aval = avaliar_irrigacao_actual(actuais, df_prev)

    area_ha = (ctx['agricultor'].get('area_hectares', 1.0) or 1.0) if ctx.get('agricultor') else 1.0
    litros_area = aval['lamina_mm'] * area_ha * 10000

    return (
        f"🌤️ **Análise Agrometeorológica em Tempo Real — {cidade_detectada} ({coords['provincia']}):**\n\n"
        f"- **Temperatura Actual:** {actuais['temperatura']:.1f} °C (Sensação: {actuais['sensacao_termica']:.1f} °C)\n"
        f"- **Humidade Relativa:** {actuais['humidade_relativa']}% · **Vento:** {actuais['vento']:.0f} km/h\n"
        f"- **Precipitação Actual:** {actuais['precipitacao']:.1f} mm · **$ET_0$ (Evapotranspiração):** {actuais['et0_hoje']:.1f} mm/dia\n"
        f"- **Semáforo de Irrigação:** **{aval['rotulo']}** (Pontuação: **{aval['pontuacao']}/100**)\n"
        f"- **Lâmina Recomendada:** **{aval['lamina_mm']} mm** (≈ **{litros_area:,.0f} litros** para {area_ha:.1f} ha)\n"
        f"- **Acção Sugerida:** {aval['descricao']} Regar preferencialmente às **{aval['horario_ideal']}**."
    )


def gerar_resposta_ia(pergunta: str, pagina_actual: str = "geral", historico: list[dict] = None) -> tuple[str, str]:
    """
    Gera resposta para os 4 pilares (Onboarding, Termos Técnicos, FAQ, Sugestões Contextuais)
    no idioma activo. Retorna (texto_resposta, nome_motor).
    """
    ctx = _obter_contexto_completo(pagina_actual)
    idioma = ctx['idioma']

    # 1. Tentar Ollama ou Gemini se disponíveis
    resp_ext, motor = _tentar_ollama_ou_gemini(pergunta, ctx, historico or [])
    if resp_ext:
        return resp_ext, motor

    q = _normalizar(pergunta.strip())

    # 2. Consulta directa de cidade/província em tempo real
    info_cidade = _consultar_clima_cidade_na_pergunta(q, ctx)
    if info_cidade:
        return info_cidade, motor

    # ─── PILAR 1: ONBOARDING (Guiar o utilizador passo a passo) ───
    if any(p in q for p in [
        'onboarding', 'comecar', 'iniciar', 'passo a passo', 'como usar', 'novo utilizador',
        'primeiro passo', 'guia', 'ndlela yo sungula', 'mweettelo woopacerya', 'ndandanda yakutoma', 'tutorial'
    ]):
        estado_onboarding = (
            "✅ **Já está autenticado!** O seu próximo passo é verificar o **Painel de Irrigação** e registar a tarefa do dia em **Controlo de Actividades**."
            if ctx['autenticado'] else
            "👉 **Você está na Página Inicial:** Comece clicando no botão **Cadastrar Agricultor** para criar a sua conta gratuita."
        )
        respostas = {
            'pt': (
                "🚀 **Guia de Onboarding — Como Utilizar o Sustentabilidade Agrónoma Passo a Passo:**\n\n"
                f"{estado_onboarding}\n\n"
                "1. **Passo 1 — Cadastro da Machamba (`Página Inicial -> Cadastrar Agricultor`):**\n"
                "   - Registe o seu nome, número de telefone (usado para login), nome da machamba, província, **cultura principal** (ex: Milho, Hortícolas, Arroz) e a **área em hectares**.\n"
                "2. **Passo 2 — Consultar o Semáforo de Rega (`Painel de Irrigação`):**\n"
                "   - Seleccione a cidade mais próxima da sua machamba. Veja o **Semáforo de Irrigação** (de *Desnecessário* a *Urgente*), a **Lâmina de Água (mm)** convertida automaticamente em litros para a sua área e o **Calendário de 5 Dias**.\n"
                "3. **Passo 3 — Registar Tarefas do Campo (`Controlo de Actividades`):**\n"
                "   - Sempre que irrigar, adubar ou capinar, registe a hora de início/fim e os litros de água. O sistema calcula as suas horas trabalhadas e o seu **Streak** (dias consecutivos a cumprir a irrigação).\n"
                "4. **Passo 4 — Personalizar Idioma e Perfil (`🌐 Idioma` / `Dados do Agricultor`):**\n"
                "   - Pode usar a plataforma em **Português, Changana, Ronga, Makhuwa ou Sena** a qualquer momento no topo da página!"
            ),
            'changana': (
                "🚀 **Ndlela yo Sungula (Onboarding) — Matirhelo ya Sistema hi Magondzo ya 4:**\n\n"
                "1. **Goza ra 1 — Tsarisa Nsimu ya Wena:** Tlilika *Tsarisa Murimi*, u nghenisa vito, telefone, xifundzha, ximilana lexikulu ni vukulu bya nsimu (hectares).\n"
                "2. **Goza ra 2 — Languta Painel ra Kucheleta:** Kambela xikombiso xa kucheleta (Semáforo), mpimo wa mati hi litros ni maxelo ya masiku ya 5.\n"
                "3. **Goza ra 3 — Tsala Mintirho ya Siku:** Loko u heta kucheleta kumbe kuhlakula, tsala awara ni mati lama tirhisiweke ka *Vulawuri bya Mintirho*.\n"
                "4. **Goza ra 4 — Hlawula Lirimi:** Ehenhla ka pheji, hlawula *Português, Changana, Ronga, Makhuwa* kumbe *Sena*."
            ),
            'ronga': (
                "🚀 **Ndlela yo Sungula (Onboarding) — Matirhelo ya Sistema hi Magondzo ya 4:**\n\n"
                "1. **Goza ra 1 — Tsarisa Nsimu ya Wena:** Tlilika *Tsarisa Murimi*, u nghenisa vito, telefone, xifundzha, ximilana lexikulu ni vukulu bya nsimu (hectares).\n"
                "2. **Goza ra 2 — Languta Painel ra Kucheleta:** Kambela xikombiso xa kucheleta (Semáforo), mpimo wa mati hi litros ni maxelo ya masiku ya 5.\n"
                "3. **Goza ra 3 — Tsala Mintirho ya Siku:** Loko u heta kucheleta kumbe kuhlakula, tsala awara ni mati lama tirhisiweke ka *Vulawuri bya Mintirho*.\n"
                "4. **Goza ra 4 — Hlawula Lirimi:** A henhla ka pheji, hlawula *Português, Changana, Ronga, Makhuwa* kumbe *Sena*."
            ),
            'makhuwa': (
                "🚀 **Mweettelo Woopacerya (Onboarding) — Ikhato 4 so Orumeela Sistema:**\n\n"
                "1. **Ekhato 1 — Olepiha Ematta:** Muthanle *Olepiha Namalima*, muhele nsina, etelefone, eporovinsiya, mbewe ni hectares.\n"
                "2. **Ekhato 2 — Oweha Painel yo Ohela Maasi:** Moone ethoonyeryo yo ohela maasi, litros sa maasi ni ihapari sa mahiku 5.\n"
                "3. **Ekhato 3 — Olepa Miteko:** Mulepe miteko sa mmatta va *Oweha Miteko*.\n"
                "4. **Ekhato 4 — Othanla Nttaava:** Vasulu va epaxina, muthanle *Português, Changana, Ronga, Makhuwa* wala *Sena*."
            ),
            'sena': (
                "🚀 **Ndandanda Yakutoma (Onboarding) — Njira 4 Zakuphatisira Sistema:**\n\n"
                "1. **Njira 1 — Kulembesa Munda:** Dingani *Kulembesa Mulimi*, lembani dzina, telefone, provinsiya, mbeu na hectares.\n"
                "2. **Njira 2 — Kuyang'ana Painel ya Kuthirira:** Onani cidziwiso ca kuthirira, mpimo wa madzi (litros) na nyengo ya ntsiku 5.\n"
                "3. **Njira 3 — Kulemba Mabasa:** Lembani mabasa adacitwa pa *Kuyang'anira Mabasa*.\n"
                "4. **Njira 4 — Kusankhula Cilongero:** Pa ntsonga ya tsamba, sankhulani *Português, Changana, Ronga, Makhuwa* peno *Sena*."
            ),
        }
        return respostas.get(idioma, respostas['pt']), motor

    # ─── PILAR 2: EXPLICAR TERMOS TÉCNICOS ───
    if any(p in q for p in [
        'termo', 'tecnico', 'glossario', 'o que e et0', 'et0', 'evapotranspiracao',
        'lamina', 'humidade volumetrica', 'mulching', 'cobertura morta', 'stress hidrico',
        'gota a gota', 'aspersao', 'sulco', 'marito ya vurimi', 'masu a olima', 'mafala a ulimi',
        'significa', 'explicar', 'explica'
    ]):
        respostas = {
            'pt': (
                "📖 **Glossário de Termos Técnicos do Sistema (Explicados de Forma Simples):**\n\n"
                "- **🌡️ $ET_0$ (Evapotranspiração de Referência — mm/dia):** É a quantidade de água que o solo perde por evaporação do sol somada à água que as plantas transpiram num dia. Se a $ET_0$ hoje é de $5\\text{ mm/dia}$, significa que o campo perdeu cerca de $5\\text{ litros de água por m}^2$.\n"
                "- **💧 Lâmina de Água ($\text{mm}$):** É a altura de água que deve aplicar na rega para repor o que a planta perdeu. **Regra prática:** $1\\text{ mm} = 1\\text{ litro por m}^2 = 10\\,000\\text{ litros por hectare (ha)}$.\n"
                "- **🌱 Humidade Volumétrica do Solo ($\text{m}^3/\\text{m}^3$):** Mede a fracção do volume do solo (entre 3 e 9 cm de profundidade) que está preenchida por água. Valores abaixo de $0.15\\text{ m}^3/\\text{m}^3$ indicam solo seco; acima de $0.35\\text{ m}^3/\\text{m}^3$ indicam solo bem húmido.\n"
                "- **🥀 Stress Hídrico:** Sofre-se quando a planta perde mais água ($ET_0$ alta) do que consegue absorver pelas raízes, fechando os estomas e reduzindo a colheita.\n"
                "- **🍂 Cobertura Morta (*Mulching*):** Camada de capim seco, palha ou restos de cultura colocada sobre o solo ao redor das plantas para manter a terra fresca e reduzir a evaporação em até $40\\%$.\n"
                "- **🚿 Rega Gota-a-Gota vs Aspersão:** A rega gota-a-gota aplica água directamente na raiz (poupa até $50\\%$ de água e não sofre com o vento), enquanto a aspersão espalha água no ar (deve ser evitada quando o vento passa de $25\\text{ km/h}$)."
            ),
            'changana': (
                "📖 **Nhlamuselo ya Marito ya Vurimi:**\n\n"
                "- **🌡️ ET0 (Evapotranspiração):** I mpimo wa mati lama humaka emisaveni hi dyambu ni le swimilanini hi siku.\n"
                "- **💧 Lâmina ya Mati (mm):** **1 mm** yi vula **1 litro ya mati hi metro quadrado (1 L/m²)** kumbe **10.000 litros hi hectare**.\n"
                "- **🌱 Kutswaka ka Misava (m³/m³):** Mpimo wa mati lama nga ndzeni ka misava (3–9 cm).\n"
                "- **🍂 Mulching (Kufunengeta Misava):** Ku veka byasi lebyi omeke ehansi ka swimilana leswaku mati ma nga omi hi xihatla."
            ),
            'ronga': (
                "📖 **Nhlamuselo ya Marito ya Vurimi:**\n\n"
                "- **🌡️ ET0 (Evapotranspiração):** I mpimo wa mati lama humaka a misaveni hi dambu ni le swimilanini hi siku.\n"
                "- **💧 Lâmina ya Mati (mm):** **1 mm** yi hlaya **1 litro ya mati hi metro quadrado (1 L/m²)** kumbe **10.000 litros hi hectare**.\n"
                "- **🌱 Kutswaka ka Misava (m³/m³):** Mpimo wa mati lama nga ndzeni ka misava (3–9 cm).\n"
                "- **🍂 Mulching (Kufunengeta Misava):** Ku veka byanyi lebyi womeke a hansi ka swimilana leswaku mati ma nga womi hi xihatla."
            ),
            'makhuwa': (
                "📖 **Otaphulela Masu a Olima:**\n\n"
                "- **🌡️ ET0 (Evapotranspiração):** Mwaattelo wa maasi onivukula vathi ni mbewe khula nihiku.\n"
                "- **💧 Lâmina ya Maasi (mm):** **1 mm** enithoonyerya **1 litro wa khula metro quadrado (1 L/m²)** = **10.000 litros/ha**.\n"
                "- **🌱 Maasi a Vathi (m³/m³):** Maasi ari vathi va etthaya (3–9 cm).\n"
                "- **🍂 Mulching:** Ohela malaxi oowuma vathi va mbewe wiira maasi ahipwe mowaakuveya."
            ),
            'sena': (
                "📖 **Mafokotozero a Mafala a Ulimi:**\n\n"
                "- **🌡️ ET0 (Evapotranspiração):** Mpimo wa madzi anapwa m'mataka na m'mbeu pa ntsiku.\n"
                "- **💧 Lâmina ya Madzi (mm):** **1 mm** isabveka **1 litro pa metro quadrado (1 L/m²)** = **10.000 litros/ha**.\n"
                "- **🌱 Kubvumbwa kwa Mataka (m³/m³):** Mpimo wa madzi ali pantsi pa mataka (3–9 cm).\n"
                "- **🍂 Mulching:** Kuika maudzu adawuma pantsi pa mbeu toera kukoya madzi m'mataka."
            ),
        }
        return respostas.get(idioma, respostas['pt']), motor

    # ─── PILAR 3: SUGERIR ACÇÕES BASEADAS NO CONTEXTO ───
    if any(p in q for p in [
        'sugerir', 'accao', 'acoes', 'acao', 'o que devo fazer', 'recomendacao para mim',
        'minha machamba', 'meu resumo', 'xitsundzuxo xa mina', 'miruku sa ematta', 'upungu wa munda'
    ]):
        if not ctx['autenticado']:
            return (
                "🎯 **Acções Recomendadas para o Seu Contexto Actual (Visitante):**\n\n"
                "1. **Criar Conta ou Entrar:** Como ainda não iniciou sessão, clique em **Cadastrar Agricultor** para registar a sua machamba, província, cultura e hectares.\n"
                "2. **Escolher o Seu Idioma:** Utilize o selector no topo para navegar em **Português, Changana, Ronga, Makhuwa ou Sena**.\n"
                "3. **Consultar Clima Agora:** Mesmo sem login, pode perguntar-me aqui na caixa de prompt: *«Como está o clima hoje em Maputo / Beira / Nampula?»* e eu consulto os dados em tempo real para si!"
            ), motor

        agr = ctx['agricultor']
        cultura = agr.get('cultura_principal', 'Milho')
        cultura_trad = traduzir_cultura(cultura)
        area = agr.get('area_hectares', 1.0) or 1.0
        aval = ctx.get('avaliacao_irrigacao')
        clima = ctx.get('clima_actual')

        bloco_clima = ""
        if aval and clima:
            litros_hoje = aval['lamina_mm'] * area * 10000
            bloco_clima = (
                f"- **Decisão de Rega em {ctx['cidade_dashboard']}:** O semáforo indica **{aval['rotulo']}** ({aval['pontuacao']}/100) com {clima['temperatura']:.1f}°C.\n"
                f"- **Volume Recomendado para os seus {area:.1f} ha:** Aplicar **{aval['lamina_mm']} mm** (≈ **{litros_hoje:,.0f} litros** / {litros_hoje/1000:.1f} m³) no horário **{aval['horario_ideal']}**.\n"
            )
        else:
            bloco_clima = "- **Consultar o Painel:** Abra o **Painel de Irrigação** para carregar a previsão meteorológica de hoje da sua província.\n"

        accao_rega = (
            f"⚠️ **Registar Irrigação de Hoje:** Ainda tem **0 irrigações** registadas hoje. Após regar os seus **{area:.1f} ha de {cultura_trad}**, vá a **Controlo de Actividades** e registe a tarefa para aumentar o seu *streak* (actualmente em **{ctx['streak']} dias**)."
            if ctx['irrigacoes_hoje'] == 0 else
            f"✅ **Cumprimento Diário Garantido:** Já registou **{ctx['irrigacoes_hoje']} irrigação(ões)** hoje! Mantenha a monitorização da humidade do solo e evite regas adicionais nas horas de maior calor."
        )

        return (
            f"🎯 **Plano de Acção Contextualizado para {agr['nome_completo']} ({agr['nome_machamba']}):**\n\n"
            f"- **Perfil Activo:** {agr['provincia']} · Cultura: **{cultura_trad}** · Área: **{area:.1f} ha** · Água acumulada: **{ctx['agua_total']:,.0f} L**\n"
            f"{bloco_clima}"
            f"- {accao_rega}\n"
            f"- **Dica para {cultura_trad}:** Verifique a drenagem dos talhões e aplique cobertura morta (*mulching*) se a temperatura ultrapassar os $30^\\circ\\text{C}$."
        ), motor

    # ─── PILAR 4: DÚVIDAS FREQUENTES (FAQ) ───
    if any(p in q for p in [
        'duvidas frequentes', 'faq', 'perguntas frequentes', 'semaforo', 'senha',
        'recuperar', 'csv', 'exportar', 'actividade', 'swivutiso', 'makoho', 'mibvundzo',
        'litros', 'calcular', 'hectare', 'cultura', 'milho', 'arroz', 'feijao', 'horticola', 'mandioca'
    ]):
        area_ex = (ctx['agricultor'].get('area_hectares', 1.0) or 1.0) if ctx.get('agricultor') else 1.0
        match_ha = re.search(r'(\d+(?:[\.,]\d+)?)\s*(?:ha|hectare)', q)
        if match_ha:
            try:
                area_ex = float(match_ha.group(1).replace(',', '.'))
            except ValueError:
                pass

        return (
            "❓ **Respostas às Dúvidas Mais Frequentes sobre o Sistema:**\n\n"
            "1. **Como funciona o Semáforo de Irrigação?**\n"
            "   - Calcula uma pontuação de **0 a 100** com base na Temperatura, $ET_0$, Humidade, Vento e Chuva: 🔴 **Urgente** (70–100), 🟠 **Alto** (50–69), 🟡 **Moderado** (30–49), 🟢 **Baixo** (15–29) e 🔵 **Desnecessário** (0–14).\n"
            f"2. **Como converter a Lâmina (mm) em Litros para {area_ex:.1f} ha?**\n"
            f"   - Multiplica-se a lâmina (mm) por $10\\,000\\text{{ L/ha}}$. Para **{area_ex:.1f} ha**, cada $1\\text{{ mm}}$ requer **{area_ex * 10000:,.0f} litros** ({area_ex * 10:.1f} m³).\n"
            "3. **Esqueci a minha senha. Como recupero?**\n"
            "   - Na página de login, abra a aba **Recuperar Senha**, digite o seu **Telefone Registado** e o **Nome da Machamba Registada** para definir uma nova senha na hora.\n"
            "4. **Como exportar o histórico de actividades para Excel?**\n"
            "   - Em **Controlo de Actividades**, filtre o período desejado e clique no botão **Exportar CSV**.\n"
            "5. **Como alterar o idioma para Changana, Ronga, Makhuwa ou Sena?**\n"
            "   - Basta escolher a língua no selector **🌐 Idioma / Língua** no topo direito de qualquer ecrã."
        ), motor

    # ─── Resposta Contextual Inteligente para Qualquer Outra Questão ───
    dica_ctx = _gerar_dica_contextual_automatica(ctx)
    return (
        f"🤖 Recebi a sua questão: *«{pergunta.strip()}»*\n\n"
        f"{dica_ctx}\n\n"
        "Posso ajudá-lo imediatamente em qualquer uma destas 4 áreas (clique num botão rápido acima ou escreva na caixa de prompt):\n"
        "- 🚀 **Onboarding:** *«Como começar a usar o sistema passo a passo?»*\n"
        "- 📖 **Termos Técnicos:** *«O que significa ET0, lâmina de água, humidade volumétrica e mulching?»*\n"
        "- 🎯 **Acções Contextuais:** *«O que devo fazer hoje na minha machamba?»* ou *«Como está o clima em Maputo / Beira / Nampula?»*\n"
        "- ❓ **Dúvidas Frequentes:** *«Como funciona o semáforo? Como recuperar a senha ou exportar CSV?»*"
    ), motor


def _injetar_css_chat_bonito():
    """Injecta estilos CSS modernos para a janela de chat no topo."""
    st.markdown("""
    <style>
        .chat-top-card {
            background: #FFFFFF;
            border: 2px solid #2E7D32;
            border-radius: 16px;
            padding: 1rem 1.25rem;
            margin: 0.5rem 0 1.25rem 0;
            box-shadow: 0 8px 28px rgba(27, 94, 32, 0.14);
        }
        .chat-header-banner {
            background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 100%);
            color: #FFFFFF;
            padding: 0.9rem 1.2rem;
            border-radius: 12px;
            margin-bottom: 0.75rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            box-shadow: 0 3px 10px rgba(27, 94, 32, 0.18);
        }
        .chat-header-title {
            font-size: 1.08rem;
            font-weight: 700;
            margin: 0;
            color: #FFFFFF;
        }
        .chat-header-sub {
            font-size: 0.78rem;
            color: #E8F5E9;
            margin: 0.15rem 0 0 0;
        }
        .chat-status-badge {
            background: rgba(255, 255, 255, 0.18);
            border: 1px solid rgba(255, 255, 255, 0.35);
            color: #FFFFFF;
            padding: 0.25rem 0.65rem;
            border-radius: 999px;
            font-size: 0.73rem;
            font-weight: 600;
            white-space: nowrap;
        }
        .chat-context-banner {
            background: #F1F8E9;
            border-left: 4px solid #2E7D32;
            padding: 0.65rem 0.9rem;
            border-radius: 8px;
            font-size: 0.84rem;
            color: #1B5E20;
            margin-bottom: 0.75rem;
        }
    </style>
    """, unsafe_allow_html=True)


def render_painel_chat_topo(pagina_actual: str = "geral", key_prefix: str = "topo"):
    """
    Renderiza a janela bonita do Chatbot no topo da página quando o botão
    '🤖 Assistente IA' está activo, mantendo-se aberta durante toda a conversa.
    """
    _injetar_css_chat_bonito()

    idioma = obter_idioma()
    hist_key = f"chat_ia_hist_{idioma}"
    motor_key = f"chat_ia_motor_{idioma}"

    if hist_key not in st.session_state:
        st.session_state[hist_key] = [
            {"role": "assistant", "content": t('ia_boas_vindas')}
        ]
    if motor_key not in st.session_state:
        st.session_state[motor_key] = "AgroIA Contextual"

    ctx = _obter_contexto_completo(pagina_actual)
    dica_auto = _gerar_dica_contextual_automatica(ctx)

    with st.container(border=True):
        # Cabeçalho bonito do Chat
        st.markdown(f"""
        <div class="chat-header-banner">
            <div>
                <div class="chat-header-title">🤖 {_ui('titulo_modal')}</div>
                <div class="chat-header-sub">{_ui('subtitulo_modal')}</div>
            </div>
            <div class="chat-status-badge">🟢 {st.session_state[motor_key]}</div>
        </div>
        """, unsafe_allow_html=True)

        # Banner de Contexto Inteligente
        st.markdown(f'<div class="chat-context-banner">{dica_auto}</div>', unsafe_allow_html=True)

        # 4 Botões de Objectivos Principais (Onboarding, Termos Técnicos, Sugerir Acções, FAQ)
        c1, c2, c3, c4 = st.columns(4)
        pergunta_atalho = None
        with c1:
            if st.button(_ui('chip_onboarding'), key=f"{key_prefix}_b_onb", use_container_width=True):
                pergunta_atalho = _ui('chip_onboarding')
        with c2:
            if st.button(_ui('chip_termos'), key=f"{key_prefix}_b_ter", use_container_width=True):
                pergunta_atalho = _ui('chip_termos')
        with c3:
            if st.button(_ui('chip_accao'), key=f"{key_prefix}_b_acc", use_container_width=True):
                pergunta_atalho = _ui('chip_accao')
        with c4:
            if st.button(_ui('chip_faq'), key=f"{key_prefix}_b_faq", use_container_width=True):
                pergunta_atalho = _ui('chip_faq')

        # Janela de mensagens com scroll
        chat_container = st.container(height=320, border=True)
        with chat_container:
            for msg in st.session_state[hist_key]:
                avatar = "🧑‍🌾" if msg["role"] == "user" else "🌱"
                with st.chat_message(msg["role"], avatar=avatar):
                    st.markdown(msg["content"])

        # Caixa de Prompt Interactiva
        with st.form(key=f"{key_prefix}_prompt_form", clear_on_submit=True):
            col_in, col_sub = st.columns([4.2, 1.2])
            with col_in:
                prompt_user = st.text_input(
                    "Prompt",
                    placeholder=_ui('placeholder_prompt'),
                    label_visibility="collapsed",
                    key=f"{key_prefix}_txt"
                )
            with col_sub:
                enviado = st.form_submit_button(
                    _ui('btn_enviar'),
                    type="primary",
                    use_container_width=True
                )

        questao_final = None
        if pergunta_atalho:
            questao_final = pergunta_atalho
        elif enviado and prompt_user and prompt_user.strip():
            questao_final = prompt_user.strip()

        if questao_final:
            st.session_state[hist_key].append({"role": "user", "content": questao_final})
            resposta, motor_usado = gerar_resposta_ia(
                questao_final,
                pagina_actual=pagina_actual,
                historico=st.session_state[hist_key]
            )
            st.session_state[motor_key] = motor_usado
            st.session_state[hist_key].append({"role": "assistant", "content": resposta})
            st.rerun()

        # Rodapé com botão de limpar conversa
        if len(st.session_state[hist_key]) > 1:
            if st.button(_ui('btn_limpar'), key=f"{key_prefix}_clear"):
                st.session_state[hist_key] = [
                    {"role": "assistant", "content": t('ia_boas_vindas')}
                ]
                st.rerun()
