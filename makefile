HOST=127.0.0.1
TEST_PATH=./

lint:
	pycodestyle Api/ --exclude=.tox

test:
	pytest --cov=Api Api/tests

run:
	python run.py
