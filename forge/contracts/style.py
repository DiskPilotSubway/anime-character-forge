"""Style contract — palette / lineart rewriting."""

from __future__ import annotations

from abc import ABC, abstractmethod

from forge.models.character import Character


class StylePlugin(ABC):
    name: str = "unnamed-style"
    version: str = "0.0.0"

    @abstractmethod
    def apply(self, character: Character) -> Character: ...