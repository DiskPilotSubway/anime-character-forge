"""Discovers plugin directories, reads manifests, imports entry points."""

from __future__ import annotations

import importlib
import importlib.util
import sys
from dataclasses import dataclass
from pathlib import Path

from forge.contracts import API_VERSION
from forge.registry.plugin_registry import PluginRegistry
from forge.utils.logging import get_logger

log = get_logger(__name__)


@dataclass(slots=True)
class PluginManifest:
    id: str
    name: str
    version: str
    api: str
    entry: str
    capabilities: tuple[str, ...]
    root: Path


class PluginLoader:
    """Walks plugin dirs, parses `plugin.toml`, imports entry modules."""

    def __init__(self, registry: PluginRegistry, plugin_dirs: tuple[Path, ...]) -> None:
        self._registry = registry
        self._dirs = plugin_dirs
        self._manifests: dict[str, PluginManifest] = {}
        self._loaded: list[str] = []

    def discover(self) -> list[PluginManifest]:
        self._manifests.clear()
        for root in self._dirs:
            if not root.exists():
                continue
            for manifest in root.glob("*/plugin.toml"):
                try:
                    m = self._parse(manifest)
                except Exception as exc:  # noqa: BLE001
                    log.warning("bad manifest %s: %s", manifest, exc)
                    continue
                self._manifests[m.id] = m
        log.info("discovered %d plugins", len(self._manifests))
        return list(self._manifests.values())

    def load_enabled(self, enabled: tuple[str, ...]) -> list[str]:
        for pid in enabled:
            m = self._manifests.get(pid)
            if m is None:
                log.warning("plugin %s requested but not found", pid)
                continue
            if m.api != API_VERSION:
                log.warning("plugin %s targets api %s (host is %s)", pid, m.api, API_VERSION)
            self._import(m)
            self._loaded.append(pid)
        return list(self._loaded)

    def unload_all(self) -> None:
        for pid in self._loaded:
            self._registry.remove_owner(pid)
        self._loaded.clear()

    def _parse(self, manifest_path: Path) -> PluginManifest:
        import tomllib

        data = tomllib.loads(manifest_path.read_text(encoding="utf-8"))
        meta = data["plugin"]
        return PluginManifest(
            id=meta["id"],
            name=meta["name"],
            version=meta["version"],
            api=meta["api"],
            entry=meta["entry"],
            capabilities=tuple(meta.get("capabilities", ())),
            root=manifest_path.parent,
        )

    def _import(self, m: PluginManifest) -> None:
        module_name, _, cls_name = m.entry.partition(":")
        if str(m.root) not in sys.path:
            sys.path.insert(0, str(m.root))
        spec = importlib.util.spec_from_file_location(
            f"forge_plugin_{m.id}", m.root / f"{module_name}.py"
        )
        if spec is None or spec.loader is None:
            raise ImportError(f"cannot import plugin {m.id}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        cls = getattr(module, cls_name)
        instance = cls()
        self._registry.register(plugin_id=m.id, instance=instance, capabilities=m.capabilities)
        log.info("loaded plugin %s (%s)", m.id, m.version)

    def check_updates(self) -> None:  # placeholder for the 0.7 updater
        pass
</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>