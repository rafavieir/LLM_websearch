# Publicar no GitHub

Dentro desta pasta:

```bash
git init
git add .
git commit -m "Initial local research agent showcase"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/local-research-agent.git
git push -u origin main
```

Antes de publicar:

```bash
git status --ignored
```

Confirme que `.env`, `.venv`, `__pycache__` e `memory.json` aparecem como
ignorados ou nao aparecem no commit.

Sugestao de nome para o repo:

```text
local-research-agent
ollama-websearch-agent
local-ai-research-agent
```
