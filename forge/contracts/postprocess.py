"""Post-process contract — final pass over a finished character."""

from __future__ import annotations

from abc import ABC, abstractmethod

from forge.models.character import Character


class PostProcessPlugin(ABC):
    name: str = "unnamed-post"
    version: str = "0.0.0"

    @abstractmethod
    def finish(self, character: Character) -> Character: ...