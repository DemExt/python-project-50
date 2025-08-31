install:
		uv sync

package-install:
		uv tool install dist/*.whl		

check:
	ruff check

lint:
	ruff check