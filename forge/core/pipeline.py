"""The generation pipeline: request -> resolve -> generate -> post-process."""

from __future__ import annotations

from dataclasses import dataclass

from forge.config.settings import Settings
from forge.contracts.generator import CharacterRequest, CharacterSheet
from forge.models.character import Character
from forge.registry.plugin_registry import PluginRegistry
from forge.utils.logging import get_logger
from forge.utils.timing import timed

log = get_logger(__name__)


@dataclass(slots=True)
class PipelineStage:
    name: str
    plugin_id: str


class GenerationPipeline:
    """Runs the built-in chain: generator -> style -> post-process."""

    def __init__(self, registry: PluginRegistry, settings: Settings) -> None:
        self._registry = registry
        self._settings = settings

    @timed
    def run(self, prompt: str, seed: int | None = None) -> CharacterSheet:
        request = CharacterRequest(prompt=prompt, seed=seed, quality=self._settings.quality)
        log.info("pipeline start prompt=%r seed=%s", prompt, seed)

        generator = self._registry.pick_generator(request.capabilities)
        sheet = generator.generate(request)
        character = Character.from_sheet(sheet)

        for style in self._registry.iter_styles():
            character = style.apply(character)

        for post in self._registry.iter_post_processors():
            character = post.finish(character)

        log.info("pipeline done id=%s", character.id)
        return character.to_sheet()