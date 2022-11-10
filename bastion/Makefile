
migrate:
	pipenv run alembic upgrade head

format:
	pipenv run autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place bastion test --exclude=__init__.py
	pipenv run isort --profile black bastion test
	pipenv run black bastion test