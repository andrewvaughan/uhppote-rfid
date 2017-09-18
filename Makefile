dependencies:
	pip install -r requirements.txt

lint: dependencies
	python setup.py lint

test: dependencies lint
	python -m unittest discover

coverage: dependencies lint
	coverage run --source uhppote_rfid test
	coverage html

.PHONY : dependencies lint test coverage
