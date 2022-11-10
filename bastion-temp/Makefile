format:
	pipenv run isort --profile black bastion
	pipenv run black bastion

run:
	make format
	PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 pipenv run python bastion/main.py

build:
	make format

install:
	pipenv install --dev

test:
	pipenv run pytest
