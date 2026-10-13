.PHONY: install check lint type test fmt run clean

PY := python

install:
	$(PY) -m pip install -e ".[dev,runtime]"

lint:
	ruff check forge tests plugins

fmt:
	ruff format forge tests plugins

type:
	mypy forge

test:
	pytest

check: lint type test

run:
	$(PY) -m forge.bootstrap.cli --gui

clean:
	rmdir /s /q .pytest_cache .mypy_cache .ruff_cache 2>nul || true