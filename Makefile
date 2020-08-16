.PHONY: install
install:
	poetry install

.PHONY: lint
lint:
	poetry run flake8 maillogger/ tests/

.PHONY: mypy
mypy:
	poetry run mypy --config-file mypy.ini

.PHONY: test
test:
	poetry run pytest tests/

.PHONY: audit
audit:
	poetry export -f requirements.txt | safety check --stdin

.PHONY: release
release:
	poetry publish -n --build -u $(username) -p $(password)
