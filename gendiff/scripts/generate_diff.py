import json
import os

import yaml

from .diff_builder import build_diff, get_all_keys


def get_data(file_path):
    with open(file_path) as f:
        content = f.read()
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.json':
        data = json.loads(content)
    elif ext in ('.yml', '.yaml'):
        data = yaml.safe_load(content)
    else:
        raise ValueError(f'Unsupported file extension: {ext}')
    
    if not isinstance(data, dict):
        raise TypeError(f"Parsed data from {file_path} is not a dictionary, got {type(data)}")
    return data


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
            # если есть какие-то другие статусы
            raise ValueError(f'Unknown status in diff tree: {status}')
    return result


def generate_diff(file_path1, file_path2, format_name='stylish'):
    data1 = get_data(file_path1)
    data2 = get_data(file_path2)
    all_keys = get_all_keys(data1, data2)
    diff_tree = build_diff(data1, data2, all_keys)

    if format_name == 'json':
        obj = tree_to_obj(diff_tree)
        return json.dumps(obj, indent=4)
    elif format_name == 'stylish':
        from gendiff.formatters import stylish as stylish_formatter
        return stylish_formatter.format_stylish(diff_tree)
    elif format_name == 'plain':
        from gendiff.formatters import plain as plain_formatter
        return plain_formatter.format_plain(diff_tree)
    elif format_name in ('yml', 'yaml'):
        from gendiff.formatters import yaml as yaml_formatter
        return yaml_formatter.format_yaml(diff_tree)
    else:
        raise ValueError(f'Unknown format: {format_name}')


def format_value(value):
    if isinstance(value, dict):
        return '[complex value]'
    elif isinstance(value, bool):
        return str(value).lower()
    elif value is None:
        return 'null'
    elif isinstance(value, str):
        return f"'{value}'"
    else:
        return str(value)


def format_stylish(diff, depth=0):
    lines = []
    indent = "  " * depth
    for item in diff:
        key = item['key']
        status = item['status']
        if status == 'nested':
            lines.append(f"{indent}  {key}: {format_stylish(item['children'], depth + 1)}")
        elif status == 'added':
            value = item.get('value', '')
            lines.append(f"{indent}+ {key}: {format_value(value)}")
        elif status == 'removed':
            value = item.get('value', '')
            lines.append(f"{indent}- {key}: {format_value(value)}")
        elif status == 'unchanged':
            value = item.get('value', '')
            lines.append(f"{indent}  {key}: {format_value(value)}")
        elif status == 'changed':
            old_value = item.get('old_value', '')
            new_value = item.get('new_value', '')
            lines.append(f"{indent}- {key}: {format_value(old_value)}")
            lines.append(f"{indent}+ {key}: {format_value(new_value)}")
    # Обертка в фигурные скобки с правильными отступами
    opening_brace = '{'
    closing_brace = indent + '}'
    if depth == 0:
        return opening_brace + '\n' + '\n'.join(lines) + '\n' + closing_brace
    else:
        return '{\n' + '\n'.join(lines) + '\n' + indent + '}'
    

def format_plain(diff):
    lines = []

    def recurse(nodes, path=''):
        for node in nodes:
            key = node['key']
            status = node['status']
            current_path = f"{path}.{key}" if path else key

            if status == 'nested':
                recurse(node['children'], current_path)
            elif status == 'added':
                value_str = format_value(node['value'])
                lines.append(f"Property '{current_path}' was added with value: {value_str}")
            elif status == 'removed':
                lines.append(f"Property '{current_path}' was removed")
            elif status == 'changed':
                old_val = format_value(node['old_value'])
                new_val = format_value(node['new_value'])
                lines.append(f"Property '{current_path}' was updated. From {old_val} to {new_val}")

    recurse(diff)
    return '\n'.join(lines)


def format_json(diff):
    return json.dumps(diff, indent=4)