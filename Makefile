PATHS = main.py test.py


black:
	black . --check --force-exclude "deps/*"

ruff:
	ruff check $(PATHS)

format:
	black . --force-exclude "deps/*"
	ruff check $(PATHS) --fix

mypy:
	mypy --install-types --non-interactive $(PATHS)

check:
	make format
	make mypy

test:
	pytest test.py -vs --tb=short --disable-warnings