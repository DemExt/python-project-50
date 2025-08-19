import argparse
import json
import os
import yaml

def read_file(filepath):
    _, ext = os.path.splitext(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        if ext == '.json':
            return json.load(f)
        elif ext in ['.yml', '.yaml']:
            return yaml.safe_load(f)
        else:
            raise ValueError(f"Unsupported file extension: {ext}")

def get_keys(data1, data2):
    return sorted(set(data1.keys() or {}) | set(data2.keys() or {}))

def build_diff(data1, data2):
    diff = []

    all_keys = get_keys(data1 or {}, data2 or {})

    for key in all_keys:
        val1 = data1.get(key) if data1 else None
        val2 = data2.get(key) if data2 else None

        if key not in data1:
            diff.append({'key': key, 'status': 'added', 'value': val2})
        elif key not in data2:
            diff.append({'key': key, 'status': 'removed', 'value': val1})
        else:
            if val1 == val2:
                diff.append({'key': key, 'status': 'unchanged', 'value': val1})
            else:
                diff.append({'key': key, 'status': 'changed', 'old_value': val1, 'new_value': val2})
    return diff

def format_stylish(diff_lines):
    result = ['{']
    result.extend(diff_lines)
    result.append('}')
    return '\n'.join(result)

def format_plain(diff):
    lines = []
    for change in diff:
        key = change['key']
        status = change['status']
        if status == 'added':
            lines.append(f"  + {key}: {format_value(change['value'])}")
        elif status == 'removed':
            lines.append(f"  - {key}: {format_value(change['value'])}")
        elif status == 'changed':
            lines.append(f"  - {key}: {format_value(change['old_value'])}")
            lines.append(f"  + {key}: {format_value(change['new_value'])}")
        # unchanged не выводим
    return '\n'.join(lines)

def format_json(diff):
    return json.dumps(diff, indent=4)

def format_value(value):
    if isinstance(value, dict):
        # Можно оставить как есть или форматировать по желанию
        return json.dumps(value)
    elif isinstance(value, bool):
        return str(value).lower()
    elif value is None:
        return 'null'
    else:
        return str(value)

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
        # Форматируем в стильный вывод
        diff_lines = []
        for item in diff:
            key = item['key']
            status = item['status']
            if status == 'added':
                diff_lines.append(f"  + {key}: {format_value(item['value'])}")
            elif status == 'removed':
                diff_lines.append(f"  - {key}: {format_value(item['value'])}")
            elif status == 'unchanged':
                diff_lines.append(f"      {key}: {format_value(item['value'])}")
            elif status == 'changed':
                diff_lines.append(f"  - {key}: {format_value(item['old_value'])}")
                diff_lines.append(f"  + {key}: {format_value(item['new_value'])}")
        
        print(format_stylish(diff_lines))
    
    elif args.format == 'plain':
        print(format_plain(diff))
    
    elif args.format == 'json':
        print(format_json(diff))


if __name__ == '__main__':
    main()
