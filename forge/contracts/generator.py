"""Generator contract — the primary plugin surface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class CharacterRequest:
    prompt: str
    seed: int | None = None
    quality: str = "standard"
    negative: str = ""
    capabilities: frozenset[str] = field(default_factory=lambda: frozenset({"face", "body"}))


@dataclass(slots=True)
class CharacterSheet:
    id: str
    prompt: str
    seed: int
    palette: list[str]
    layers: dict[str, Any]
    meta: dict[str, Any] = field(default_factory=dict)


class GeneratorPlugin(ABC):
    """Turns a CharacterRequest into a CharacterSheet."""

    name: str = "unnamed-generator"
    version: str = "0.0.0"
    capabilities: frozenset[str] = frozenset()

    @abstractmethod
    def generate(self, req: CharacterRequest) -> CharacterSheet: ...