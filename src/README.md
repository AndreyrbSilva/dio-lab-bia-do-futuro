# Passo a Passo de Execução

## Setup da API

```bash
# 1. Criar conta em console.groq.com e gerar uma API key
# 2. Criar o arquivo de secrets do Streamlit
mkdir -p .streamlit
touch .streamlit/secrets.toml
```

Adicionar a key no `.streamlit/secrets.toml`:

```toml
GROQ_API_KEY = "sua-key-aqui"
```

> Nunca suba o `secrets.toml` pro GitHub. Adicione ao `.gitignore`:
> ```bash
> echo ".streamlit/secrets.toml" >> .gitignore
> ```

## Código Completo

Todo o código-fonte está no arquivo `src/app.py`.

## Como Rodar

```bash
# 1. Criar e ativar o ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 2. Instalar dependências
pip install streamlit pandas requests

# 3. Rodar o app
streamlit run ./src/app.py
```

## Evidência de Execução

<img width="1237" height="642" alt="image" src="https://github.com/user-attachments/assets/eb0fb6a8-59f4-4314-9a30-5d4f2b5d2e6e" />
