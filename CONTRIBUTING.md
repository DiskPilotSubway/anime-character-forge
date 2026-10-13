# Contributing to anime-character-forge

Thanks for wanting to help build the forge. This repo is a **Windows-first
desktop tool** for generating AI anime characters — face, body, outfit,
palette, and pose — driven by a plugin host so the community can ship new
generators, style packs, and post-processors without touching core.

We take plugins seriously. The core stays small; the plugins do the work.

## Repo layout

```
anime-character-forge/
├── forge/                  # core host — the plugin runtime
│   ├── bootstrap/          # entry point, CLI, app lifecycle
│   ├── core/               # generation pipeline, scheduler, job graph
│   ├── loader/             # plugin discovery + import machinery
│   ├── registry/           # plugin registration, capability table
│   ├── contracts/          # shared ABCs + dataclasses (the plugin API)
│   ├── handlers/           # built-in request handlers
│   ├── services/           # model runtime, IO, cache, telemetry
│   ├── models/             # domain models (Character, Palette, Pose…)
│   ├── config/             # settings loader, default TOML
│   └── utils/              # logging, timing, paths, image helpers
├── plugins/                # first-party plugins shipped in-tree
├── tests/                  # pytest suite
├── docs/                   # extra docs (see /docs)
├── pyproject.toml
└── Makefile
```

## Setting up

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
pytest -q
```

We target **Python 3.12** on Windows 10/11 (x64). Linux/macOS work for
development but the shipping target is Windows.

## Writing a plugin

Every plugin implements one or more contracts from `forge/contracts/`.
The three required surfaces:

1. `GeneratorPlugin` — turns a `CharacterRequest` into a `CharacterSheet`.
2. `StylePlugin` — optionally rewrites the character's palette / lineart.
3. `PostProcessPlugin` — final pass (upscale, cleanup, tag).

Minimal example:

```python
from forge.contracts.generator import GeneratorPlugin, CharacterRequest, CharacterSheet

class MyAnimeGen(GeneratorPlugin):
    name = "my-anime-gen"
    version = "0.1.0"
    capabilities = {"face", "body"}

    def generate(self, req: CharacterRequest) -> CharacterSheet:
        ...
```

Drop the module under `plugins/<your_plugin>/` with a `plugin.toml`
manifest. The loader will pick it up on next launch.

## Plugin manifest

```toml
[plugin]
id = "my-anime-gen"
name = "My Anime Generator"
version = "0.1.0"
api = "1.2"
entry = "my_anime_gen:MyAnimeGen"
capabilities = ["face", "body"]

[plugin.meta]
author = "you"
license = "MIT"
```

## Style rules

- Type hints on every public function. `mypy --strict` on `forge/` must pass.
- No global mutable state. The registry is the only shared authority.
- Logging via `forge.utils.logging.get_logger(__name__)` — no `print`.
- Image buffers are always `numpy.ndarray` (H, W, 4) uint8, RGBA order.
- Determinism matters: pass the seed through, never call `random` directly.

## Tests

- Unit tests live next to their module in `tests/`.
- A plugin without a test does not merge.
- Run `make check` before opening a PR — it runs ruff, mypy, and pytest.

## Commit style

Conventional-ish, lowercase, imperative:

```
loader: add hot-reload for plugin.toml changes
core: split job graph into scheduler + executor
contracts: add StyleTransfer contract v0.3
```

## PR checklist

- [ ] `make check` passes
- [ ] New plugin has a manifest + a test
- [ ] Public API changes bump `api` in `forge/contracts/__init__.py`
- [ ] No new binary blobs in the tree