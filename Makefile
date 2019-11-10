TEST_CMD = python3 tests
CHECKSTYLE_CMD = flake8
PYTHON = python

all: checkstyle test main
	
test:
	$(TEST_CMD).py

flake8:
	pip install flake8

checkstyle: flake8
	$(CHECKSTYLE_CMD) *.py

clean:
	rm -f *.pyc
	rm -rf __pycache__

main:
	$(PYTHON) main.py

help: 
	@echo "all - runs all the commands including checkstyle, test and the algorithm"
	@echo "clean - remove Python file artifacts"
	@echo "checkstyle - check style with flake8"
	@echo "test - run all the test"
	@echo "main - run the main algorithm"

