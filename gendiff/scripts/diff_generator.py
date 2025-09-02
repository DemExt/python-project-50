import json
import os

import yaml


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