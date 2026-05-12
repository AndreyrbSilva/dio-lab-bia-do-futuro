# Base de Conhecimento

## Dados Utilizados

| Arquivo | Formato | Utilização no Rumo |
|---------|---------|---------------------|
| `perfil_usuario.json` | JSON | Carregar renda mensal, gastos fixos e nome do usuário para personalizar o planejamento |
| `metas.json` | JSON | Armazenar as metas ativas do usuário (nome, valor total, valor guardado, prazo) |
| `transacoes.csv` | CSV | Calcular quanto o usuário realmente tem disponível por mês com base no histórico de gastos |
| `historico_metas.csv` | CSV | Mostrar metas já concluídas e reforçar o progresso do usuário |

---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

Os arquivos originais foram adaptados para o contexto de planejamento de metas. O `perfil_investidor.json` foi renomeado para `perfil_usuario.json` e os campos de perfil de investidor foram substituídos por informações de renda e gastos fixos mensais. O `produtos_financeiros.json` foi removido, pois o Rumo não trabalha com produtos financeiros. No lugar, foi criado o arquivo `metas.json` para armazenar as metas ativas do usuário com valor, progresso e prazo.

---

## Estratégia de Integração

### Como os dados são carregados?

Os arquivos JSON e CSV são carregados no início da sessão e injetados diretamente no prompt do agente:

```python
import pandas as pd
import json

perfil = json.load(open('./data/perfil_usuario.json'))
metas = json.load(open('./data/metas.json'))
transacoes = pd.read_csv('./data/transacoes.csv')
historico_metas = pd.read_csv('./data/historico_metas.csv')
```

### Como os dados são usados no prompt?

Os dados são injetados no system prompt para que o Rumo tenha contexto completo do usuário desde o início da conversa. Em soluções mais robustas, o ideal seria carregar essas informações dinamicamente para suportar múltiplos usuários e atualizações em tempo real.

```text
PERFIL DO USUÁRIO (data/perfil_usuario.json):
{
  "nome": "Ana Costa",
  "idade": 24,
  "profissao": "Designer Freelancer",
  "renda_mensal": 3500.00,
  "gastos_fixos_mensais": 1800.00,
  "saldo_disponivel_estimado": 1700.00
}

METAS ATIVAS DO USUÁRIO (data/metas.json):
[
  {
    "meta": "Viagem para a Europa",
    "valor_total": 8000.00,
    "valor_guardado": 1200.00,
    "aporte_mensal_planejado": 400.00,
    "prazo_desejado": "2026-07"
  },
  {
    "meta": "Notebook novo",
    "valor_total": 4500.00,
    "valor_guardado": 900.00,
    "aporte_mensal_planejado": 300.00,
    "prazo_desejado": "2025-12"
  }
]

TRANSAÇÕES DO USUÁRIO (data/transacoes.csv):
data,descricao,categoria,valor,tipo
2025-10-01,Freela design,receita,3500.00,entrada
2025-10-02,Aluguel,moradia,900.00,saida
2025-10-05,Supermercado,alimentacao,380.00,saida
2025-10-08,Conta de Luz,moradia,95.00,saida
2025-10-10,Uber,transporte,60.00,saida
2025-10-12,iFood,alimentacao,95.00,saida
2025-10-15,Spotify,lazer,21.90,saida
2025-10-18,Academia,saude,89.00,saida
2025-10-20,Farmácia,saude,45.00,saida
2025-10-25,Reserva viagem,meta,400.00,saida

HISTÓRICO DE METAS CONCLUÍDAS (data/historico_metas.csv):
data_conclusao,meta,valor_total,meses_para_atingir
2025-03-01,Fundo de emergência,6000.00,8
2025-08-01,Celular novo,2200.00,5
```

---

## Exemplo de Contexto Montado

> Versão sintetizada para otimizar o consumo de tokens mantendo as informações essenciais.

```
DADOS DO USUÁRIO:
- Nome: Ana Costa
- Renda mensal: R$ 3.500
- Gastos fixos: R$ 1.800
- Disponível por mês: R$ 1.700

METAS ATIVAS:
- Viagem Europa: R$ 1.200 / R$ 8.000 (aporte: R$ 400/mês, prazo: jul/2026)
- Notebook novo: R$ 900 / R$ 4.500 (aporte: R$ 300/mês, prazo: dez/2025)

RESUMO DE GASTOS (out/2025):
- Moradia: R$ 995
- Alimentação: R$ 475
- Transporte: R$ 60
- Saúde: R$ 134
- Lazer: R$ 21,90
- Total de saídas: R$ 1.685,90

METAS CONCLUÍDAS: 2 (Fundo de emergência, Celular novo)
```
