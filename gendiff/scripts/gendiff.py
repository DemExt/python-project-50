import argparse
import json
#import yaml не нужно
import os

def read_file(filepath):
    _, ext = os.path.splitext(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        if ext == '.json':
            return json.load(f)
        #elif ext in ['.yml', '.yaml']:
           # return yaml.safe_load(f)
        else:
            raise ValueError(f"Unsupported file extension: {ext}")

def generate_diff(data1, data2, format='stylish'):
    """
    Генерирует строку с различиями между двумя словарями.
    """
    def get_keys():
        return sorted(data1.keys() | data2.keys())

    def build_diff():
        diff_lines = []

        for key in get_keys():
            if key not in data1:
                # Ключ добавлен во второй файл
                diff_lines.append(f"  + {key}: {format_value(data2[key])}")
            elif key not in data2:
                # Ключ удалён из второго файла
                diff_lines.append(f"  - {key}: {format_value(data1[key])}")
            else:
                # Ключ есть в обоих файлах
                if data1[key] == data2[key]:
                    # Значения совпадают
                    diff_lines.append(f"    {key}: {format_value(data1[key])}")
                else:
                    # Значения отличаются
                    diff_lines.append(f"  - {key}: {format_value(data1[key])}")
                    diff_lines.append(f"  + {key}: {format_value(data2[key])}")

        return diff_lines

    def format_value(value):
        if isinstance(value, dict):
            lines = ['{']
            for k, v in value.items():
                lines.append(f"    {k}: {format_value(v)}")
            lines.append('  }')
            return '\n'.join(lines)
        elif isinstance(value, bool):
            return str(value).lower()
        elif value is None:
            return 'null'
        else:
            return str(value)

    lines = build_diff()
    result = ['{']
    result.extend(lines)
    result.append('}')
    return '\n'.join(result)


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

    #print("Файлы:", args.first_file, args.second_file)
    #print("Формат вывода:", args.format)

    data1 = read_file(args.first_file)
    data2 = read_file(args.second_file)

    diff = generate_diff(data1, data2, format=args.format)
    print(diff)
    
if __name__ == '__main__':
    main()
