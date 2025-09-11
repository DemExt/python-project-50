from .format import format_value

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
                    lines.append(f"Property '{current_path}' was removed. Old value: {value_str}")
                else:
                    lines.append(f"Property '{current_path}' was removed")
            elif status == 'modified':
                old_val = format_value(node['old_value'])
                new_val = format_value(node['new_value'])
                lines.append(f"Property '{current_path}' was updated. From {old_val} to {new_val}")
                
    recurse(node_list)
    return '\n'.join(lines)