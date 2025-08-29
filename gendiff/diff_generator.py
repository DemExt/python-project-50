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
    return sorted(set((data1 or {}).keys()) | set((data2 or {}).keys()))

def build_diff(data1, data2):
    diff = []

    all_keys = get_keys(data1, data2)

    for key in all_keys:
        val1 = data1.get(key) if data1 else None
        val2 = data2.get(key) if data2 else None

        if key not in data1:
            diff.append({'key': key, 'status': 'added', 'value': val2})
        elif key not in data2:
            diff.append({'key': key, 'status': 'removed', 'value': val1})
        else:
            # Обработка вложенных словарей
            if isinstance(val1, dict) and isinstance(val2, dict):
                nested_diff = build_diff(val1, val2)
                diff.append({'key': key, 'status': 'nested', 'children': nested_diff})
            elif val1 == val2:
                diff.append({'key': key, 'status': 'unchanged', 'value': val1})
            else:
                diff.append({'key': key, 'status': 'changed', 'old_value': val1, 'new_value': val2})
    return diff

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