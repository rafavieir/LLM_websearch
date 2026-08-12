# LLM Websearch

**uma IA local pode pesquisar na web antes de responder.**

Ollama + Qwen + Python. Quando a pergunta precisa de informacao atual, o
agente faz uma busca web, monta uma ideia com base nos resultados e depois gera
a resposta final.

## Como funciona

```text
pergunta do usuario
-> busca na web
-> cria uma ideia com base nos resultados
-> responde usando esse contexto
```

No terminal aparecem duas partes:

```text
Agent idea >
ideia que o modelo criou com base na pesquisa

Agent >
resposta final
```

## Tecnologias

- Python
- Ollama
- Qwen
- ddgs para websearch
- dotenv para configuracao

## Rodando

```bash
python -m venv .venv
pip install -r requirements.txt
cp .env.example .env
python run.py
```

No Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python run.py
```

## Configuracao

Edite o `.env` se precisar:

```env
OLLAMA_BASE_URL=http://127.0.0.1:11434
OLLAMA_MODEL=qwen3:8b
```

Se o Ollama estiver em uma VPS, da para usar tunel SSH:

```bash
ssh -L 11434:127.0.0.1:11434 usuario@IP_DA_VPS
python run.py
```

## Comandos

Dentro do chat:

```text
/check
/web novidades do Ollama
/clear
/exit
```

Tambem da para perguntar de forma normal:

```text
pesquise boas praticas para agentes locais com LLM
```

## Ideia

O projeto e pequeno de proposito.

A intencao foi mostrar um fluxo simples de IA local com ferramenta:

1. pesquisar;
2. usar contexto real;
3. gerar uma ideia;
4. responder melhor.

Nao e um produto final, e um experimento de homelab.
