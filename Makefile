install:
	@python -m venv venv
	@source venv/bin/activate
	@pip install --upgrade pip
	@pip install -r requirements.txt
format:
	@isort .
	@blue .
lint:
	@prospector --with-tool pydocstyle --doc-warning
	isort --check-only .
	blue --check .
