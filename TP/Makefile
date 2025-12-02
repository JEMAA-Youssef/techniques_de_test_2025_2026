# --- Test targets ---
test:
	PYTHONPATH=$(PWD) pytest -v

unit_test:
	PYTHONPATH=$(PWD) pytest -v --ignore=tests/performance

perf_test:
	PYTHONPATH=$(PWD) pytest -v tests/performance

coverage:
	PYTHONPATH=$(PWD) coverage run -m pytest && coverage report -m && coverage html

lint:
	ruff check .

doc:
	pdoc3 triangulator -o docs
