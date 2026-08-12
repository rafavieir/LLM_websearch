from __future__ import annotations

import re

from .config import Settings
from .ollama_client import OllamaClient
from .web_search import render_search_context, search_web


SYSTEM_PROMPT = """
You are a local research agent running on top of Ollama.

Behavior:
- Answer like a practical technical collaborator, not a generic chatbot.
- Use web search context when it is provided.
- Separate facts, assumptions, and recommendations when the topic is uncertain.
- Do not invent search results, dates, URLs, versions, prices, or current facts.
- When using web results, cite the URLs from the provided context.
- Keep answers concise unless the user asks for detail.
"""


IDEA_PROMPT = """
You are the synthesis layer of a local AI research agent.

Read the web search context and create your own grounded idea from it.
Do not merely summarize links. Build a useful angle, hypothesis, or conclusion
that could become a short post, note, or technical recommendation.

Return:
- Core idea
- Why it matters
- Evidence from the search context
- Caveats

Only use the provided search context. Do not invent sources.
"""


SEARCH_TRIGGERS = (
    "pesquise",
    "busque",
    "procure",
    "websearch",
    "web search",
    "google",
    "noticia",
    "notícias",
    "latest",
    "atual",
    "hoje",
    "2026",
)


def should_search(text: str) -> bool:
    lowered = text.lower()
    return lowered.startswith("/web ") or any(trigger in lowered for trigger in SEARCH_TRIGGERS)


def clean_search_query(text: str) -> str:
    if text.lower().startswith("/web "):
        return text[5:].strip()
    cleaned = re.sub(r"\b(pesquise|busque|procure|websearch|web search)\b", "", text, flags=re.IGNORECASE)
    return cleaned.strip() or text.strip()


class ResearchAgent:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or Settings()
        self.client = OllamaClient(self.settings)
        self.messages: list[dict[str, str]] = [{"role": "system", "content": SYSTEM_PROMPT.strip()}]

    def reset(self) -> None:
        self.messages = [{"role": "system", "content": SYSTEM_PROMPT.strip()}]

    def ask(self, question: str) -> tuple[str, int, str | None]:
        search_count = 0
        generated_idea: str | None = None
        if should_search(question):
            query = clean_search_query(question)
            results = search_web(query, settings=self.settings)
            search_count = len(results)
            search_context = render_search_context(query, results)
            generated_idea = self._generate_research_idea(question, search_context)
            self.messages.append(
                {
                    "role": "system",
                    "content": (
                        f"{search_context}\n\n"
                        "AGENT GENERATED IDEA FROM THE SEARCH\n"
                        f"{generated_idea}\n\n"
                        "Use the generated idea as the main angle, but keep the final answer aligned with the user's request."
                    ),
                }
            )

        self.messages.append({"role": "user", "content": question})
        answer = self.client.chat(self.messages)
        self.messages.append({"role": "assistant", "content": answer})
        self._trim_history()
        return answer, search_count, generated_idea

    def _generate_research_idea(self, question: str, search_context: str) -> str:
        messages = [
            {"role": "system", "content": IDEA_PROMPT.strip()},
            {"role": "system", "content": search_context},
            {"role": "user", "content": f"Question: {question}\nGenerate the grounded idea now."},
        ]
        return self.client.chat(messages)

    def _trim_history(self, keep_last: int = 24) -> None:
        if len(self.messages) <= keep_last + 1:
            return
        self.messages = [
            self.messages[0],
            {"role": "system", "content": "Conversation was trimmed. Prioritize the latest request."},
            *self.messages[-keep_last:],
        ]
