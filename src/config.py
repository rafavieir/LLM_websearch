from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434").strip().rstrip("/")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "qwen3:8b").strip()
    ollama_timeout: int = int(os.getenv("OLLAMA_TIMEOUT", "180"))
    ollama_temperature: float = float(os.getenv("OLLAMA_TEMPERATURE", "0.2"))
    search_region: str = os.getenv("SEARCH_REGION", "br-pt").strip()
    search_max_results: int = int(os.getenv("SEARCH_MAX_RESULTS", "6"))
