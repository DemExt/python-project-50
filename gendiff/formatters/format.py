def format_value(value, depth=0):
    indent = '    ' * depth
    if isinstance(value, dict):
        lines = []
        lines.append('{')
        for k, v in value.items():
            lines.append(f"{indent}    {k}: {format_value(v, depth + 1)}")
        lines.append(f"{indent}}}")
        return '\n'.join(lines)
    elif isinstance(value, list):
        # Например, можно вывести упрощенно
        return '[complex value]'
    elif value is None:
        return 'null'
    elif isinstance(value, bool):
        return str(value).lower()
    elif isinstance(value, str):
        # В зависимости от тестов: с кавычками или без
        
        return f"{value}"
    else:
        return str(value)