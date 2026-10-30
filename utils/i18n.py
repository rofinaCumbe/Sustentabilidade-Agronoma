"""
Sustentabilidade Agrónoma — Módulo de Internacionalização (Multi-Idioma)
Suporte para Português e línguas nacionais de Moçambique:
- Português (pt)
- Changana / Xichangana (changana)
- Ronga / Xironga (ronga)
- Makhuwa / Emakhuwa (makhuwa)
- Sena / Cisena (sena)
"""

import streamlit as st

IDIOMAS = {
    'pt': 'Português',
    'changana': 'Changana',
    'ronga': 'Ronga',
    'makhuwa': 'Makhuwa',
    'sena': 'Sena',
}

TRADUCOES = {
    # ─── Geral & Navegação ───
    'app_titulo': {
        'pt': 'Sustentabilidade Agrónoma',
        'changana': 'Vuhlayisi bya Vurimi',
        'ronga': 'Vuhlayisi bya Vurimi',
        'makhuwa': 'Okhapelela wa Olima',
        'sena': 'Kukoya Ulimi Wamasiku Onsene',
    },
    'seletor_idioma': {
        'pt': 'Idioma / Língua',
        'changana': 'Lirimi',
        'ronga': 'Lirimi',
        'makhuwa': 'Nttaava',
        'sena': 'Cilongero',
    },
    'nav_painel': {
        'pt': 'Painel de Irrigação',
        'changana': 'Painel ra Kucheleta',
        'ronga': 'Painel ra Kucheleta',
        'makhuwa': 'Painel yo Ohela Maasi',
        'sena': 'Painel ya Kuthirira',
    },
    'nav_actividades': {
        'pt': 'Controlo de Actividades',
        'changana': 'Vulawuri bya Mintirho',
        'ronga': 'Vulawuri bya Mintirho',
        'makhuwa': 'Oweha Miteko',
        'sena': 'Kuyang\'anira Mabasa',
    },
    'nav_perfil': {
        'pt': 'Dados do Agricultor',
        'changana': 'Mahungu ya Murimi',
        'ronga': 'Mahungu ya Murimi',
        'makhuwa': 'Ihapari sa Namalima',
        'sena': 'Mphangwa za Mulimi',
    },
    'nav_sair': {
        'pt': 'Terminar Sessão',
        'changana': 'Huma',
        'ronga': 'Huma',
        'makhuwa': 'Okhuma',
        'sena': 'Kubuluka',
    },

    # ─── Página Inicial (Landing Page) ───
    'landing_subtitulo': {
        'pt': (
            'Plataforma de apoio à decisão de irrigação e gestão de actividades agrícolas para Moçambique. '
            'Monitore a temperatura em tempo real na sua machamba ou plantação, identifique os dias e horários '
            'ideais para irrigar com base na previsão meteorológica de 5 dias e registe o cumprimento e horário '
            'de cada tarefa realizada no campo.'
        ),
        'changana': (
            ' xitirhisiwa xa kupfuna makungu ya kucheleta ni vulawuri bya mintirho ya vurimi eMoçambique. '
            'Langutisa kuhisa ka moya hi nkarhi wa kona ensin\'wini ya wena, tiva masiku ni minkarhi leyinene '
            'ya kucheleta hi kulandza xiyimo xa maxelo xa masiku ya 5, u tlhela u tsala mintirho hinkwayo leyi endliweke.'
        ),
        'ronga': (
            'Xitirhisiwa xa kupfuna makungu ya kucheleta ni vulawuri bya mintirho ya vurimi aMoçambique. '
            'Langutisa kuhisa ka moya hi nkarhi wa kona a nsin\'wini ya wena, tiva masiku ni minkarhi leyinene '
            'ya kucheleta hi kulandza xiyimo xa maxelo xa masiku ya 5, u tlhela u tsala mintirho hinkwayo leyi yendliweke.'
        ),
        'makhuwa': (
            'Ephurojekiti yo okhaliherya olaka wa ohela maasi ni oweha miteko sa olima oMoçambique. '
            'Moone oviha wa epheyo mowaakuveya mmatta mwanyu, musuwele mahiku ni ikatema sooloka '
            'so ohela maasi mweettela otaphulela wa epula wa mahiku 5 ni mulepe miteko soothene siri mpantta.'
        ),
        'sena': (
            'Ndandanda yakuphedza kusankhula kuthirira na kuyang\'anira mabasa a ulimi ku Moçambique. '
            'Onani kupisa kwa mphepo pa ndzidzi wene m\'munda mwanu, dziwani ntsiku na ndzidzi wadidi '
            'wakuthirira mukubverana na cidziwiso ca nyengo ca ntsiku 5 pontho lembani mabasa onsene adacitwa.'
        ),
    },
    'btn_entrar_conta': {
        'pt': 'Entrar na Conta',
        'changana': 'Nghena ka Akhawunti',
        'ronga': 'Nghena ka Akhawunti',
        'makhuwa': 'Okela mu Akhawunti',
        'sena': 'Kupita mu Akhawunti',
    },
    'btn_cadastrar_agricultor': {
        'pt': 'Cadastrar Agricultor',
        'changana': 'Tsarisa Murimi',
        'ronga': 'Tsarisa Murimi',
        'makhuwa': 'Olepiha Namalima',
        'sena': 'Kulembesa Mulimi',
    },
    'sec_recursos': {
        'pt': 'Recursos da Plataforma',
        'changana': ' leswi Kumekaka ka Plataforma',
        'ronga': 'Leswi Kumekaka ka Plataforma',
        'makhuwa': 'Itthu Siri mu Plataforma',
        'sena': 'Pinthu Piri mu Plataforma',
    },
    'feat1_titulo': {
        'pt': 'Monitoria Térmica Real',
        'changana': 'Kulangutisa Kuhisa ka Moya',
        'ronga': 'Kulangutisa Kuhisa ka Moya',
        'makhuwa': 'Oweha Oviha wa Epheyo',
        'sena': 'Kuyang\'anira Kupisa kwa Mphepo',
    },
    'feat1_desc': {
        'pt': 'Dados meteorológicos reais para as províncias de Moçambique, com previsão para 5 dias.',
        'changana': 'Mahungu ya maxelo ya ntiyiso ya swifundzha swa Moçambique, ni kuprofeta ka masiku ya 5.',
        'ronga': 'Mahungu ya maxelo ya ntiyiso ya swifundzha swa Moçambique, ni kuprofeta ka masiku ya 5.',
        'makhuwa': 'Ihapari sa epheyo ni epula sa iporovinsiya sa Moçambique, ni olaka wa mahiku 5.',
        'sena': 'Mphangwa za nyengo za m\'maprovinsiya a Moçambique, na cidziwiso ca ntsiku 5.',
    },
    'feat2_titulo': {
        'pt': 'Decisão de Irrigação',
        'changana': 'Makungu ya Kucheleta',
        'ronga': 'Makungu ya Kucheleta',
        'makhuwa': 'Olaka wa Ohela Maasi',
        'sena': 'Cisankhulo ca Kuthirira',
    },
    'feat2_desc': {
        'pt': 'Indicador de urgência, cálculo da lâmina de água recomendada e dias ideais para regar.',
        'changana': 'Xikombiso xa xilaveko, mpimo wa mati lama lavekaka ni masiku lamanene ya kucheleta.',
        'ronga': 'Xikombiso xa xilaveko, mpimo wa mati lama lavekaka ni masiku lamanene ya kucheleta.',
        'makhuwa': 'Ethoonyeryo ya othowa, mwaattelo wa maasi onireerela ni mahiku ooloka ohela maasi.',
        'sena': 'Cidziwiso ca kufunika, mpimo wa madzi anafunika na ntsiku zadidi zakuthirira.',
    },
    'feat3_titulo': {
        'pt': 'Análise de Dados',
        'changana': 'Kuxopaxopa ka Mahungu',
        'ronga': 'Kuxopaxopa ka Mahungu',
        'makhuwa': 'Otokosa Ihapari',
        'sena': 'Kudinga Mphangwa',
    },
    'feat3_desc': {
        'pt': 'Gráficos interactivos da evolução térmica de 48 horas, humidade do solo e evapotranspiração.',
        'changana': 'Swifaniso swa ku cinca ka kuhisa hi tiawara ta 48, kutswaka ka misava ni kupfumaleka ka mati.',
        'ronga': 'Swifaniso swa ku cinca ka kuhisa hi tiawara ta 48, kutswaka ka misava ni kupfumaleka ka mati.',
        'makhuwa': 'Igrafiko sa oviha wa epheyo wa iwoora 48, maasi a vathi ni ovukula wa maasi.',
        'sena': 'Magrafiko a kupisa kwa maora 48, kubvumbwa kwa mataka na kupwa kwa madzi.',
    },
    'feat4_titulo': {
        'pt': 'Controlo de Actividades',
        'changana': 'Vulawuri bya Mintirho',
        'ronga': 'Vulawuri bya Mintirho',
        'makhuwa': 'Oweha Miteko',
        'sena': 'Kuyang\'anira Mabasa',
    },
    'feat4_desc': {
        'pt': 'Registo da hora de início e fim das tarefas na machamba e verificação do cumprimento das regas.',
        'changana': 'Kutsala nkarhi wa kusungula ni wa kuheta mintirho ensin\'wini ni kuhlola kucheleta.',
        'ronga': 'Kutsala nkarhi wa kusungula ni wa kuheta mintirho a nsin\'wini ni kuhlola kucheleta.',
        'makhuwa': 'Olepa ewoora yoopacerya ni yoomaliha miteko mmatta ni oweha akhala wiira maasi aaheliwa.',
        'sena': 'Kulemba ndzidzi wakutoma na wakumalisa mabasa m\'munda na kuona khala kuthirira kwacitwa.',
    },
    'sec_fluxo': {
        'pt': 'Fluxo de Trabalho',
        'changana': 'Ndlela ya Kutirha',
        'ronga': 'Ndlela ya Kutirha',
        'makhuwa': 'Mweettelo wa Muteko',
        'sena': 'Ndandanda ya Basa',
    },
    'step1_titulo': {
        'pt': '1. Cadastro do Agricultor',
        'changana': '1. Kutsarisa Murimi',
        'ronga': '1. Kutsarisa Murimi',
        'makhuwa': '1. Olepiha Namalima',
        'sena': '1. Kulembesa Mulimi',
    },
    'step1_desc': {
        'pt': 'Registe os seus dados, a província, a cultura principal e a área em hectares da sua machamba.',
        'changana': 'Tsarisa vito ra wena, xifundzha, swimilana leswi u rimaka ni vukulu bya nsimu ya wena.',
        'ronga': 'Tsarisa vito ra wena, xifundzha, swimilana leswi u rimaka ni vukulu bya nsimu ya wena.',
        'makhuwa': 'Mulepe nsina nanyu, eporovinsiya, mbewe munlima anyu ni wunnuwa wa ematta anyu.',
        'sena': 'Lembani dzina yanu, provinsiya, mbeu inalima imwe na ukulu wa munda wanu.',
    },
    'step2_titulo': {
        'pt': '2. Consulta do Painel',
        'changana': '2. Kulanguta Painel',
        'ronga': '2. Kulanguta Painel',
        'makhuwa': '2. Oweha Painel',
        'sena': '2. Kuyang\'ana Painel',
    },
    'step2_desc': {
        'pt': 'Verifique no painel de controlo a previsão para 5 dias e os dias ideais para realizar a irrigação.',
        'changana': 'Languta ka painel maxelo ya masiku ya 5 ni masiku lamanene ya kucheleta nsimu.',
        'ronga': 'Languta ka painel maxelo ya masiku ya 5 ni masiku lamanene ya kucheleta nsimu.',
        'makhuwa': 'Moone va painel ihapari sa mahiku 5 ni mahiku ooloka ohela maasi mmatta.',
        'sena': 'Onani pa painel cidziwiso ca ntsiku 5 na ntsiku zadidi zakuthirira munda.',
    },
    'step3_titulo': {
        'pt': '3. Registo de Execução',
        'changana': '3. Kutsala Mintirho',
        'ronga': '3. Kutsala Mintirho',
        'makhuwa': '3. Olepa Miteko',
        'sena': '3. Kulemba Mabasa',
    },
    'step3_desc': {
        'pt': 'Aponte as actividades realizadas com a respectiva hora e acompanhe o histórico de cumprimento.',
        'changana': 'Tsala mintirho leyi u yi endleke ni nkarhi wa kona u landzelela matimu ya mintirho.',
        'ronga': 'Tsala mintirho leyi u yi yendleke ni nkarhi wa kona u landzelela matimu ya mintirho.',
        'makhuwa': 'Mulepe miteko sothene mwarumeelale anyu ni ewoora aya nave muwehe mweettelo aya.',
        'sena': 'Lembani mabasa adacita imwe pabodzi na ndzidzi wace pontho onani mbiri ya mabasa.',
    },

    # ─── Autenticação (Login / Cadastro / Recuperação) ───
    'btn_voltar_inicio': {
        'pt': '← Voltar à Página Inicial',
        'changana': '← Tlhelela Kusunguleni',
        'ronga': '← Tlhelela Kusunguleni',
        'makhuwa': '← Otthikela Woopaceryani',
        'sena': '← Kubwerera Patsogolo',
    },
    'auth_titulo': {
        'pt': 'Acesso do Agricultor',
        'changana': 'Kunghena ka Murimi',
        'ronga': 'Kunghena ka Murimi',
        'makhuwa': 'Okela wa Namalima',
        'sena': 'Kupita kwa Mulimi',
    },
    'auth_subtitulo': {
        'pt': 'Entre na sua conta, cadastre a sua machamba ou recupere a sua senha',
        'changana': 'Nghena ka akhawunti ya wena, tsarisa nsimu kumbe pfuxeta xihundla xa wena',
        'ronga': 'Nghena ka akhawunti ya wena, tsarisa nsimu kumbe pfuxeta xihundla xa wena',
        'makhuwa': 'Mukele mu akhawunti, mulepihe ematta anyu wala mutthikihe esenhya anyu',
        'sena': 'Pitani mu akhawunti yanu, lembesani munda wanu peno bwezerani senhya yanu',
    },
    'tab_recuperar': {
        'pt': 'Recuperar Senha',
        'changana': 'Pfuxeta Xihundla',
        'ronga': 'Pfuxeta Xihundla',
        'makhuwa': 'Otthikiha Esenhya',
        'sena': 'Kubwezera Senhya',
    },
    'lbl_telefone': {
        'pt': 'Telefone',
        'changana': 'qingho / Telefone',
        'ronga': 'Runqingho / Telefone',
        'makhuwa': 'Etelefone',
        'sena': 'Telefone',
    },
    'help_telefone_login': {
        'pt': 'Número de telefone usado no cadastro',
        'changana': 'Nomboro ya telefone leyi tirhisiweke loko u tsarisa',
        'ronga': 'Nomboro ya telefone leyi tirhisiweke loko u tsarisa',
        'makhuwa': 'Enumero ya etelefone yorumeeliwa okathi woolepiha',
        'sena': 'Numero ya telefone idaphatisirwa pakulembesa',
    },
    'lbl_senha': {
        'pt': 'Senha',
        'changana': 'Xihundla (Senha)',
        'ronga': 'Xihundla (Senha)',
        'makhuwa': 'Esenhya',
        'sena': 'Senhya',
    },
    'ph_senha': {
        'pt': 'Introduza a sua senha',
        'changana': 'Nghenisa xihundla xa wena',
        'ronga': 'Nghenisa xihundla xa wena',
        'makhuwa': 'Muhele esenhya anyu',
        'sena': 'ikani senhya yanu',
    },
    'btn_entrar': {
        'pt': 'Entrar',
        'changana': 'Nghena',
        'ronga': 'Nghena',
        'makhuwa': 'Okela',
        'sena': 'Kupita',
    },
    'err_login_vazio': {
        'pt': 'Preencha o número de telefone e a senha.',
        'changana': 'Tatisa nomboro ya telefone ni xihundla.',
        'ronga': 'Tatisa nomboro ya telefone ni xihundla.',
        'makhuwa': 'Muhele enumero ya etelefone ni esenhya.',
        'sena': 'Lembani numero ya telefone na senhya.',
    },
    'err_login_invalido': {
        'pt': "Telefone ou senha incorrectos. Caso tenha esquecido a senha, utilize a aba 'Recuperar Senha'.",
        'changana': "Telefone kumbe xihundla a swi lulamanga. Loko u rivale xihundla, tirhisa 'Pfuxeta Xihundla'.",
        'ronga': "Telefone kumbe xihundla a swi lulamanga. Loko u rivale xihundla, tirhisa 'Pfuxeta Xihundla'.",
        'makhuwa': "Etelefone wala esenhya khahiyo yoophwanelela. Mwalyala, murumeele 'Otthikiha Esenhya'.",
        'sena': "Telefone peno senhya si yene tayi. Khala mwaiwala, phatisirani 'Kubwezera Senhya'.",
    },
    'lbl_nome_completo': {
        'pt': 'Nome Completo *',
        'changana': 'Vito Hinkwaro *',
        'ronga': 'Vito Hinkwaro *',
        'makhuwa': 'Nsina Noomalela *',
        'sena': 'Dzina Yonsene *',
    },
    'ph_nome_completo': {
        'pt': 'O seu nome completo',
        'changana': 'Vito ra wena hinkwaro',
        'ronga': 'Vito ra wena hinkwaro',
        'makhuwa': 'Nsina nanyu noomalela',
        'sena': 'Dzina yanu yonsene',
    },
    'lbl_nome_machamba': {
        'pt': 'Nome da Machamba / Plantação *',
        'changana': 'Vito ra Nsimu / Machamba *',
        'ronga': 'Vito ra Nsimu / Machamba *',
        'makhuwa': 'Nsina na Ematta *',
        'sena': 'Dzina ya Munda / Machamba *',
    },
    'ph_nome_machamba': {
        'pt': 'Ex: Machamba Boa Colheita',
        'changana': 'Xikombiso: Nsimu ya Ntshovelo Lowunene',
        'ronga': 'Xikombiso: Nsimu ya Ntshovelo Lowunene',
        'makhuwa': 'Nthoo.: Ematta yootthuna',
        'sena': 'Citsandzo: Munda wa Kukolola Kwambiri',
    },
    'lbl_provincia': {
        'pt': 'Província *',
        'changana': 'Xifundzha (Província) *',
        'ronga': 'Xifundzha (Província) *',
        'makhuwa': 'Eporovinsiya *',
        'sena': 'Provinsiya *',
    },
    'lbl_distrito': {
        'pt': 'Distrito',
        'changana': 'Xifundzhantsongo (Distrito)',
        'ronga': 'Xifundzhantsongo (Distrito)',
        'makhuwa': 'Edistrito',
        'sena': 'Distrito',
    },
    'lbl_telefone_obrig': {
        'pt': 'Telefone *',
        'changana': 'Telefone *',
        'ronga': 'Telefone *',
        'makhuwa': 'Etelefone *',
        'sena': 'Telefone *',
    },
    'lbl_email_opc': {
        'pt': 'Email (opcional)',
        'changana': 'Email (a swi bohi)',
        'ronga': 'Email (a swi bohi)',
        'makhuwa': 'Email (khahiyo yoolaka)',
        'sena': 'Email (khala muli nayo)',
    },
    'lbl_senha_min': {
        'pt': 'Senha * (mínimo 6 caracteres)',
        'changana': 'Xihundla * (kusukela ka 6 wa maletere)',
        'ronga': 'Xihundla * (kusukela ka 6 wa maletere)',
        'makhuwa': 'Esenhya * (iletera 6 wala opwaha)',
        'sena': 'Senhya * (maletera 6 peno kupiringana)',
    },
    'lbl_confirmar_senha': {
        'pt': 'Confirmar Senha *',
        'changana': 'Tiyisisa Xihundla *',
        'ronga': 'Tiyisisa Xihundla *',
        'makhuwa': 'Olipiha Esenhya *',
        'sena': 'Kutsimikiza Senhya *',
    },
    'sec_dados_agronomicos': {
        'pt': '**Dados Agronómicos da Machamba**',
        'changana': '**Mahungu ya Vurimi bya Nsimu**',
        'ronga': '**Mahungu ya Vurimi bya Nsimu**',
        'makhuwa': '**Ihapari sa Olima wa Ematta**',
        'sena': '**Mphangwa za Ulimi wa Munda**',
    },
    'lbl_cultura_principal': {
        'pt': 'Cultura Principal',
        'changana': 'Ximilana Lexikulu',
        'ronga': 'Ximilana Lexikulu',
        'makhuwa': 'Mbewe Yuulupale',
        'sena': 'Mbeu Ikulu',
    },
    'lbl_area_ha': {
        'pt': 'Área (hectares)',
        'changana': 'Vukulu bya Nsimu (hectares)',
        'ronga': 'Vukulu bya Nsimu (hectares)',
        'makhuwa': 'Wunnuwa wa Ematta (hectares)',
        'sena': 'Ukulu wa Munda (hectares)',
    },
    'btn_concluir_cadastro': {
        'pt': 'Concluir Cadastro',
        'changana': 'Hetisa Kutsarisa',
        'ronga': 'Hetisa Kutsarisa',
        'makhuwa': 'Omaliha Olepiha',
        'sena': 'Kumalisa Kulembesa',
    },
    'err_nome_curto': {
        'pt': 'Nome completo é obrigatório (mínimo 3 caracteres).',
        'changana': 'Vito hinkwaro ra laveka (kusukela ka 3 wa maletere).',
        'ronga': 'Vito hinkwaro ra laveka (kusukela ka 3 wa maletere).',
        'makhuwa': 'Nsina noomalela ninnireerela (iletera 3).',
        'sena': 'Dzina yonsene inafunika (maletera 3).',
    },
    'err_machamba_obrig': {
        'pt': 'Nome da machamba é obrigatório.',
        'changana': 'Vito ra nsimu ra laveka.',
        'ronga': 'Vito ra nsimu ra laveka.',
        'makhuwa': 'Nsina na ematta ninnireerela.',
        'sena': 'Dzina ya munda inafunika.',
    },
    'err_telefone_curto': {
        'pt': 'Telefone é obrigatório (mínimo 8 dígitos).',
        'changana': 'Nomboro ya telefone ya laveka (8 wa tinomboro).',
        'ronga': 'Nomboro ya telefone ya laveka (8 wa tinomboro).',
        'makhuwa': 'Etelefone ennireerela (inumero 8).',
        'sena': 'Telefone inafunika (manumero 8).',
    },
    'err_senha_curta': {
        'pt': 'A senha deve ter no mínimo 6 caracteres.',
        'changana': 'Xihundla xi fanele kuva ni 6 wa maletere kumbe kutlula.',
        'ronga': 'Xihundla xi fanele kuva ni 6 wa maletere kumbe kutlula.',
        'makhuwa': 'Esenhya erina okhala ni iletera 6.',
        'sena': 'Senhya isafunika kukhala na maletera 6.',
    },
    'err_senhas_diferentes': {
        'pt': 'As senhas não coincidem.',
        'changana': 'Swihundla a swiringani.',
        'ronga': 'Swihundla a swiringani.',
        'makhuwa': 'Isenhya khasinlikana.',
        'sena': 'Masenhya khadalandana tayi.',
    },
    'msg_conta_criada': {
        'pt': "Conta criada com sucesso! Aceda à aba 'Entrar na Conta' para iniciar sessão.",
        'changana': "Akhawunti yi tumbuluxiwe kahle! Nghena ka 'Nghena ka Akhawunti'.",
        'ronga': "Akhawunti yi tumbuluxiwe kahle! Nghena ka 'Nghena ka Akhawunti'.",
        'makhuwa': "Akhawunti yoopattuxiwa saana! Mukele va 'Okela mu Akhawunti'.",
        'sena': "Akhawunti yakonzedwa mwadidi! Pitani pa 'Kupita mu Akhawunti'.",
    },
    'rec_instrucoes': {
        'pt': 'Informe o seu número de telefone e o nome da sua machamba registada para redefinir a senha.',
        'changana': 'Boxa nomboro ya telefone ni vito ra nsimu leyi u yi tsariseke leswaku u cinca xihundla.',
        'ronga': 'Boxa nomboro ya telefone ni vito ra nsimu leyi u yi tsariseke leswaku u cinca xihundla.',
        'makhuwa': 'Muhimye enumero ya etelefone ni nsina na ematta yoolempwa wiira mutthikihe esenhya.',
        'sena': 'Longani numero ya telefone na dzina ya munda wanu udalembeswa toera kucinja senhya.',
    },
    'lbl_tel_registado': {
        'pt': 'Telefone Registado *',
        'changana': 'Telefone Leyi Tsarisiweke *',
        'ronga': 'Telefone Leyi Tsarisiweke *',
        'makhuwa': 'Etelefone Yoolempwa *',
        'sena': 'Telefone Idalembeswa *',
    },
    'lbl_machamba_registada': {
        'pt': 'Nome da Machamba Registada *',
        'changana': 'Vito ra Nsimu Leyi Tsarisiweke *',
        'ronga': 'Vito ra Nsimu Leyi Tsarisiweke *',
        'makhuwa': 'Nsina na Ematta Yoolempwa *',
        'sena': 'Dzina ya Munda Udalembeswa *',
    },
    'lbl_nova_senha_min': {
        'pt': 'Nova Senha * (mínimo 6 caracteres)',
        'changana': 'Xihundla Lexintshwa * (6 wa maletere)',
        'ronga': 'Xihundla Lexintshwa * (6 wa maletere)',
        'makhuwa': 'Esenhya Esya * (iletera 6)',
        'sena': 'Senhya Ipswa * (maletera 6)',
    },
    'lbl_conf_nova_senha': {
        'pt': 'Confirmar Nova Senha *',
        'changana': 'Tiyisisa Xihundla Lexintshwa *',
        'ronga': 'Tiyisisa Xihundla Lexintshwa *',
        'makhuwa': 'Olipiha Esenhya Esya *',
        'sena': 'Kutsimikiza Senhya Ipswa *',
    },
    'btn_redefinir_senha': {
        'pt': 'Redefinir Senha',
        'changana': 'Cinca Xihundla',
        'ronga': 'Cinca Xihundla',
        'makhuwa': 'Orukunuxa Esenhya',
        'sena': 'Kucinja Senhya',
    },
    'err_rec_campos': {
        'pt': 'Preencha o número de telefone e o nome da machamba.',
        'changana': 'Tatisa nomboro ya telefone ni vito ra nsimu.',
        'ronga': 'Tatisa nomboro ya telefone ni vito ra nsimu.',
        'makhuwa': 'Muhele enumero ya etelefone ni nsina na ematta.',
        'sena': 'Lembani numero ya telefone na dzina ya munda.',
    },

    # ─── Dashboard ───
    'saudacao_dia': {
        'pt': 'Bom dia',
        'changana': 'Avuxeni',
        'ronga': 'Avuxeni',
        'makhuwa': 'Salama / Oxile',
        'sena': 'Mabuka bwanji',
    },
    'saudacao_tarde': {
        'pt': 'Boa tarde',
        'changana': 'Inhlikanhi',
        'ronga': 'Inhlikanhi',
        'makhuwa': 'Othana wooloka',
        'sena': 'Masikati adidi',
    },
    'saudacao_noite': {
        'pt': 'Boa noite',
        'changana': 'Riperile',
        'ronga': 'Riperile',
        'makhuwa': 'Ohiyu wooloka',
        'sena': 'Usiku wadidi',
    },
    'lbl_machamba': {
        'pt': 'Machamba',
        'changana': 'Nsimu',
        'ronga': 'Nsimu',
        'makhuwa': 'Ematta',
        'sena': 'Munda',
    },
    'lbl_cultura': {
        'pt': 'Cultura',
        'changana': 'Ximilana',
        'ronga': 'Ximilana',
        'makhuwa': 'Mbewe',
        'sena': 'Mbeu',
    },
    'lbl_area': {
        'pt': 'Área',
        'changana': 'Vukulu',
        'ronga': 'Vukulu',
        'makhuwa': 'Wunnuwa',
        'sena': 'Ukulu',
    },
    'sel_localizacao_clima': {
        'pt': 'Localização para dados meteorológicos',
        'changana': 'Ndhawu ya mahungu ya maxelo',
        'ronga': 'Ndhawu ya mahungu ya maxelo',
        'makhuwa': 'Nipuro na ihapari sa epula ni epheyo',
        'sena': 'Mbuto ya mphangwa za nyengo',
    },
    'btn_actualizar_dados': {
        'pt': 'Actualizar Dados',
        'changana': 'Pfuxeta Mahungu',
        'ronga': 'Pfuxeta Mahungu',
        'makhuwa': 'Ovinyererya Ihapari',
        'sena': 'Kusasanyira Mphangwa',
    },
    'spinner_clima': {
        'pt': 'A obter dados meteorológicos para {cidade}...',
        'changana': 'Kukumeka mahungu ya maxelo ya {cidade}...',
        'ronga': 'Kukumeka mahungu ya maxelo ya {cidade}...',
        'makhuwa': 'Ophavela ihapari sa epheyo sa {cidade}...',
        'sena': 'Kusaka mphangwa za nyengo za {cidade}...',
    },
    'err_clima_internet': {
        'pt': 'Não foi possível obter dados meteorológicos. Verifique a sua ligação à Internet.',
        'changana': 'A swi kotekanga kukuma mahungu ya maxelo. Kambela Internet ya wena.',
        'ronga': 'A swi kotekanga kukuma mahungu ya maxelo. Kambela Internet ya wena.',
        'makhuwa': 'Khawaaniherye ophwanya ihapari sa epheyo. Moone Internet anyu.',
        'sena': 'Cimwana kugumana mphangwa za nyengo. Yang\'anani Internet yanu.',
    },
    'card_temp_actual': {
        'pt': 'Temperatura Actual',
        'changana': 'Kuhisa ka Sweswi',
        'ronga': 'Kuhisa ka Swoswi',
        'makhuwa': 'Oviha wa Vano',
        'sena': 'Kupisa kwa Cincino',
    },
    'card_sensacao': {
        'pt': 'Sensação',
        'changana': 'ermatitwelo',
        'ronga': 'Matitwelo',
        'makhuwa': ' Wiupuwela',
        'sena': 'Mabvekesero',
    },
    'card_humidade_ar': {
        'pt': 'Humidade do Ar',
        'changana': 'Kutswaka ka Moya',
        'ronga': 'Kutswaka ka Moya',
        'makhuwa': 'Maasi a Mwepeyo',
        'sena': 'Kubvumbwa kwa Mphepo',
    },
    'card_vento': {
        'pt': 'Vento',
        'changana': 'Moya',
        'ronga': 'Moya',
        'makhuwa': 'Epheyo',
        'sena': 'Mphepo',
    },
    'card_estado_irrigacao': {
        'pt': 'Estado de Irrigação',
        'changana': 'Xiyimo xa Kucheleta',
        'ronga': 'Xiyimo xa Kucheleta',
        'makhuwa': 'Mukhalelo wo Ohela Maasi',
        'sena': 'Makhaliro a Kuthirira',
    },
    'card_pontuacao': {
        'pt': 'Pontuação',
        'changana': 'Mpimo',
        'ronga': 'Mpimo',
        'makhuwa': 'Mpimo',
        'sena': 'Mpimo',
    },
    'card_irrigacoes_hoje': {
        'pt': 'Irrigações Hoje',
        'changana': 'Kucheleta Namuntlha',
        'ronga': 'Kucheleta Namuntlha',
        'makhuwa': 'Ohela Maasi Olelo',
        'sena': 'Kuthirira Lero',
    },
    'card_streak': {
        'pt': 'Streak: {streak} dia(s)',
        'changana': 'Masiku ya kulandzelelana: {streak}',
        'ronga': 'Masiku ya kulandzelelana: {streak}',
        'makhuwa': 'Mahiku oottharelana: {streak}',
        'sena': 'Ntsiku zakutowererana: {streak}',
    },
    'sec_recomendacao_irrigacao': {
        'pt': 'Recomendação de Irrigação',
        'changana': 'Xitsundzuxo xa Kucheleta',
        'ronga': 'Xitsundzuxo xa Kucheleta',
        'makhuwa': 'Miruku so Ohela Maasi',
        'sena': 'Upungu wa Kuthirira',
    },
    'detalhes_avaliacao': {
        'pt': '**Detalhes da Avaliação**',
        'changana': '** Vuxokoxoko bya Kambisiso**',
        'ronga': '**Vuxokoxoko bya Kambisiso**',
        'makhuwa': '**Itthu so Otokosa**',
        'sena': '**Mphangwa za Kudinga**',
    },
    'met_lamina': {
        'pt': 'Lâmina de Água Sugerida',
        'changana': 'Mpimo wa Mati lowu Pimanyisiwaka',
        'ronga': 'Mpimo wa Mati lowu Pimanyisiwaka',
        'makhuwa': 'Mwaattelo wa Maasi',
        'sena': 'Mpimo wa Madzi Unafunika',
    },
    'met_temperatura': {
        'pt': 'Temperatura',
        'changana': 'Kuhisa',
        'ronga': 'Kuhisa',
        'makhuwa': 'Oviha',
        'sena': 'Kupisa',
    },
    'met_precipitacao': {
        'pt': 'Precipitação',
        'changana': 'Mpfula',
        'ronga': 'Mpfula',
        'makhuwa': 'Epula',
        'sena': 'Bvula',
    },
    'met_horario_ideal': {
        'pt': 'Horário Ideal',
        'changana': 'Nkarhi Lowunene',
        'ronga': 'Nkarhi Lowunene',
        'makhuwa': 'Ewoora Yooloka',
        'sena': 'Ndzidzi Wadidi',
    },
    'met_et0': {
        'pt': 'ET0 (Evapotranspiração)',
        'changana': 'ET0 (Kupfumaleka ka Mati)',
        'ronga': 'ET0 (Kupfumaleka ka Mati)',
        'makhuwa': 'ET0 (Ovukula wa Maasi)',
        'sena': 'ET0 (Kupwa kwa Madzi)',
    },
    'met_prob_chuva': {
        'pt': 'Prob. Chuva Prevista',
        'changana': 'Kukoteka ka Mpfula',
        'ronga': 'Kukoteka ka Mpfula',
        'makhuwa': 'Owehererya Epula',
        'sena': ' Cidziwiso ca Bvula',
    },
    'info_volume_estimado': {
        'pt': 'Para os seus **{area:.1f} ha**, o volume total estimado é de **{litros:,.0f} litros** ({m3:.1f} m³).',
        'changana': ' eka **{area:.1f} ha** ya wena, mati hinkwawo lama lavekaka hi **{litros:,.0f} litros** ({m3:.1f} m³).',
        'ronga': 'Aka **{area:.1f} ha** ya wena, mati hinkwawo lama lavekaka hi **{litros:,.0f} litros** ({m3:.1f} m³).',
        'makhuwa': 'Wa **{area:.1f} ha** anyu, maasi oothene anireerela ti **{litros:,.0f} litros** ({m3:.1f} m³).',
        'sena': 'Kwa **{area:.1f} ha** yanu, madzi onsene anafunika ndi **{litros:,.0f} litros** ({m3:.1f} m³).',
    },
    'sec_previsao_5dias': {
        'pt': 'Previsão Meteorológica — Próximos 5 Dias',
        'changana': 'Xiyimo xa Maxelo — Masiku ya 5 Lama Taka',
        'ronga': 'Xiyimo xa Maxelo — Masiku ya 5 Lama Taka',
        'makhuwa': 'Ihapari sa Epula — Mahiku 5 Oohoolo',
        'sena': 'Mphangwa za Nyengo — Ntsiku 5 Zinafuna Kudza',
    },
    'sec_calendario_irrigacao': {
        'pt': 'Calendário de Irrigação',
        'changana': 'Khalendara ya Kucheleta',
        'ronga': 'Khalendara ya Kucheleta',
        'makhuwa': 'Ekalendariyo yo Ohela Maasi',
        'sena': 'Kalendari ya Kuthirira',
    },
    'col_data': {
        'pt': 'Data',
        'changana': 'Siku',
        'ronga': 'Siku',
        'makhuwa': 'Nihiku',
        'sena': 'Ntsiku',
    },
    'col_condicao': {
        'pt': 'Condição',
        'changana': 'Xiyimo',
        'ronga': 'Xiyimo',
        'makhuwa': 'Mukhalelo',
        'sena': 'Makhaliro',
    },
    'col_max': {
        'pt': 'Máx',
        'changana': 'Kuhisa Ngopfu',
        'ronga': 'Kuhisa Ngopfu',
        'makhuwa': 'Yuulupale',
        'sena': 'Kupisa',
    },
    'col_min': {
        'pt': 'Mín',
        'changana': 'Kutsongo',
        'ronga': 'Kutsongo',
        'makhuwa': 'Yaamukhaani',
        'sena': 'Kuthontola',
    },
    'col_chuva': {
        'pt': 'Chuva',
        'changana': 'Mpfula',
        'ronga': 'Mpfula',
        'makhuwa': 'Epula',
        'sena': 'Bvula',
    },
    'col_status': {
        'pt': 'Status',
        'changana': 'Xiyimo',
        'ronga': 'Xiyimo',
        'makhuwa': 'Mukhalelo',
        'sena': 'Makhaliro',
    },
    'col_recomendacao': {
        'pt': 'Recomendação',
        'changana': 'Xitsundzuxo',
        'ronga': 'Xitsundzuxo',
        'makhuwa': 'Miruku',
        'sena': 'Upungu',
    },
    'col_lamina': {
        'pt': 'Lâmina',
        'changana': 'Mpimo wa Mati',
        'ronga': 'Mpimo wa Mati',
        'makhuwa': 'Maasi',
        'sena': 'Madzi',
    },
    'col_observacoes': {
        'pt': 'Observações',
        'changana': 'Switsundzuxo',
        'ronga': 'Switsundzuxo',
        'makhuwa': ' masu',
        'sena': ' Mafokotozero',
    },
    'sec_graficos': {
        'pt': 'Gráficos de Análise',
        'changana': 'Swifaniso swa Kuxopaxopa',
        'ronga': 'Swifaniso swa Kuxopaxopa',
        'makhuwa': 'Igrafiko so Otokosa',
        'sena': 'Magrafiko a Kudinga',
    },
    'tab_temp_48h': {
        'pt': 'Temperatura (48h)',
        'changana': 'Kuhisa (48h)',
        'ronga': 'Kuhisa (48h)',
        'makhuwa': 'Oviha (48h)',
        'sena': 'Kupisa (48h)',
    },
    'tab_humidade_solo': {
        'pt': 'Humidade do Solo',
        'changana': 'Kutswaka ka Misava',
        'ronga': 'Kutswaka ka Misava',
        'makhuwa': 'Maasi a Vathi',
        'sena': 'Kubvumbwa kwa Mataka',
    },
    'graf_titulo_temp': {
        'pt': 'Previsão de Temperatura Horária',
        'changana': 'Kuhisa hi Tiawara',
        'ronga': 'Kuhisa hi Tiawara',
        'makhuwa': 'Oviha wa Khula Ewoora',
        'sena': 'Kupisa kwa Ndzidzi Wonsene',
    },
    'graf_limiar_30': {
        'pt': '30°C — Limiar de irrigação alta',
        'changana': '30°C — Xilaveko lexikulu xa kucheleta',
        'ronga': '30°C — Xilaveko lexikulu xa kucheleta',
        'makhuwa': '30°C — Othowa wuulupale wa maasi',
        'sena': '30°C — Kufunika kukulu kwa kuthirira',
    },
    'graf_eixo_hora': {
        'pt': 'Hora',
        'changana': 'Awara',
        'ronga': 'Awara',
        'makhuwa': 'Ewoora',
        'sena': 'Ndzidzi',
    },
    'graf_titulo_solo': {
        'pt': 'Humidade Volumétrica do Solo e Probabilidade de Chuva',
        'changana': 'Kutswaka ka Misava ni Kukoteka ka Mpfula',
        'ronga': 'Kutswaka ka Misava ni Kukoteka ka Mpfula',
        'makhuwa': 'Maasi a Vathi ni Owehererya Epula',
        'sena': 'Kubvumbwa kwa Mataka na Cidziwiso ca Bvula',
    },
    'sec_dicas': {
        'pt': 'Dicas Agronómicas',
        'changana': 'Switsundzuxo swa Vurimi',
        'ronga': 'Switsundzuxo swa Vurimi',
        'makhuwa': 'Miruku sa Olima',
        'sena': 'Upungu wa Ulimi',
    },
    'rodape_actualizado': {
        'pt': 'Dados actualizados em {data} · Localização: {cidade} ({lat}, {lon})',
        'changana': 'Mahungu ma pfuxetiwile hi {data} · Ndhawu: {cidade} ({lat}, {lon})',
        'ronga': 'Mahungu ma pfuxetiwile hi {data} · Ndhawu: {cidade} ({lat}, {lon})',
        'makhuwa': 'Ihapari soovinyererihiwa {data} · Nipuro: {cidade} ({lat}, {lon})',
        'sena': 'Mphangwa zasasanyirwa pa {data} · Mbuto: {cidade} ({lat}, {lon})',
    },

    # ─── Página de Actividades ───
    'act_titulo': {
        'pt': 'Gestão de Actividades Agrícolas',
        'changana': 'Vulawuri bya Mintirho ya Vurimi',
        'ronga': 'Vulawuri bya Mintirho ya Vurimi',
        'makhuwa': 'Oweha Miteko sa Olima',
        'sena': 'Kuyang\'anira Mabasa a Ulimi',
    },
    'act_subtitulo': {
        'pt': 'Registo e controlo de tarefas do campo',
        'changana': 'Kutsala ni kulangutisa mintirho ya le nsin\'wini',
        'ronga': 'Kutsala ni kulangutisa mintirho ya le nsin\'wini',
        'makhuwa': 'Olepa ni oweha miteko sa mmatta',
        'sena': 'Kulemba na kuyang\'anira mabasa a m\'munda',
    },
    'card_act_hoje': {
        'pt': 'Actividades Hoje',
        'changana': 'Mintirho Namuntlha',
        'ronga': 'Mintirho Namuntlha',
        'makhuwa': 'Miteko Olelo',
        'sena': 'Mabasa Lero',
    },
    'card_horas_trab': {
        'pt': 'Horas Trabalhadas',
        'changana': 'Tiawara leti Tirhiweke',
        'ronga': 'Tiawara leti Tirhiweke',
        'makhuwa': 'Iwoora Soorumeeliwa',
        'sena': 'Maora Adaphatwa Basa',
    },
    'card_pendentes': {
        'pt': 'Pendentes',
        'changana': 'Leswi Saleke',
        'ronga': 'Leswi Saleke',
        'makhuwa': 'Sohimala',
        'sena': 'Pidakhala',
    },
    'card_dias_consecutivos': {
        'pt': 'Dias Consecutivos',
        'changana': 'Masiku ya Kulandzelelana',
        'ronga': 'Masiku ya Kulandzelelana',
        'makhuwa': 'Mahiku Oottharelana',
        'sena': 'Ntsiku Zakutowererana',
    },
    'cumprimento_ok': {
        'pt': '<strong>Irrigação realizada hoje!</strong> Já registou {n} irrigação(ões). Água total utilizada: <strong>{agua:,.0f} litros</strong> no acumulado.',
        'changana': '<strong>Kucheleta ku endliwile namuntlha!</strong> U tsarise {n} wa kucheleta. Mati hinkwawo lama tirhisiweke: <strong>{agua:,.0f} litros</strong>.',
        'ronga': '<strong>Kucheleta ku yendliwile namuntlha!</strong> U tsarise {n} wa kucheleta. Mati hinkwawo lama tirhisiweke: <strong>{agua:,.0f} litros</strong>.',
        'makhuwa': '<strong>Maasi aaheliwa olelo!</strong> Moolepa {n} ohela maasi. Maasi oothene: <strong>{agua:,.0f} litros</strong>.',
        'sena': '<strong>Kuthirira kwacitwa lero!</strong> Mwalemba {n} kuthirira. Madzi onsene adaphatisirwa: <strong>{agua:,.0f} litros</strong>.',
    },
    'cumprimento_alerta': {
        'pt': '<strong>Ainda não registou irrigação hoje.</strong> Verifique a recomendação no Dashboard e registe a actividade quando irrigar.',
        'changana': '<strong>A wu se tsala kucheleta namuntlha.</strong> Languta xitsundzuxo ka Painel u tlhela u tsala loko u cheleta.',
        'ronga': '<strong>A wu se tsala kucheleta namuntlha.</strong> Languta xitsundzuxo ka Painel u tlhela u tsala loko u cheleta.',
        'makhuwa': '<strong>Nlelo khamulenpe ohela maasi olelo.</strong> Moone miruku va Painel ni mulepe okathi munahela anyu maasi.',
        'sena': '<strong>Mudzati kulemba kuthirira lero tayi.</strong> Onani upungu pa Painel pontho lembani basa mukathirira.',
    },
    'sec_registar_act': {
        'pt': 'Registar Nova Actividade',
        'changana': 'Tsala Ntirho Lowuntshwa',
        'ronga': 'Tsala Ntirho Lowuntshwa',
        'makhuwa': 'Olepa Muteko Musya',
        'sena': 'Kulemba Basa Ipswa',
    },
    'lbl_tipo_act': {
        'pt': 'Tipo de Actividade *',
        'changana': 'Muxaka wa Ntirho *',
        'ronga': 'Muxaka wa Ntirho *',
        'makhuwa': 'Mukhalelo wa Muteko *',
        'sena': 'Mtundu wa Basa *',
    },
    'lbl_data_obrig': {
        'pt': 'Data *',
        'changana': 'Siku *',
        'ronga': 'Siku *',
        'makhuwa': 'Nihiku *',
        'sena': 'Ntsiku *',
    },
    'lbl_parcela': {
        'pt': 'Parcela / Talhão',
        'changana': 'Xiphemu xa Nsimu (Talhão)',
        'ronga': 'Xiphemu xa Nsimu (Talhão)',
        'makhuwa': 'Mpantta wa Ematta',
        'sena': 'Khundu ya Munda',
    },
    'ph_parcela': {
        'pt': 'Ex: Talhão 1 - Milho',
        'changana': 'Xik.: Xiphemu 1 - Xifake',
        'ronga': 'Xik.: Xiphemu 1 - Xifake',
        'makhuwa': 'Nthoo.: Mpantta 1 - Naakhuwo',
        'sena': 'Cits.: Khundu 1 - Mapira/Cimanga',
    },
    'lbl_hora_inicio': {
        'pt': 'Hora de Início',
        'changana': 'Awara ya Kusungula',
        'ronga': 'Awara ya Kusungula',
        'makhuwa': 'Ewoora Yoopacerya',
        'sena': 'Ndzidzi Wakutoma',
    },
    'lbl_hora_fim': {
        'pt': 'Hora de Fim',
        'changana': 'Awara ya Kuheta',
        'ronga': 'Awara ya Kuheta',
        'makhuwa': 'Ewoora Yoomaliha',
        'sena': 'Ndzidzi Wakumalisa',
    },
    'lbl_qtd_agua': {
        'pt': 'Quantidade de Água (litros)',
        'changana': 'Mpimo wa Mati (litros)',
        'ronga': 'Mpimo wa Mati (litros)',
        'makhuwa': 'Mwaattelo wa Maasi (litros)',
        'sena': 'Mpimo wa Madzi (litros)',
    },
    'help_qtd_agua': {
        'pt': 'Preencher apenas se for irrigação',
        'changana': 'Tatisa ntsena loko u cheleta',
        'ronga': 'Tatisa ntsena loko u cheleta',
        'makhuwa': 'Muhele paahi akhala ohela maasi',
        'sena': 'Lembani basi khala ndi kuthirira',
    },
    'ph_observacoes': {
        'pt': 'Notas sobre a actividade, condições do solo, etc.',
        'changana': 'Mahungu ya ntirho, xiyimo xa misava, ni swin\'wana.',
        'ronga': 'Mahungu ya ntirho, xiyimo xa misava, ni swin\'wana.',
        'makhuwa': 'Masu a muteko, mukhalelo wa etthaya, n.k.',
        'sena': 'Mafokotozero a basa, makhaliro a mataka, n.k.',
    },
    'btn_registar_act': {
        'pt': 'Registar Actividade',
        'changana': 'Tsala Ntirho',
        'ronga': 'Tsala Ntirho',
        'makhuwa': 'Olepa Muteko',
        'sena': 'Kulemba Basa',
    },
    'sec_historico_act': {
        'pt': 'Histórico de Actividades',
        'changana': 'Matimu ya Mintirho',
        'ronga': 'Matimu ya Mintirho',
        'makhuwa': 'Mweettelo wa Miteko',
        'sena': 'Mbiri ya Mabasa',
    },
    'lbl_filtrar_tipo': {
        'pt': 'Filtrar por tipo',
        'changana': 'Hlawula hi muxaka',
        'ronga': 'Hlawula hi muxaka',
        'makhuwa': 'Othanla mukhalelo',
        'sena': 'Kusankhula mtundu',
    },
    'lbl_filtrar_estado': {
        'pt': 'Filtrar por estado',
        'changana': 'Hlawula hi xiyimo',
        'ronga': 'Hlawula hi xiyimo',
        'makhuwa': 'Othanla mweettelo',
        'sena': 'Kusankhula makhaliro',
    },
    'lbl_de': {
        'pt': 'De',
        'changana': 'Kusukela',
        'ronga': 'Kusukela',
        'makhuwa': 'Okhuma',
        'sena': 'Kutoma',
    },
    'lbl_ate': {
        'pt': 'Até',
        'changana': 'Kufikela',
        'ronga': 'Kufikela',
        'makhuwa': 'Mpaka',
        'sena': 'Mpaka',
    },
    'msg_act_encontradas': {
        'pt': '**{n}** actividades encontradas no período seleccionado.',
        'changana': '**{n}** wa mintirho leyi kumekeke.',
        'ronga': '**{n}** wa mintirho leyi kumekeke.',
        'makhuwa': 'Miteko **{n}** soophwanyiwa.',
        'sena': 'Mabasa **{n}** agumanika.',
    },
    'btn_exportar_csv': {
        'pt': 'Exportar CSV',
        'changana': 'Humexa CSV',
        'ronga': 'Humexa CSV',
        'makhuwa': 'Okhumiha CSV',
        'sena': 'Kubulusa CSV',
    },
    'sec_gerir_act': {
        'pt': 'Gerir Actividades',
        'changana': 'Lawula Mintirho',
        'ronga': 'Lawula Mintirho',
        'makhuwa': 'Oweha Miteko',
        'sena': 'Kuyang\'anira Mabasa',
    },
    'btn_marcar_concluida': {
        'pt': 'Marcar Concluída',
        'changana': 'Fungha leswaku wu Herile',
        'ronga': 'Fungha leswaku wu Herile',
        'makhuwa': 'Ohela Yoomala',
        'sena': 'Kuika Yamala',
    },
    'btn_marcar_pendente': {
        'pt': 'Marcar Pendente',
        'changana': 'Fungha leswaku wa ha Sala',
        'ronga': 'Fungha leswaku wa ha Sala',
        'makhuwa': 'Ohela Yohimala',
        'sena': 'Kuika Idakhala',
    },
    'btn_apagar': {
        'pt': 'Apagar',
        'changana': 'Sula',
        'ronga': 'Sula',
        'makhuwa': 'Ofuta',
        'sena': 'Kufudza',
    },
    'msg_act_removida': {
        'pt': 'Actividade removida.',
        'changana': 'Ntirho wu suriwile.',
        'ronga': 'Ntirho wu suriwile.',
        'makhuwa': 'Muteko woofutiwa.',
        'sena': 'Basa yafudzwa.',
    },
    'info_sem_act': {
        'pt': 'Nenhuma actividade encontrada para os filtros seleccionados.',
        'changana': 'A ku kumekanga mintirho.',
        'ronga': 'A ku kumekanga mintirho.',
        'makhuwa': 'Khivo muteko oophwanyiwa.',
        'sena': 'Nkhabe basa idagumanika.',
    },
    'sec_resumo_semanal': {
        'pt': 'Resumo Semanal',
        'changana': 'Nkatsakanyo wa Vhiki',
        'ronga': 'Nkatsakanyo wa Vhiki',
        'makhuwa': 'Mweettelo wa Esumana',
        'sena': 'Cidziwiso ca Sumana',
    },
    'sem_cumprido': {
        'pt': 'Cumprido',
        'changana': 'Ku Endliwile',
        'ronga': 'Ku Yendliwile',
        'makhuwa': 'Yoorumeeliwa',
        'sena': 'Kwacitwa',
    },
    'sem_nao_registado': {
        'pt': 'Não registado',
        'changana': 'A swi tsariwanga',
        'ronga': 'A swi tsariwanga',
        'makhuwa': 'Khayoolempwa',
        'sena': 'Sikudalembwa tayi',
    },

    # ─── Perfil ───
    'perfil_registado_em': {
        'pt': 'Registado em',
        'changana': 'Tsarisiwile hi',
        'ronga': 'Tsarisiwile hi',
        'makhuwa': 'Yoolempwa nihiku',
        'sena': 'Adalembeswa pa',
    },
    'stat_area_machamba': {
        'pt': 'Área da Machamba',
        'changana': 'Vukulu bya Nsimu',
        'ronga': 'Vukulu bya Nsimu',
        'makhuwa': 'Wunnuwa wa Ematta',
        'sena': 'Ukulu wa Munda',
    },
    'stat_agua_total': {
        'pt': 'Água Total Registada',
        'changana': 'Mati Hinkwawo Lama Tirhisiweke',
        'ronga': 'Mati Hinkwawo Lama Tirhisiweke',
        'makhuwa': 'Maasi Oothene Oolempwa',
        'sena': 'Madzi Onsene Adalembwa',
    },
    'sec_editar_dados': {
        'pt': 'Editar Dados',
        'changana': 'Lulamisa Mahungu',
        'ronga': 'Lulamisa Mahungu',
        'makhuwa': 'Olokiherya Ihapari',
        'sena': 'Kusasanyira Mphangwa',
    },
    'help_tel_bloqueado': {
        'pt': 'O telefone não pode ser alterado (é usado para login)',
        'changana': 'Nomboro ya telefone a yi cinciwi (yi tirhisiwa kunghena)',
        'ronga': 'Nomboro ya telefone a yi cinciwi (yi tirhisiwa kunghena)',
        'makhuwa': 'Etelefone khenrukunuxiwa (enirumeeliwa okela)',
        'sena': 'Telefone nkhabe kucinjwa (isaphatisirwa pakupita)',
    },
    'sec_alterar_senha': {
        'pt': '**Alterar Senha** (deixe em branco para manter a actual)',
        'changana': '**Cinca Xihundla** (tshika swi nga tsariwanga loko u nga lavi kucinca)',
        'ronga': '**Cinca Xihundla** (tshika swi nga tsariwanga loko u nga lavi kucinca)',
        'makhuwa': '**Orukunuxa Esenhya** (muhiye voothowa akhala wiira khamuniphavela)',
        'sena': '**Kucinja Senhya** (siyani mwakusowa cinthu khala nkhabe funa kucinja)',
    },
    'lbl_nova_senha': {
        'pt': 'Nova Senha',
        'changana': 'Xihundla Lexintshwa',
        'ronga': 'Xihundla Lexintshwa',
        'makhuwa': 'Esenhya Esya',
        'sena': 'Senhya Ipswa',
    },
    'lbl_confirmar_nova': {
        'pt': 'Confirmar Nova Senha',
        'changana': 'Tiyisisa Xihundla Lexintshwa',
        'ronga': 'Tiyisisa Xihundla Lexintshwa',
        'makhuwa': 'Olipiha Esenhya Esya',
        'sena': 'Kutsimikiza Senhya Ipswa',
    },
    'btn_guardar_alteracoes': {
        'pt': 'Guardar Alterações',
        'changana': 'Hlayisa Ku Cinca',
        'ronga': 'Hlayisa Ku Cinca',
        'makhuwa': 'Oweha Orukunuxa',
        'sena': 'Kukoya Macinjiro',
    },
    'msg_perfil_actualizado': {
        'pt': 'Perfil actualizado com sucesso!',
        'changana': 'Mahungu ma pfuxetiwile kahle!',
        'ronga': 'Mahungu ma pfuxetiwile kahle!',
        'makhuwa': 'Ihapari soolokiheriwa saana!',
        'sena': 'Mphangwa zasasanyirwa mwadidi!',
    },
    'err_perfil_actualizar': {
        'pt': 'Erro ao actualizar o perfil.',
        'changana': 'Xihoxo eka kupfuxeta mahungu.',
        'ronga': 'Xihoxo aka kupfuxeta mahungu.',
        'makhuwa': ' yookhala etthu yoovonya.',
        'sena': 'Kwacitika madodo pakusasanyira mphangwa.',
    },
    'btn_sair_conta': {
        'pt': 'Sair da Conta',
        'changana': 'Huma ka Akhawunti',
        'ronga': 'Huma ka Akhawunti',
        'makhuwa': 'Okhuma mu Akhawunti',
        'sena': 'Kubuluka mu Akhawunti',
    },

    # ─── Assistente IA ───
    'nav_assistente': {
        'pt': 'Assistente IA',
        'changana': 'Mupfuni wa IA',
        'ronga': 'Mupfuni wa IA',
        'makhuwa': 'Namakhaliherya IA',
        'sena': 'Mphedzi wa IA',
    },
    'ia_titulo': {
        'pt': 'Assistente IA — Sustentabilidade Agrónoma',
        'changana': 'Mupfuni wa IA — Vuhlayisi bya Vurimi',
        'ronga': 'Mupfuni wa IA — Vuhlayisi bya Vurimi',
        'makhuwa': 'Namakhaliherya IA — Okhapelela wa Olima',
        'sena': 'Mphedzi wa IA — Kukoya Ulimi',
    },
    'ia_subtitulo': {
        'pt': 'Tire dúvidas sobre o funcionamento do sistema, recomendações de irrigação, registo de actividades e culturas agrícolas.',
        'changana': 'Vutisa hi matirhelo ya xitirhisiwa, switsundzuxo swa kucheleta, kutsala mintirho ni vurimi.',
        'ronga': 'Vutisa hi matirhelo ya xitirhisiwa, switsundzuxo swa kucheleta, kutsala mintirho ni vurimi.',
        'makhuwa': 'Mukoha voohimya sa mweettelo wa esistema, miruku so ohela maasi, olepa miteko ni mbewe.',
        'sena': 'Bvundzisani thangwi ya maphatisiro a sistema, upungu wa kuthirira, kulemba mabasa na mbeu.',
    },
    'ia_boas_vindas': {
        'pt': (
            'Olá! Sou o **Assistente Inteligente da plataforma Sustentabilidade Agrónoma**. 🌱\n\n'
            'Posso responder às suas dúvidas sobre:\n'
            '- **Funcionamento do Sistema:** cadastro, login, recuperação de senha, perfil e troca de idioma.\n'
            '- **Painel de Irrigação:** como funciona o semáforo de rega, cálculo da lâmina de água (mm e litros), ET0 e previsão de 5 dias.\n'
            '- **Controlo de Actividades:** como registar tarefas, filtrar histórico, exportar CSV e acompanhar dias consecutivos (*streak*).\n'
            '- **A sua Machamba e Culturas:** dados actuais da sua conta e recomendações para milho, arroz, feijão, hortícolas, mandioca e cana-de-açúcar.\n\n'
            'Como posso ajudar hoje?'
        ),
        'changana': (
            'Avuxeni! Hi mina **Mupfuni wa IA wa Vuhlayisi bya Vurimi**. 🌱\n\n'
            'Ndzi nga ku pfuna hi:\n'
            '- **Matirhelo ya Sistema:** kutsarisa, kunghena, kupfuxeta xihundla ni kucinca lirimi.\n'
            '- **Painel ra Kucheleta:** matirhelo ya xikombiso xa kucheleta, mpimo wa mati (mm ni litros), ET0 ni maxelo ya masiku ya 5.\n'
            '- **Vulawuri bya Mintirho:** kutsala mintirho ya nsimu, kulanguta matimu ni ku humexa CSV.\n'
            '- **Nsimu ya Wena ni Swimilana:** xifake, mpunga, tinyawa, xumbula, matsavu ni movha.\n\n'
            'Ndzi nga ku pfuna hi yini namuntlha?'
        ),
        'ronga': (
            'Avuxeni! Hi mina **Mupfuni wa IA wa Vuhlayisi bya Vurimi**. 🌱\n\n'
            'Ndzi nga ku pfuna hi:\n'
            '- **Matirhelo ya Sistema:** kutsarisa, kunghena, kupfuxeta xihundla ni kucinca lirimi.\n'
            '- **Painel ra Kucheleta:** matirhelo ya xikombiso xa kucheleta, mpimo wa mati (mm ni litros), ET0 ni maxelo ya masiku ya 5.\n'
            '- **Vulawuri bya Mintirho:** kutsala mintirho ya nsimu, kulanguta matimu ni ku humexa CSV.\n'
            '- **Nsimu ya Wena ni Swimilana:** xifake, mpunga, tinyawa, xumbula, matsavu ni movha.\n\n'
            'Ndzi nga ku pfuna hi yini namuntlha?'
        ),
        'makhuwa': (
            'Salama! Miyo ka **Namakhaliherya IA wa Okhapelela wa Olima**. 🌱\n\n'
            'Kinoowerya waakhula makoho anyu voohimya sa:\n'
            '- **Mweettelo wa Sistema:** olepiha, okela, otthikiha esenhya ni orukunuxa nttaava.\n'
            '- **Painel yo Ohela Maasi:** ethoonyeryo yo ohela maasi, mwaattelo wa maasi (mm ni litros), ET0 ni ihapari sa mahiku 5.\n'
            '- **Oweha Miteko:** olepa miteko sa mmatta, oweha mweettelo ni okhumiha CSV.\n'
            '- **Ematta Anyu ni Mbewe:** naakhuwo, muka, ekutte, matakhwani, mathapa ni muhale.\n\n'
            'Kikhaliherye sai olelo?'
        ),
        'sena': (
            'Mabuka bwanji! Ine ndine **Mphedzi wa IA wa Kukoya Ulimi**. 🌱\n\n'
            'Ndinakwanisa kutawira mibvundzo yanu thangwi ya:\n'
            '- **Maphatisiro a Sistema:** kulembesa, kupita, kubwezera senhya na kucinja cilongero.\n'
            '- **Painel ya Kuthirira:** cidziwiso ca kuthirira, mpimo wa madzi (mm na litros), ET0 na nyengo ya ntsiku 5.\n'
            '- **Kuyang\'anira Mabasa:** kulemba mabasa a m\'munda, mbiri ya mabasa na kubulusa CSV.\n'
            '- **Munda Wanu na Mbeu:** cimanga, mpunga, nyemba, mbwani, masamba na muzimbe.\n\n'
            'Ndikuphedzeni tani lero?'
        ),
    },
    'ia_sugestoes_titulo': {
        'pt': 'Perguntas Frequentes (clique para perguntar):',
        'changana': 'Swivutiso leswi Tolovelekeke (tlilika ku vutisa):',
        'ronga': 'Swivutiso leswi Tolovelekeke (tlilika ku vutisa):',
        'makhuwa': 'Makoho Oolimaleliwa (muthanle wiira mukoha):',
        'sena': 'Mibvundzo Yakudzoloereka (dingani toera kubvundza):',
    },
    'ia_q1': {
        'pt': 'Como funciona o semáforo de irrigação?',
        'changana': 'Xi tirha njhani xikombiso xa kucheleta?',
        'ronga': 'Xi tirha njhani xikombiso xa kucheleta?',
        'makhuwa': 'Enirumeela sai ethoonyeryo yo ohela maasi?',
        'sena': 'Cisaphata tani basa cidziwiso ca kuthirira?',
    },
    'ia_q2': {
        'pt': 'Como é calculada a quantidade de água (lâmina)?',
        'changana': 'Wu pimisiwa njhani mpimo wa mati?',
        'ronga': 'Wu pimisiwa njhani mpimo wa mati?',
        'makhuwa': 'Onipimiwa sai mwaattelo wa maasi?',
        'sena': 'Usapimiwa tani mpimo wa madzi?',
    },
    'ia_q3': {
        'pt': 'Como registar e exportar actividades?',
        'changana': 'Ndzi tsala njhani mintirho ni ku humexa CSV?',
        'ronga': 'Ndzi tsala njhani mintirho ni ku humexa CSV?',
        'makhuwa': 'Kinlepa sai miteko ni okhumiha CSV?',
        'sena': 'Ndinalemba tani mabasa na kubulusa CSV?',
    },
    'ia_q4': {
        'pt': 'Como recuperar a senha ou mudar o idioma?',
        'changana': 'Ndzi pfuxeta njhani xihundla kumbe kucinca lirimi?',
        'ronga': 'Ndzi pfuxeta njhani xihundla kumbe kucinca lirimi?',
        'makhuwa': 'Kinrukunuxa sai esenhya wala nttaava?',
        'sena': 'Ndinacinja tani senhya peno cilongero?',
    },
    'ia_q5': {
        'pt': 'Qual é o resumo actual da minha machamba?',
        'changana': 'Hi xihi xiyimo xa nsimu ya mina sweswi?',
        'ronga': 'Hi xihi xiyimo xa nsimu ya mina swoswi?',
        'makhuwa': 'Exeeni mweettelo wa ematta aka vano?',
        'sena': 'Ndi cipi cidziwiso ca munda wanga cincino?',
    },
    'ia_input_placeholder': {
        'pt': 'Digite aqui a sua questão sobre o sistema, irrigação, clima ou culturas...',
        'changana': 'Tsala laha xivutiso xa wena hi sistema, kucheleta, maxelo kumbe swimilana...',
        'ronga': 'Tsala laha xivutiso xa wena hi sistema, kucheleta, maxelo kumbe swimilana...',
        'makhuwa': 'Mulepe va nikoho nanyu voohimya sa sistema, ohela maasi, epula wala mbewe...',
        'sena': 'Lembani pano m\'bvundzo wanu thangwi ya sistema, kuthirira, nyengo peno mbeu...',
    },
    'ia_lbl_caixa_prompt': {
        'pt': 'Caixa de Prompt — Coloque a sua questão ao Assistente IA:',
        'changana': 'Bokisi ra Xivutiso — Vutisa Mupfuni wa IA:',
        'ronga': 'Bokisi ra Xivutiso — Vutisa Mupfuni wa IA:',
        'makhuwa': 'Nipuro no Okoha — Mukoha Namakhaliherya IA:',
        'sena': 'Bokosi ya M\'bvundzo — Bvundzani Mphedzi wa IA:',
    },
    'ia_btn_enviar': {
        'pt': 'Enviar Questão ➤',
        'changana': 'Rhumela Xivutiso ➤',
        'ronga': 'Rhumela Xivutiso ➤',
        'makhuwa': 'Orumiha Nikoho ➤',
        'sena': 'kutumiza M\'bvundzo ➤',
    },
    'ia_btn_limpar': {
        'pt': 'Limpar Conversa',
        'changana': 'Sula Mabulo',
        'ronga': 'Sula Mabulo',
        'makhuwa': 'Ofuta Mwaha',
        'sena': 'Kufudza Makani',
    },
    'ia_expander_rapido': {
        'pt': '🤖 Assistente IA Interactivo — Coloque aqui as suas dúvidas sobre o sistema',
        'changana': '🤖 Mupfuni wa IA — Vutisa laha swivutiso swa wena hi sistema',
        'ronga': '🤖 Mupfuni wa IA — Vutisa laha swivutiso swa wena hi sistema',
        'makhuwa': '🤖 Namakhaliherya IA — Mukoha va makoho anyu voohimya sa sistema',
        'sena': '🤖 Mphedzi wa IA — Bvundzani pano mibvundzo yanu thangwi ya sistema',
    },
}

# ─── Traduções de Valores de Domínio (Culturas, Tipos de Actividade, Estados, Clima, Níveis) ───

CULTURAS_TRADUCAO = {
    'Milho': {'pt': 'Milho', 'changana': 'Xifake (Milho)', 'ronga': 'Xifake (Milho)', 'makhuwa': 'Naakhuwo (Milho)', 'sena': 'Cimanga (Milho)'},
    'Arroz': {'pt': 'Arroz', 'changana': 'Mpunga (Arroz)', 'ronga': 'Mpunga (Arroz)', 'makhuwa': 'Muka (Arroz)', 'sena': 'Mpunga (Arroz)'},
    'Feijão': {'pt': 'Feijão', 'changana': 'Tinyawa (Feijão)', 'ronga': 'Tinyawa (Feijão)', 'makhuwa': 'Ekutte (Feijão)', 'sena': 'Nyemba (Feijão)'},
    'Mandioca': {'pt': 'Mandioca', 'changana': 'Xumbula (Mandioca)', 'ronga': 'Xumbula (Mandioca)', 'makhuwa': 'Matakhwani (Mandioca)', 'sena': 'Farinya / Mbwani (Mandioca)'},
    'Hortícolas': {'pt': 'Hortícolas', 'changana': 'Matsavu (Hortícolas)', 'ronga': 'Matsavu (Hortícolas)', 'makhuwa': 'Mathapa (Hortícolas)', 'sena': 'Masamba (Hortícolas)'},
    'Fruteiras': {'pt': 'Fruteiras', 'changana': 'Mihandzu (Fruteiras)', 'ronga': 'Mihandzu (Fruteiras)', 'makhuwa': 'Mihokorokho (Fruteiras)', 'sena': 'Misapo (Fruteiras)'},
    'Cana-de-Açúcar': {'pt': 'Cana-de-Açúcar', 'changana': 'Movha (Cana-de-Açúcar)', 'ronga': 'Movha (Cana-de-Açúcar)', 'makhuwa': 'Muhale (Cana-de-Açúcar)', 'sena': 'Muzimbe (Cana-de-Açúcar)'},
    'Algodão': {'pt': 'Algodão', 'changana': 'Swifufunhukwani / Algodão', 'ronga': 'Algodão', 'makhuwa': 'Ntthonje (Algodão)', 'sena': 'Thonje (Algodão)'},
    'Tabaco': {'pt': 'Tabaco', 'changana': 'Fole (Tabaco)', 'ronga': 'Fole (Tabaco)', 'makhuwa': 'Soni (Tabaco)', 'sena': 'Fodya (Tabaco)'},
    'Amendoim': {'pt': 'Amendoim', 'changana': 'Timanga (Amendoim)', 'ronga': 'Timanga (Amendoim)', 'makhuwa': 'Mattuvi (Amendoim)', 'sena': 'Manduwi (Amendoim)'},
    'Soja': {'pt': 'Soja', 'changana': 'Soja', 'ronga': 'Soja', 'makhuwa': 'Soja', 'sena': 'Soja'},
    'Gergelim': {'pt': 'Gergelim', 'changana': 'Lihlula (Gergelim)', 'ronga': 'Lihlula (Gergelim)', 'makhuwa': 'Namuhakhu (Gergelim)', 'sena': 'Uchitowe (Gergelim)'},
    'Outros': {'pt': 'Outros', 'changana': "Swin'wana", 'ronga': "Swin'wana", 'makhuwa': 'Sikina', 'sena': 'Pinango'},
}

TIPOS_ACTIVIDADE_TRADUCAO = {
    'Todos': {'pt': 'Todos', 'changana': 'Hinkwaswo', 'ronga': 'Hinkwaswo', 'makhuwa': 'Soothene', 'sena': 'Pyonsene'},
    'Irrigação': {'pt': 'Irrigação', 'changana': 'Kucheleta (Irrigação)', 'ronga': 'Kucheleta (Irrigação)', 'makhuwa': 'Ohela Maasi (Irrigação)', 'sena': 'Kuthirira (Irrigação)'},
    'Adubação': {'pt': 'Adubação', 'changana': 'Kuchela Manyoro (Adubação)', 'ronga': 'Kuchela Manyoro (Adubação)', 'makhuwa': 'Ohela Manyoro (Adubação)', 'sena': 'Kuika Manyowa (Adubação)'},
    'Pulverização': {'pt': 'Pulverização', 'changana': 'Kufafazela Murhi (Pulverização)', 'ronga': 'Kufafazela Murhi (Pulverização)', 'makhuwa': 'Owaza Mirette (Pulverização)', 'sena': 'Kupopela Mankhwala (Pulverização)'},
    'Capina': {'pt': 'Capina', 'changana': 'Kuhlakula (Capina)', 'ronga': 'Kuhlakula (Capina)', 'makhuwa': 'Opalela (Capina)', 'sena': 'Kulima / Kupalira (Capina)'},
    'Sementeira': {'pt': 'Sementeira', 'changana': 'Kubyala (Sementeira)', 'ronga': 'Kubyala (Sementeira)', 'makhuwa': 'Waala (Sementeira)', 'sena': 'Kubzala (Sementeira)'},
    'Colheita': {'pt': 'Colheita', 'changana': 'Kutshovela (Colheita)', 'ronga': 'Kutshovela (Colheita)', 'makhuwa': 'Ohepha (Colheita)', 'sena': 'Kukolola (Colheita)'},
    'Poda': {'pt': 'Poda', 'changana': 'Kutsema Marhavi (Poda)', 'ronga': 'Kutsema Marhavi (Poda)', 'makhuwa': 'Ohakola (Poda)', 'sena': 'Kudula Nthambi (Poda)'},
    'Outros': {'pt': 'Outros', 'changana': "Swin'wana", 'ronga': "Swin'wana", 'makhuwa': 'Sikina', 'sena': 'Pinango'},
}

ESTADOS_TRADUCAO = {
    'Todos': {'pt': 'Todos', 'changana': 'Hinkwaswo', 'ronga': 'Hinkwaswo', 'makhuwa': 'Soothene', 'sena': 'Pyonsene'},
    'Concluída': {'pt': 'Concluída', 'changana': 'Wu Herile', 'ronga': 'Wu Herile', 'makhuwa': 'Yoomala', 'sena': 'Yamala'},
    'Pendente': {'pt': 'Pendente', 'changana': 'Wa ha Sala', 'ronga': 'Wa ha Sala', 'makhuwa': 'Yohimala', 'sena': 'Idakhala'},
}

DIAS_SEMANA_TRADUCAO = {
    'Monday': {'pt': 'Segunda', 'changana': 'Musumbhunuku', 'ronga': 'Musumbhunuku', 'makhuwa': ' Nihiku noopacerya', 'sena': 'Ciposi'},
    'Tuesday': {'pt': 'Terça', 'changana': 'Ravumbirhi', 'ronga': 'Ravumbirhi', 'makhuwa': 'Nihiku na nenli', 'sena': 'Cipiri'},
    'Wednesday': {'pt': 'Quarta', 'changana': 'Ravunharhu', 'ronga': 'Ravunharhu', 'makhuwa': 'Nihiku na neeraru', 'sena': 'Citatu'},
    'Thursday': {'pt': 'Quinta', 'changana': 'Ravumune', 'ronga': 'Ravumune', 'makhuwa': 'Nihiku na neexexe', 'sena': 'Cinai'},
    'Friday': {'pt': 'Sexta', 'changana': 'Ravuntlhanu', 'ronga': 'Ravuntlhanu', 'makhuwa': 'Nihiku na neethanu', 'sena': 'Cisano'},
    'Saturday': {'pt': 'Sábado', 'changana': 'Mugqivela', 'ronga': 'Mugqivela', 'makhuwa': 'Esabadu', 'sena': 'Sabudu'},
    'Sunday': {'pt': 'Domingo', 'changana': 'Sonto', 'ronga': 'Sonto', 'makhuwa': 'Etuminku', 'sena': 'Dimingu'},
}

NIVEIS_IRRIGACAO_TRADUCAO = {
    'URGENTE': {
        'pt': {
            'rotulo': 'URGENTE — Irrigar Imediatamente',
            'descricao': 'Condições críticas de calor e alta perda de água. Risco elevado de stress hídrico.',
        },
        'changana': {
            'rotulo': 'XIhatla — Cheleta Sweswi',
            'descricao': 'Kuhisa lokukulu ni kupfumaleka ka mati. Swimilana swi le khombyeni ra ku oma.',
        },
        'ronga': {
            'rotulo': 'XIHATLA — Cheleta Swoswi',
            'descricao': 'Kuhisa lokukulu ni kupfumaleka ka mati. Swimilana swi le khombyeni ra ku woma.',
        },
        'makhuwa': {
            'rotulo': 'MOWAAKUVEYA — Muhele Maasi Vano',
            'descricao': 'Oviha wuulupale ni othowa wa maasi. Ibewe siri va nritti noowuma.',
        },
        'sena': {
            'rotulo': 'MWAKUCIMBIZA — Thirirani Cincino',
            'descricao': 'Kupisa kukulu na kupwa kwa madzi. Mbeu ziri pa ngozi yakulenguka.',
        },
    },
    'ALTO': {
        'pt': {
            'rotulo': 'ALTO — Irrigar Hoje',
            'descricao': 'Temperaturas elevadas e solo a secar. Irrigar nas horas mais frescas.',
        },
        'changana': {
            'rotulo': 'HENHLA — Cheleta Namuntlha',
            'descricao': 'Kuhisa lokukulu naswona misava ya oma. Cheleta loko dyambu ri nga se hisa.',
        },
        'ronga': {
            'rotulo': 'HENHLA — Cheleta Namuntlha',
            'descricao': 'Kuhisa lokukulu naswona misava ya woma. Cheleta loko dambu ri nga se hisa.',
        },
        'makhuwa': {
            'rotulo': 'WUULUPALE — Muhele Maasi Olelo',
            'descricao': 'Oviha wuulupale ni etthaya enowuma. Muhele maasi vooxixelo wala makaaripi.',
        },
        'sena': {
            'rotulo': 'KUKULU — Thirirani Lero',
            'descricao': 'Kupisa kukulu na mataka akumira. Thirirani namacibese peno namasikati.',
        },
    },
    'MODERADO': {
        'pt': {
            'rotulo': 'MODERADO — Irrigar se Possível',
            'descricao': 'Clima ameno sem chuva prevista. Monitorar humidade do solo.',
        },
        'changana': {
            'rotulo': 'XIKARHI — Cheleta Loko Swi Koteka',
            'descricao': 'Maxelo ya kahle handle ka mpfula. Langutisa kutswaka ka misava.',
        },
        'ronga': {
            'rotulo': 'XIKARHI — Cheleta Loko Swi Koteka',
            'descricao': 'Maxelo ya kahle handle ka mpfula. Langutisa kutswaka ka misava.',
        },
        'makhuwa': {
            'rotulo': 'VA ERIYARI — Muhele Maasi Mwawerya',
            'descricao': 'Epheyo yooloka ohikhanle epula. Moone maasi a vathi.',
        },
        'sena': {
            'rotulo': 'PAKATI — Thirirani Khala Munakwanisa',
            'descricao': 'Nyengo yadidi cakusowa bvula. Yang\'anirani kubvumbwa kwa mataka.',
        },
    },
    'BAIXO': {
        'pt': {
            'rotulo': 'BAIXO — Não é Necessário Irrigar',
            'descricao': 'Chuva prevista ou temperaturas frescas. Poupança de água recomendada.',
        },
        'changana': {
            'rotulo': 'HANSI — A Swi Laveki Kucheleta',
            'descricao': 'Ku languteriwe mpfula kumbe ku titimela. Hlayisa mati.',
        },
        'ronga': {
            'rotulo': 'HANSI — A Swi Laveki Kucheleta',
            'descricao': 'Ku languteriwe mpfula kumbe ku titimela. Hlayisa mati.',
        },
        'makhuwa': {
            'rotulo': 'VAKHAANI — Khonireerela Ohela Maasi',
            'descricao': 'Epula enowehereriwa wala oriirya. Mukhapelele maasi.',
        },
        'sena': {
            'rotulo': 'PANTSI — Nkhabe Funika Kuthirira',
            'descricao': 'Bvula inafuna kubvumba peno kunathontola. Koyani madzi.',
        },
    },
    'DESNECESSARIO': {
        'pt': {
            'rotulo': 'DESNECESSÁRIO — Solo com Humidade Suficiente',
            'descricao': 'Solo húmido ou chuva recente abundante. Evitar encharcamento.',
        },
        'changana': {
            'rotulo': 'A SWI LAVEKI — Misava yi Tswakile',
            'descricao': 'Misava yi na mati yo ringanela kumbe kuve ni mpfula. Papalata ku tala ka mati.',
        },
        'ronga': {
            'rotulo': 'A SWI LAVEKI — Misava yi Tswakile',
            'descricao': 'Misava yi na mati yo ringanela kumbe kuve ni mpfula. Papalata ku tala ka mati.',
        },
        'makhuwa': {
            'rotulo': 'KHONIREERELA — Etthaya Erina Maasi Oophiyera',
            'descricao': 'Etthaya yoowetta wala epula yoopwa. Муhihele maasi oopwaha.',
        },
        'sena': {
            'rotulo': 'NKHABE FUNIKA — Mataka Ali na Madzi Akukwana',
            'descricao': 'Mataka abvumbwa peno bvula yabvumba cincino. Calirani kuzadza madzi.',
        },
    },
}

RECOMENDACOES_5DIAS_TRADUCAO = {
    'Não Irrigar': {
        'pt': 'Não Irrigar',
        'changana': 'U Nga Cheleti',
        'ronga': 'U Nga Cheleti',
        'makhuwa': 'Muhihele Maasi',
        'sena': 'Lekani Kuthirira',
    },
    'Irrigar (Urgente)': {
        'pt': 'Irrigar (Urgente)',
        'changana': 'Cheleta (Xihatla)',
        'ronga': 'Cheleta (Xihatla)',
        'makhuwa': 'Muhele Maasi (Mowaakuveya)',
        'sena': 'Thirirani (Mwakucimbiza)',
    },
    'Irrigar': {
        'pt': 'Irrigar',
        'changana': 'Cheleta',
        'ronga': 'Cheleta',
        'makhuwa': 'Muhele Maasi',
        'sena': 'Thirirani',
    },
    'Irrigar se Possível': {
        'pt': 'Irrigar se Possível',
        'changana': 'Cheleta loko swi koteka',
        'ronga': 'Cheleta loko swi koteka',
        'makhuwa': 'Muhele maasi mwawerya',
        'sena': 'Thirirani khala munakwanisa',
    },
    'Opcional': {
        'pt': 'Opcional',
        'changana': 'Ku Hlawula',
        'ronga': 'Ku Hlawula',
        'makhuwa': 'Yoothanla',
        'sena': 'Cisankhulo',
    },
}


def obter_idioma() -> str:
    """Retorna o código do idioma actual na sessão ('pt' por omissão)."""
    idioma = st.session_state.get('idioma', 'pt')
    if idioma not in IDIOMAS:
        idioma = 'pt'
        st.session_state['idioma'] = 'pt'
    return idioma


def definir_idioma(codigo: str):
    """Define o idioma actual na sessão."""
    if codigo in IDIOMAS:
        st.session_state['idioma'] = codigo


def t(chave: str, **kwargs) -> str:
    """
    Traduz uma chave para o idioma actual da sessão.
    Faz fallback para Português ('pt') caso a chave/idioma não exista.
    """
    idioma = obter_idioma()
    item = TRADUCOES.get(chave, {})
    texto = item.get(idioma) or item.get('pt') or chave
    if kwargs:
        try:
            return texto.format(**kwargs)
        except Exception:
            return texto
    return texto


def traduzir_cultura(cultura: str) -> str:
    """Traduz o nome da cultura mantendo o valor original como fallback."""
    idioma = obter_idioma()
    return CULTURAS_TRADUCAO.get(cultura, {}).get(idioma, cultura)


def traduzir_tipo_actividade(tipo: str) -> str:
    """Traduz o tipo de actividade mantendo o valor original como fallback."""
    idioma = obter_idioma()
    return TIPOS_ACTIVIDADE_TRADUCAO.get(tipo, {}).get(idioma, tipo)


def traduzir_estado(estado: str) -> str:
    """Traduz o estado da actividade mantendo o valor original como fallback."""
    idioma = obter_idioma()
    return ESTADOS_TRADUCAO.get(estado, {}).get(idioma, estado)


def traduzir_dia_semana(dia_en: str) -> str:
    """Traduz o dia da semana em inglês para o idioma seleccionado."""
    idioma = obter_idioma()
    return DIAS_SEMANA_TRADUCAO.get(dia_en, {}).get(idioma, dia_en)


def traduzir_nivel_irrigacao(nivel: str) -> tuple[str, str]:
    """Retorna (rotulo, descricao) traduzidos para o nível de irrigação."""
    idioma = obter_idioma()
    dados = NIVEIS_IRRIGACAO_TRADUCAO.get(nivel, {}).get(idioma)
    if not dados:
        dados = NIVEIS_IRRIGACAO_TRADUCAO.get(nivel, {}).get('pt', {'rotulo': nivel, 'descricao': ''})
    return dados['rotulo'], dados['descricao']


def traduzir_recomendacao_5dias(rec_pt: str) -> str:
    """Traduz a recomendação do calendário de 5 dias."""
    idioma = obter_idioma()
    return RECOMENDACOES_5DIAS_TRADUCAO.get(rec_pt, {}).get(idioma, rec_pt)


def render_seletor_idioma(key_suffix: str = ""):
    """
    Renderiza a barra de topo com o botão do Assistente IA e o selector de idioma,
    abrindo o painel interactivo do Chatbot no topo quando activado.
    """
    import importlib
    import utils.assistant as _assistant_mod
    importlib.reload(_assistant_mod)
    from utils.assistant import render_painel_chat_topo, _ui

    idioma_actual = obter_idioma()
    codigos = list(IDIOMAS.keys())
    idx_actual = codigos.index(idioma_actual) if idioma_actual in codigos else 0

    if 'chat_ia_aberto' not in st.session_state:
        st.session_state['chat_ia_aberto'] = False

    col_spacer, col_ia, col_lang = st.columns([2.2, 1.4, 1.4])
    with col_ia:
        st.markdown("<div style='margin-top: 1.72rem;'></div>", unsafe_allow_html=True)
        label_btn = _ui('btn_fechar') if st.session_state['chat_ia_aberto'] else _ui('btn_abrir')
        tipo_btn = "secondary" if st.session_state['chat_ia_aberto'] else "primary"
        if st.button(label_btn, key=f"btn_toggle_ia_{key_suffix}", type=tipo_btn, use_container_width=True):
            st.session_state['chat_ia_aberto'] = not st.session_state['chat_ia_aberto']
            st.rerun()

    with col_lang:
        novo_idioma = st.selectbox(
            f"🌐 {t('seletor_idioma')}",
            options=codigos,
            index=idx_actual,
            format_func=lambda c: IDIOMAS[c],
            key=f"seletor_idioma_{key_suffix}",
        )
        if novo_idioma != idioma_actual:
            definir_idioma(novo_idioma)
            if st.session_state.get('autenticado') and st.session_state.get('agricultor_id'):
                try:
                    from utils.database import actualizar_agricultor
                    actualizar_agricultor(st.session_state['agricultor_id'], {'idioma': novo_idioma})
                except Exception:
                    pass
            st.rerun()

    if st.session_state.get('chat_ia_aberto'):
        render_painel_chat_topo(pagina_actual=key_suffix or "geral", key_prefix=f"chat_{key_suffix}")
