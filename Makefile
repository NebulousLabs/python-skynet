dirs = siaskynet/ tests/

build:
	python -m compileall ./siaskynet

install:
	python -m pip install pipenv
	pipenv install --dev

lint:
	flake8 $(dirs)
	pylint $(dirs)

test:
	pytest
