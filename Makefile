.PHONY: clean system-packages python-packages install tests run all

clean:
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.log' -delete

system-packages:
	sudo apt install python-pip -y

python-packages:
	pip install -r requirements.txt

install: system-packages python-packages

test:
	python manage.py test

run:
	python manage.py runserver

all: clean install tests run

dbcreate:
	python manage.py create_db

migrate:
	python manage.py database migrate

initdb:
	python manage.py database init
