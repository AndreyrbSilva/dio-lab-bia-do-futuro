import json
import pandas as pd
import requests
import streamlit as st

# ============ CONFIGURAÇÃO ============
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODELO = "llama-3.3-70b-versatile"

# ============ CARREGAR DADOS ============
perfil = json.load(open('./data/perfil_usuario.json'))
metas = json.load(open('./data/metas.json'))
transacoes = pd.read_csv('./data/transacoes.csv')
historico = pd.read_csv('./data/historico_metas.csv')

# ============ MONTAR CONTEXTO ============
contexto = f"""
USUÁRIO: {perfil['nome']}, {perfil['idade']} anos, {perfil['profissao']}
RENDA MENSAL: R$ {perfil['renda_mensal']} | GASTOS FIXOS: R$ {perfil['gastos_fixos_mensais']} | DISPONÍVEL: R$ {perfil['saldo_disponivel_estimado']}

METAS ATIVAS:
{json.dumps(metas, indent=2, ensure_ascii=False)}

TRANSAÇÕES RECENTES:
{transacoes.to_string(index=False)}

METAS CONCLUÍDAS:
{historico.to_string(index=False)}
"""

# ============ SYSTEM PROMPT ============
SYSTEM_PROMPT = """Você é o Rumo, um assistente de planejamento financeiro objetivo e direto.

OBJETIVO:
Ajudar jovens adultos a transformar metas financeiras em planos concretos, calculando prazos e aportes mensais com base na renda e nos gastos reais do usuário.

REGRAS:
- Use SEMPRE os dados fornecidos no contexto (perfil, metas, transações);
- NUNCA recomende produtos financeiros ou onde guardar o dinheiro;
- NUNCA invente valores, prazos ou projeções sem base nos dados do usuário;
- Se uma meta estiver inviável no prazo desejado, seja honesto e sugira ajustes;
- Linguagem informal e direta, sem enrolação;
- Se não tiver uma informação necessária, pergunte ao usuário antes de calcular;
- Responda de forma objetiva, com no máximo 3 parágrafos.
"""

# ============ CHAMAR GROQ ============
def perguntar(msg):
    r = requests.post(
        GROQ_URL,
        headers={
            "Authorization": f"Bearer {st.secrets['GROQ_API_KEY']}",
            "Content-Type": "application/json",
        },
        json={
            "model": MODELO,
            "messages": [
                {"role": "system", "content": f"{SYSTEM_PROMPT}\n\nCONTEXTO DO USUÁRIO:\n{contexto}"},
                {"role": "user", "content": msg},
            ],
        },
    )
    return r.json()["choices"][0]["message"]["content"]

# ============ INTERFACE ============
st.title("🎯 Rumo, seu planejador de metas financeiras")

if pergunta := st.chat_input("Me conta sua meta ou dúvida..."):
    st.chat_message("user").write(pergunta)
    with st.spinner("Calculando..."):
        st.chat_message("assistant").write(perguntar(pergunta))
        
