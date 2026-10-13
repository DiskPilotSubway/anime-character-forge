"""Thin desktop launcher. The real UI lives in a separate plugin in 0.7."""

from __future__ import annotations

from forge.bootstrap.app import ForgeApp
from forge.utils.logging import get_logger

log = get_logger(__name__)


def launch(app: ForgeApp) -> int:
    log.info("GUI launch requested; falling back to console mode in 0.6.x")
    print("forge GUI is under construction — use --generate for now")
    return 0