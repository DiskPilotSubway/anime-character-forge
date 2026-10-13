"""Application lifecycle: build the host, load plugins, run the pipeline."""

from __future__ import annotations

from dataclasses import dataclass

from forge.config.settings import Settings, load_settings
from forge.core.pipeline import GenerationPipeline
from forge.loader.plugin_loader import PluginLoader
from forge.registry.plugin_registry import PluginRegistry
from forge.services.character_store import CharacterStore
from forge.utils.logging import get_logger

log = get_logger(__name__)


@dataclass(slots=True)
class ForgeApp:
    """Owns the long-lived objects for a single forge session."""

    settings: Settings
    registry: PluginRegistry
    loader: PluginLoader
    pipeline: GenerationPipeline
    store: CharacterStore

    @classmethod
    def build(cls, settings: Settings | None = None) -> "ForgeApp":
        settings = settings or load_settings()
        registry = PluginRegistry()
        loader = PluginLoader(registry, plugin_dirs=settings.plugin_dirs)
        loader.discover()
        loader.load_enabled(settings.enabled_plugins)
        pipeline = GenerationPipeline(registry, settings)
        store = CharacterStore(settings.output_dir)
        return cls(settings, registry, loader, pipeline, store)

    def shutdown(self) -> None:
        log.info("forge shutting down; %d plugins registered", self.registry.count())
        self.loader.unload_all()