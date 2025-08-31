import argparse

from diff_builder import build_diff
from diff_generator import (
    format_json,
    format_plain,
    # build_diff,
    format_stylish,
    read_file,
)


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

    diff = build_diff(data1 or {}, data2 or {})

    if args.format == 'stylish':
        print(format_stylish(diff))
    elif args.format == 'plain':
        print(format_plain(diff))
    elif args.format == 'json':
        print(format_json(diff))


if __name__ == '__main__':
    main()