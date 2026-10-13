"""Shared plugin contracts. Bump API_VERSION when these change."""

from forge.contracts.generator import CharacterRequest, CharacterSheet, GeneratorPlugin
from forge.contracts.postprocess import PostProcessPlugin
from forge.contracts.style import StylePlugin

API_VERSION = "1.2"

__all__ = [
    "API_VERSION",
    "CharacterRequest",
    "CharacterSheet",
    "GeneratorPlugin",
    "PostProcessPlugin",
    "StylePlugin",
]