"""Command-line entry point for the forge."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from forge.bootstrap.app import ForgeApp
from forge.config.settings import load_settings
from forge.utils.logging import configure_logging
from forge.utils.paths import default_output_dir


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="forge", description="AI anime character forge")
    p.add_argument("--gui", action="store_true", help="launch the desktop UI")
    p.add_argument("--generate", metavar="PROMPT", help="generate one character from a prompt")
    p.add_argument("--seed", type=int, default=None, help="deterministic seed")
    p.add_argument("--out", type=Path, default=default_output_dir(), help="output directory")
    p.add_argument("--list-plugins", action="store_true", help="list registered plugins and exit")
    p.add_argument("--enable", action="append", default=[], help="enable a plugin by id")
    p.add_argument("-v", "--verbose", action="store_true")
    return p


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    configure_logging(verbose=args.verbose)

    settings = load_settings()
    if args.enable:
        settings.enabled_plugins = tuple(dict.fromkeys((*settings.enabled_plugins, *args.enable)))
    settings.output_dir = args.out

    app = ForgeApp.build(settings)

    if args.list_plugins:
        for entry in app.registry.describe():
            print(f"{entry.id:<24} v{entry.version:<8} caps={','.join(entry.capabilities)}")
        return 0

    if args.generate:
        sheet = app.pipeline.run(prompt=args.generate, seed=args.seed)
        path = app.store.save(sheet)
        print(f"saved -> {path}")
        return 0

    if args.gui:
        from forge.bootstrap.gui import launch

        return launch(app)

    print("nothing to do; pass --generate, --list-plugins, or --gui", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())