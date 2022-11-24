install:
	@python -m venv venv
	@source venv/bin/activate
	@pip install --upgrade pip
	@pip install -r requirements.txt
format:
	@isort .
	@blue .
lint:
	@isort . --check
	@blue . --check
	@prospector --with-tool pep257 --doc-warning
