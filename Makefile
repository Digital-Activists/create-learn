.PHONY: resetmigrations run

resetmigrations:
	find . -path "CreateLearn/apps/*/migrations/*.py" -not -name "__init__.py" -delete
	find . -path "CreateLearn/apps/*/migrations/*.pyc" -delete
	find . -path "CreateLearn/db.sqlite3" -delete
	python manage.py makemigrations
	python manage.py migrate

run:
	python manage.py runserver

reset-and-run: resetmigrations run