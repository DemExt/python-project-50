install:
		uv sync

package-install:
		uv tool install dist/*.whl		

lint:
	uv run ruff check