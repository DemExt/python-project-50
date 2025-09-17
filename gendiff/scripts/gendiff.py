import argparse  # точка входа, только argparse и вызов главной функции

from gendiff.scripts.generate_diff import generate_diff


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
    
    file_path1 = args.first_file
    file_path2 = args.second_file

    result = generate_diff(file_path1, file_path2, formatter=args.format)
    print(result)


if __name__ == '__main__':
    main()