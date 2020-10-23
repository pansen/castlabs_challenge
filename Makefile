SHELL := /bin/bash
export PYTHONUNBUFFERED := 1

# We use `pipenv` since it provides a convenient locking mechanism and distinguishes
# between dev and prod dependencies. That is the only thing we want from it.
# Usually it is providing much more magic, by setting `PIPENV_VENV_IN_PROJECT=true`
# we instruct it to behave like a regular `venv`.
export PIPENV_VENV_IN_PROJECT=true

PYTHON_GLOBAL := $(shell /usr/bin/which python3.8)
PIPENV := $(PYTHON_GLOBAL) -m pipenv

VENV_DIRNAME := .venv
VENV := ./$(VENV_DIRNAME)

.DEFAULT_GOAL := dev.build

.PHONY: bootstrap
bootstrap:
	@$(PIPENV) > /dev/null 2>&1 \
		&& echo "Dependencies already exist." \
		|| $(PYTHON_GLOBAL) -m pip install pipenv

.env:
	cp .env.example .env

.PHONY: build
build: .env
	$(PIPENV) install

.PHONY: dev.build
dev.build: .env
	$(PIPENV) install --dev

.PHONY: dev.lock
dev.lock:
	$(PIPENV) lock --dev
	make dev.build

.PHONY: test
test:
	.venv/bin/pytest pansen


.PHONY: dev.run
dev.run:
	.venv/bin/pansen_castlabs


.PHONY: clean
clean: pyc-clean
	rm -rf \
		.env \
		"$(VENV)" \
		.mypy_cache \
		./*".egg-info"

.PHONY: pyc-clean
pyc-clean:
	@find ./ -type d -name __pycache__ | xargs -P 20 rm -rf
	@find ./ -name '*.pyc'             | xargs -P 20 rm -rf

