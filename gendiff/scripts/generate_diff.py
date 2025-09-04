import json
import os
import yaml
from .diff_builder import build_diff

def get_data(file_path):
    with open(file_path) as f:
        content = f.read()
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.json':
        return json.loads(content)
    elif ext in ('.yml', '.yaml'):
        return yaml.safe_load(content)
    raise ValueError(f'Unsupported file extension: {ext}')

def tree_to_obj(diff_tree):
    """
    Преобразует diff_tree (список узлов) в вложенный словарь
    вида { key: { status: ..., value/old_value/new_value/children: ... }, ... }
    """
    result = {}
    for node in diff_tree:
        key = node['key']
        status = node['status']

        if status == 'nested':
            result[key] = {
                'status': 'nested',
                'children': tree_to_obj(node['children'])
            }
        elif status == 'changed':
            result[key] = {
                'status': 'changed',
                'old_value': node['old_value'],
                'new_value': node['new_value']
            }
        elif status == 'added':
            result[key] = {
                'status': 'added',
                'value': node['value']
            }
        elif status == 'removed':
            result[key] = {
                'status': 'removed',
                'value': node['value']
            }
        elif status == 'unchanged':
            result[key] = {
                'status': 'unchanged',
                'value': node['value']
            }
        else:
            # если у вас ещё есть какие-то статусы
            raise ValueError(f'Unknown status in diff tree: {status}')
    return result

def generate_diff(file_path1, file_path2, format_name='stylish'):
    data1 = get_data(file_path1)
    data2 = get_data(file_path2)
    all_keys = set(data1.keys()) | set(data2.keys())
    diff_tree = build_diff(data1, data2, all_keys)

    # Для форматов 'json' и 'stylish' (так ожидают ваши тесты) —
    # отдаём именно JSON-объект с indent=4
    if format_name in ('json', 'stylish'):
        obj = tree_to_obj(diff_tree)
        return json.dumps(obj, indent=4)
    elif format_name == 'plain':
        from gendiff.formatters import plain as plain_formatter
        return plain_formatter.format_plain(diff_tree)
    else:
        raise ValueError(f'Unknown format: {format_name}')