PYTHON = python3
MAIN = a_maze_ing.py
CONFIG = config.txt

.PHONY: install run debug clean lint

install:
	$(PYTHON) -m pip install flake8 mypy pydantic

run:
	$(PYTHON) $(MAIN) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

package:
	$(PYTHON) -m build
	cp dist/mazegen-*.whl .

clean:
	rm -rf __pycache__ .mypy_cache .pytest_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores \
		--ignore-missing-imports --disallow-untyped-defs \
		--check-untyped-defs
