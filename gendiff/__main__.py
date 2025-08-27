import json
import os
from gendiff.diff_builder import build_diff
from gendiff.formatters import plain, stylish

def get_data(file_path):
    with open(file_path) as f:
        content = f.read()
        ext = os.path.splitext(file_path)[1]
        if ext == '.json':
            return json.loads(content)
        # Можно добавить поддержку yaml и других форматов при необходимости
        raise ValueError(f'Unsupported file extension: {ext}')

def generate_diff(file_path1, file_path2, format_name='stylish'):
    data1 = get_data(file_path1)
    data2 = get_data(file_path2)

    diff_tree = build_diff(data1, data2)

    if format_name == 'plain':
        from gendiff.formatters import plain as plain_formatter
        return plain_formatter.format_plain(diff_tree)
    elif format_name == 'stylish':
        from gendiff.formatters import stylish as stylish_formatter
        return stylish_formatter.format_stylish(diff_tree)
    elif format_name == 'json':
        return json.dumps(diff_tree, indent=4)
    else:
        raise ValueError(f'Unknown format: {format_name}')