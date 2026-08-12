from __future__ import annotations

from src.agent import ResearchAgent
from src.config import Settings
from src.ollama_client import OllamaError
from src.web_search import SearchError


def main() -> int:
    settings = Settings()
    agent = ResearchAgent(settings)

    print()
    print("=" * 72)
    print(" Local Research Agent - Ollama + Web Search")
    print("=" * 72)
    print(f"Model : {settings.ollama_model}")
    print(f"Ollama: {settings.ollama_base_url}")
    print()
    print("Commands: /web <query>, /check, /clear, /exit")
    print("-" * 72)

    while True:
        try:
            question = input("\nYou > ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nBye.")
            return 0

        if not question:
            continue
        if question.lower() in {"/exit", "exit", "quit", "sair"}:
            print("Bye.")
            return 0
        if question.lower() in {"/clear", "clear", "limpar"}:
            agent.reset()
            print("Conversation cleared.")
            continue
        if question.lower() == "/check":
            try:
                status = agent.client.check()
                print(f"Ollama OK: {status['base_url']}")
                print(f"Configured model: {status['model']}")
                print(f"Model available: {status['model_available']}")
                print("Available models:", ", ".join(status["available_models"]) or "(none)")
            except OllamaError as exc:
                print(f"Check failed: {exc}")
            continue

        try:
            answer, search_count, generated_idea = agent.ask(question)
        except (OllamaError, SearchError) as exc:
            print(f"Error: {exc}")
            continue

        print()
        if search_count:
            print(f"[websearch] {search_count} result(s) injected")
        if generated_idea:
            print()
            print("Agent idea >")
            print(generated_idea)
            print()
        print("Agent >")
        print(answer)


if __name__ == "__main__":
    raise SystemExit(main())
