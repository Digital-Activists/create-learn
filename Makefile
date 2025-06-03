.PHONY: resetmigrations run

resetmigrations:
	find . -path "*/CreateLearn/apps/*/migrations/*.py" ! -name "__init__.py" -delete
	find . -path "*/CreateLearn/apps/*/migrations/*.pyc" -delete
	find . -path "*/CreateLearn/db.sqlite3" -delete
	python manage.py makemigrations
	python manage.py migrate
	python manage.py fill_all_data

run:
	python manage.py runserver

reset-and-run: resetmigrations run

pip-install-dev:
	pip install --upgrade pip pip-tools
	pip-sync requirements.txt requirements-dev.txt

pip-install:
	pip install --upgrade pip pip-tools
	pip-sync requirements.txt

pip-update:
	pip install --upgrade pip pip-tools
	pip-compile requirements.in
	pip-compile requirements-dev.in
	pip-sync requirements.txt requirements-dev.txt