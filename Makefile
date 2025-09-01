install:
		uv sync

build:
		uv build

package-install:
		uv tool install dist/*.whl		

check:
	pip install --quiet --upgrade ruff	
	ruff check

test-coverage:
	pip install --quiet --upgrade pytest pytest-cov pyyaml
	uv run pytest --cov=gendiff --cov-report xml

lint:
	pip install --quiet --upgrade ruff
	ruff check