dirs = siaskynet/ tests/

build:
	python -m compileall ./siaskynet

install:
	python -m pip install pipenv
	pipenv install --dev

lint:
	flake8 $(dirs) --count --show-source --statistics --per-file-ignores='__init__.py:F401'
	pylint $(dirs) -d invalid-name,protected-access,dangerous-default-value

test:
	pytest
