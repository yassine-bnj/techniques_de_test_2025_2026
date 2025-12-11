.PHONY: test unit_test perf_test coverage lint doc

test:
	python -m pytest

unit_test:
	python -m pytest -m "not performance"

perf_test:
	python -m pytest -m performance

coverage:
	python -m coverage run -m pytest -m "not performance"
	python -m coverage report

lint:
	python -m ruff check .

doc:
	python -m pdoc -o docs triangulator --force