# Local Research Agent

A small portfolio-friendly homelab project that connects a local Ollama model
to web search and lets the model build its own grounded idea before answering.

It is intentionally standalone and safe to publish: no production credentials,
no private ticket data, no internal integrations.

## What It Does

- Runs locally against Ollama.
- Uses `qwen3:8b` or any model available in your Ollama instance.
- Performs web search with `ddgs` when the user asks for current information.
- Runs a synthesis step where the model creates a grounded idea from the search.
- Injects both the evidence and the generated idea before answering.
- Keeps the CLI simple enough to understand and extend.

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
cp .env.example .env
python run.py
```

If Ollama is running on a VPS, create an SSH tunnel:

```bash
ssh -L 11434:127.0.0.1:11434 user@YOUR_VPS_IP
python run.py
```

## Configuration

Edit `.env`:

```env
OLLAMA_BASE_URL=http://127.0.0.1:11434
OLLAMA_MODEL=qwen3:8b
OLLAMA_TIMEOUT=180
OLLAMA_TEMPERATURE=0.2
SEARCH_REGION=br-pt
SEARCH_MAX_RESULTS=6
```

## Commands

Inside the chat:

```text
/check
/web latest Ollama tool calling examples
/clear
/exit
```

Natural language also works:

```text
Pesquise as novidades do Ollama e resuma com links.
Busque boas praticas para agentes locais com LLM.
```

When web search is triggered, the CLI prints two sections:

```text
Agent idea >
...the model's own grounded idea based on the search...

Agent >
...the final answer to the user...
```

## Architecture

```text
run.py
src/
  agent.py          # search -> idea synthesis -> final answer
  config.py         # .env settings
  ollama_client.py  # Ollama /api/chat wrapper
  web_search.py     # ddgs search adapter
```

## Why This Exists

This repository is a small public showcase of local AI orchestration:

- local-first LLM usage;
- tool/context injection;
- web search as evidence;
- model-generated ideas grounded in that evidence;
- clean separation between model, tool, and interface.

It is a compact version of the same engineering pattern used in internal support
automation: collect evidence first, synthesize an angle, then let the model
answer over confirmed context.
