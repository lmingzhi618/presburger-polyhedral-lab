test:
	pytest -v

cov:
	pytest --cov=src --cov-report=term-missing
