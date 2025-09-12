import argparse  # точка входа, только argparse и вызов главной функции

from gendiff.scripts.diff_builder import build_diff, get_all_keys, read_file

from ..formatters.json import format_diff_json
from ..formatters.plain import format_plain
from ..formatters.stylish import format_diff_stylish


def main():
    parser = argparse.ArgumentParser(description='Генератор диффов')
    parser.add_argument('first_file', help='Первый файл для сравнения')
    parser.add_argument('second_file', help='Второй файл для сравнения')
    parser.add_argument(
        '-f', '--format',
        dest='format',
        default='stylish',
        choices=['stylish', 'plain', 'json'],
        help='выберите формат вывода'
    )

    args = parser.parse_args()

    data1 = read_file(args.first_file)
    data2 = read_file(args.second_file)

    all_keys = get_all_keys(data1, data2)

    diff = build_diff(data1 or {}, data2 or {}, all_keys)

    if args.format == 'stylish':
        print(format_diff_stylish(diff))
    elif args.format == 'plain':
        print(format_plain(diff))
    elif args.format == 'json':
        print(format_diff_json(diff))


if __name__ == '__main__':
    main()