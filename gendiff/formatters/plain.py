def format_value(value):
    if isinstance(value, (dict, list)):
        return '[complex value]'
    elif value is None:
        return 'null'
    elif isinstance(value, bool):
        return str(value).lower()
    elif isinstance(value, str):
        return f"'{value}'"
    else:
        return str(value)


def format_plain(node_list):
    lines = []

    def recurse(nodes, path=''):
        for node in nodes:
            key = node['name']
            status = node['action']
            current_path = f"{path}.{key}" if path else key

            if status == 'nested':
                recurse(node['children'], current_path)
            elif status == 'added':
                # Используем 'new_value'
                value_str = format_value(node['new_value'])
                lines.append(f"Property '{current_path}' was added with value: {value_str}")
            elif status == 'deleted':
                # Возможно, есть 'old_value'
                old_value = node.get('old_value')
                if old_value is not None:
                    value_str = format_value(old_value)
                    lines.append(f"Property '{current_path}' was removed")
                else:
                    lines.append(f"Property '{current_path}' was removed")
            elif status == 'modified':
                new_val = format_value(node['new_value'])
                old_val = format_value(node['old_value'])
                lines.append(f"Property '{current_path}' was updated. From {old_val} to {new_val}")
                
    recurse(node_list)
    return '\n'.join(lines)