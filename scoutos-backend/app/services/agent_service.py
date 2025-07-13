"""Agent service and backends for chat and tagging."""

from __future__ import annotations

import os
from typing import Protocol, List

from fastapi import HTTPException
from openai import AsyncOpenAI


class AgentBackend(Protocol):
    """Interface for agent model backends."""

    async def chat(self, prompt: str, max_tokens: int = 200) -> str:
        """Return a chat completion."""

    async def generate_tags(self, content: str) -> List[str]:
        """Suggest tags for ``content``."""

    async def merge_advice(self, memory_a: str, memory_b: str) -> str:
        """Return merge guidance for two memories."""


class OpenAIBackend:
    """Backend that calls the OpenAI API."""

    def __init__(self) -> None:
        self.api_key = os.getenv("OPENAI_API_KEY")

    async def _ask(self, prompt: str, max_tokens: int = 200) -> str:
        if not self.api_key:
            raise HTTPException(
                status_code=500,
                detail="OPENAI_API_KEY environment variable is not set",
            )
        try:
            client = AsyncOpenAI(api_key=self.api_key)
            completions = client.chat.completions
            if hasattr(completions, "create"):
                resp = await completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_tokens,
                )
            else:
                resp = await completions.acreate(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_tokens,
                )
            return resp.choices[0].message.content
        except Exception as exc:  # pragma: no cover - network errors
            raise HTTPException(
                status_code=503,
                detail=f"OpenAI request failed: {exc}",
            )

    async def chat(self, prompt: str, max_tokens: int = 200) -> str:
        return await self._ask(prompt, max_tokens=max_tokens)

    async def generate_tags(self, content: str) -> List[str]:
        prompt = (
            "Suggest 3 to 5 short single-word tags for the following text. "
            "Return only a comma separated list of the tags.\n" + content
        )
        answer = await self._ask(prompt)
        tags = [t.strip() for t in answer.split(";") if t.strip()]
        if len(tags) == 1:
            tags = [t.strip() for t in answer.split(",") if t.strip()]
        return tags

    async def merge_advice(self, memory_a: str, memory_b: str) -> str:
        prompt = (
            "Provide guidance on how to merge the following two memory entries "
            "and explain the reasoning:\nMemory A:\n" + memory_a + "\nMemory B:\n" + memory_b
        )
        return await self._ask(prompt)


class LocalBackend:
    """Very small stub backend for local testing."""

    async def chat(self, prompt: str, max_tokens: int = 200) -> str:  # noqa: ARG002
        return "Local model response"

    async def generate_tags(self, content: str) -> List[str]:  # noqa: ARG002
        return []

    async def merge_advice(self, memory_a: str, memory_b: str) -> str:  # noqa: ARG002
        return "Local merge advice"


class AgentService:
    """Service facade selecting the desired backend."""

    def __init__(self, backend: AgentBackend | None = None) -> None:
        if backend:
            self.backend = backend
        else:
            kind = os.getenv("AGENT_BACKEND", "openai").lower()
            if kind == "local":
                self.backend = LocalBackend()
            else:
                self.backend = OpenAIBackend()

    async def chat(self, prompt: str, max_tokens: int = 200) -> str:
        return await self.backend.chat(prompt, max_tokens=max_tokens)

    async def generate_tags(self, content: str) -> List[str]:
        return await self.backend.generate_tags(content)

    async def merge_advice(self, memory_a: str, memory_b: str) -> str:
        return await self.backend.merge_advice(memory_a, memory_b)

    def get_status(self) -> dict[str, str]:
        return {"backend": self.backend.__class__.__name__}

