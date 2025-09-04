from .format import format_value


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