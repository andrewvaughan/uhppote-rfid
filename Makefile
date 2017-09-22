dependencies:
	pip install -r requirements.txt

lint-docstring: dependencies
	python setup.py lint_docstring

lint: dependencies lint-docstring
	python setup.py lint

test: clean-pyc dependencies lint
	python -m unittest discover

coverage: clean-pyc dependencies lint
	coverage run --source uhppote_rfid test
	coverage html

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f  {} +

clean: clean-pyc
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info

.PHONY : dependencies lint-docstring lint test coverage clean-pyc clean
