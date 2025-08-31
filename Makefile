install:
		uv sync

package-install:
		uv tool install dist/*.whl		

check:
	uv run ruff check

lint:
	uv run ruff check