install:
	@poetry install
	@poetry shell
format:
	@poetry run isort .
	@blue .
lint:
	@prospector --with-tool pydocstyle --doc-warning
	@poetry run isort --check-only .
	@blue --check .
