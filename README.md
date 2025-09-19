### Hexlet tests and linter status:
[![Actions Status](https://github.com/DemExt/python-project-50/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/DemExt/python-project-50/actions)

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=DemExt_python-project-50&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=DemExt_python-project-50)

[![SonarQube Cloud](https://sonarcloud.io/images/project_badges/sonarcloud-light.svg)](https://sonarcloud.io/summary/new_code?id=DemExt_python-project-50)

[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=DemExt_python-project-50&metric=coverage)](https://sonarcloud.io/summary/new_code?id=DemExt_python-project-50)

Difference Calculator (gendiff)

gendiff is a command-line tool for finding differences between files. This is the second project developed as part of the Hexlet course.

Supported File Formats

- JSON (.json)

- YAML (.yaml, .yml)

Usage

Place the files you want to compare inside the tests/test_data directory.
Run the following command, replacing file1 and file2 with your actual file names:
uv run gendiff tests/test_data/<file1> tests/test_data/<file2>
By default, the output is formatted using the stylish formatter.
To use a different format (json or plain), specify it with the -f flag:

Пример вывода инструмента при использовании разных форматтеров:

Default (stylish) formatter:
uv run gendiff tests/test_data/<file1> tests/test_data/<file1>
Using the JSON formatter:
uv run gendiff -f stylish tests/test_data/<file1> tests/test_data/<file1>
Using the Plain formatter:
uv run gendiff -f plain tests/test_data/<file1> tests/test_data/<file1>

Development and Testing

Linting

Run ruff to check for linting issues:

make lint
Running Tests

make test-coverage

демонстрация в процессе написания кода:

https://asciinema.org/a/cprV1s5mllyvz9D7HOyGcAXg6

https://asciinema.org/a/y0XB0UucIeMvBW6zPOeN58tj2

 https://asciinema.org/a/3RZIPviEJR8C3nyriDRtGs7tL