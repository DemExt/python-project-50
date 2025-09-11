def format_yaml(diff_tree, depth=0):
    """
    Рекурсивно форматирует diff_tree в YAML-подобный текст с плюсами и минусами.
    """
    lines = []
    indent = '  ' * depth
    for node in diff_tree:
        key = node['key']
        status = node['status']
        if status == 'nested':
            lines.append(f"{indent}  {key}:")
            lines.append(format_yaml(node['children'], depth + 2))
        elif status == 'added':
            value = to_str(node['value'], depth + 1)
            lines.append(f"{indent}+ {key}: {value}")
        elif status == 'deleted':
            value = to_str(node['value'], depth + 1)
            lines.append(f"{indent}- {key}: {value}")
        elif status == 'unchanged':
            value = to_str(node['value'], depth + 1)
            lines.append(f"{indent}  {key}: {value}")
        elif status == 'modified':
            old_value = to_str(node['old_value'], depth + 1)
            new_value = to_str(node['new_value'], depth + 1)
            lines.append(f"{indent}- {key}: {old_value}")
            lines.append(f"{indent}+ {key}: {new_value}")
    return '\n'.join(lines)


def to_str(value, depth):
    """
    Преобразует значение в строку с учетом вложенности.
    Если значение — словарь, форматирует его с отступами.
    """
    if isinstance(value, dict):
        lines = []
        indent = '  ' * depth
        for k, v in value.items():
            lines.append(f"{indent}{k}: {to_str(v, depth + 1)}")
        return '\n' + '\n'.join(lines)
    elif isinstance(value, bool):
        return str(value).lower()
    elif value is None:
        return 'null'
    else:
        return str(value)