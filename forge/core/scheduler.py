"""Job scheduler for batch generation."""

from __future__ import annotations

import queue
import threading
from collections.abc import Iterable
from dataclasses import dataclass, field

from forge.contracts.generator import CharacterRequest, CharacterSheet
from forge.utils.logging import get_logger

log = get_logger(__name__)


@dataclass(slots=True)
class Job:
    request: CharacterRequest
    result: CharacterSheet | None = None
    error: BaseException | None = None


@dataclass(slots=True)
class Scheduler:
    """Bounded, single-producer/multi-worker job queue."""

    max_workers: int = 2
    _queue: queue.Queue[Job] = field(default_factory=queue.Queue)
    _workers: list[threading.Thread] = field(default_factory=list)
    _stop: threading.Event = field(default_factory=threading.Event)

    def submit(self, requests: Iterable[CharacterRequest]) -> None:
        for req in requests:
            self._queue.put(Job(request=req))

    def start(self, handler) -> None:  # noqa: ANN001 - handler is a callable
        for i in range(self.max_workers):
            t = threading.Thread(target=self._worker, args=(handler,), name=f"forge-w{i}", daemon=True)
            t.start()
            self._workers.append(t)

    def _worker(self, handler) -> None:  # noqa: ANN001
        while not self._stop.is_set():
            try:
                job = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue
            try:
                job.result = handler(job.request)
            except BaseException as exc:  # noqa: BLE001 - job isolation
                job.error = exc
                log.exception("job failed prompt=%r", job.request.prompt)
            finally:
                self._queue.task_done()

    def stop(self) -> None:
        self._stop.set()
        for t in self._workers:
            t.join(timeout=2.0)