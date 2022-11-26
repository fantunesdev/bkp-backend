install:
	@python -m venv venv
	@source venv/bin/activate
	@pip install --upgrade pip
	@pip install -r requirements.txt
format:
	@poetry run isort .
	@blue .
lint:
	@prospector --with-tool pydocstyle --doc-warning
	@poetry run isort --check-only .
	@blue --check .
