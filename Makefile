install:
		uv sync

build:
		uv build

package-install:
		uv tool install dist/*.whl		

check:
	ruff check

lint:
	ruff check