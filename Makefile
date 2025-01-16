.PHONY: run
run:
	python manage.py runserver 0.0.0.0:8000

.PHONY: lint
lint:
	python scripts/lint.py

.PHONY: format
format:
	python scripts/format.py