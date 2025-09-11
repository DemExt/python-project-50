from .format import format_value

def format_stylish(diff, depth=0):
    lines = []
    indent = '    ' * depth
    indent_sign = '  '  # два пробела, отступ между знаком и ключом
    
    for item in diff:
        key = item['name']
        status = item['action']
        if status == 'nested':
            children = format_stylish(item['children'], depth + 1)
            lines.append(f"{indent}    {key}: {children}")
        elif status == 'added':
            value = item.get('new_value')
            lines.append(f"{indent}  + {key}: {format_value(value, depth + 1)}")
        elif status == 'deleted':
            value = item.get('old_value')
            lines.append(f"{indent}  - {key}: {format_value(value, depth + 1)}")
        elif status == 'unchanged':
            value = item.get('value')
            lines.append(f"{indent}    {key}: {format_value(value, depth + 1)}")
        elif status == 'modified':
            old_value = item.get('old_value')
            new_value = item.get('new_value')
            lines.append(f"{indent}  - {key}: {format_value(old_value, depth + 1)}")
            lines.append(f"{indent}  + {key}: {format_value(new_value, depth + 1)}")
            
    return '{\n' + '\n'.join(lines) + '\n' + indent + '}'