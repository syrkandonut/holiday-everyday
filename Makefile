ifneq (,$(wildcard .env))
    include .env
    export
endif

.PHONY: run
run:
	python manage.py runserver ${SERVER_PORT}

.PHONY: seed
seed:
	python manage.py loaddata tags

.PHONY: admin
admin:
	python manage.py createsuperuser

.PHONY: makemigra
makemigra:
	python manage.py makemigrations

.PHONY: migra
migra:
	python manage.py migrate

.PHONY: lint
lint:
	python scripts/lint.py

.PHONY: format
format:
	python scripts/format.py
