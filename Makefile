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