ROOT_DIR=.
SRC_DIR=src
TEST_DIR=tests
BANDIT_CFG=bandit.yml

all:
	@echo Installing required dependencies...
	@pip install -r requirements.txt
.PHONY: all

crypto:
	@python $(SRC_DIR)/main.py
.PHONY: crypto

test:
	@export PYTHONPATH=$(SRC_DIR); pytest
.PHONY: test

lint-flake8:
	@echo Lint flake8
	@flake8
.PHONY: lint-flake8

lint-isort:
	@echo Lint isort
	@isort ./ --atomic
.PHONY: lint-isort

lint-bandit:
	@echo Lint bandit
	@bandit -qr $(SRC_DIR) $(TEST_DIR) -c $(BANDIT_CFG)
.PHONY: lint-bandit

lint-pylint:
	@echo Lint pylint
	@pylint $(SRC_DIR) $(TEST_DIR)
.PHONY: lint-pylint

lint-black:
	@echo Lint black
	@black $(SRC_DIR) $(TEST_DIR)
.PHONY: lint-black

lint: \
	lint-isort \
	lint-black \
	lint-flake8 \
	lint-bandit \
	lint-pylint
