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
	uv run pytest --cov=hexlet_python_package_50 --cov-report xml

lint:
	pip install --quiet --upgrade ruff
	ruff check