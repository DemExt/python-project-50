def main():
    import argparse
    parser = argparse.ArgumentParser(
        description='Генератор диффов'
    )
    
    parser.add_argument('first_file', help='Первый файл для сравнения')
    parser.add_argument('second_file', help='Второй файл для сравнения')
    parser.add_argument(
        '-f', '--format',
        dest='format',
        default='stylish',
        help='set format of output'
    )

    args = parser.parse_args()

    print("Файлы:", args.first_file, args.second_file)
    print("Формат вывода:", args.format)

if __name__ == '__main__':
    main()