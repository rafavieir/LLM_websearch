from __future__ import annotations

from typing import Any

import requests

from .config import Settings


class OllamaError(RuntimeError):
    pass


class OllamaClient:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or Settings()

    def check(self) -> dict[str, Any]:
        try:
            response = requests.get(
                f"{self.settings.ollama_base_url}/api/tags",
                timeout=min(self.settings.ollama_timeout, 30),
            )
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as exc:
            raise OllamaError(f"Could not reach Ollama at {self.settings.ollama_base_url}: {exc}") from exc
        except ValueError as exc:
            raise OllamaError("Ollama returned invalid JSON.") from exc

        models = [item.get("name", "") for item in data.get("models", []) if item.get("name")]
        return {
            "base_url": self.settings.ollama_base_url,
            "model": self.settings.ollama_model,
            "model_available": self.settings.ollama_model in models,
            "available_models": models,
        }

    def chat(self, messages: list[dict[str, str]]) -> str:
        payload = {
            "model": self.settings.ollama_model,
            "messages": messages,
            "stream": False,
            "think": False,
            "options": {"temperature": self.settings.ollama_temperature},
        }

        try:
            response = requests.post(
                f"{self.settings.ollama_base_url}/api/chat",
                json=payload,
                timeout=self.settings.ollama_timeout,
            )
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as exc:
            raise OllamaError(f"Ollama chat failed: {exc}") from exc
        except ValueError as exc:
            raise OllamaError("Ollama returned invalid JSON.") from exc

        message = data.get("message")
        if not isinstance(message, dict) or not isinstance(message.get("content"), str):
            raise OllamaError("Ollama returned an unexpected response shape.")
        return message["content"]
