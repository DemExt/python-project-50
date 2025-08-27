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

def format_plain(node_list):
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

    recurse(node_list)
    return '\n'.join(lines)