# Sustentabilidade Agrónoma

Sistema de apoio à decisão de irrigação e controlo de actividades agrícolas para Moçambique, desenvolvido em Python.

## Funcionalidades Principais

- **Página Inicial de Apresentação** — visão geral da plataforma e fluxo de utilização
- **Cadastro e Recuperação de Senha** — registo de agricultores, machambas, culturas e áreas com redefinição segura de senha
- **Painel de Irrigação** — monitoria de temperatura e condições agrometeorológicas em tempo real para as províncias de Moçambique
- **Previsão para 5 Dias** — identificação dos dias e horários ideais para irrigação com cálculo da lâmina de água
- **Análise Gráfica** — evolução térmica de 48 horas e humidade volumétrica do solo
- **Controlo de Actividades** — registo da hora de início e fim das actividades agrícolas e verificação de cumprimento
- **Multi-Idioma (Línguas Nacionais)** — interface disponível em Português, Changana, Ronga, Makhuwa e Sena
- **Assistente IA no Topo** — chatbot interactivo para dúvidas frequentes, onboarding, glossário técnico e recomendações contextuais

## Arquitectura Técnica

- **Linguagem:** Python
- **Processamento e Ciência de Dados:** Pandas
- **Visualização de Dados:** Plotly
- **Persistência de Dados:** MongoDB Atlas (`sustentabilidadedb`) com espelho local em SQLite (`data/sustentabilidade.db`)

## Execução do Projecto

```bash
pip install -r requirements.txt
python -m streamlit run app.py
```
