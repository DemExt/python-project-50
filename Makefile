install:
		uv sync

build:
		uv build

package-install:
		uv tool install dist/*.whl		

check:
	pip install --quiet --upgrade ruff	
	ruff check

lint:
	pip install --quiet --upgrade ruff
	ruff check