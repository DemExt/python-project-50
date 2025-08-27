def build_diff(dict1, dict2):
    diff = []

    all_keys = sorted(set(dict1.keys()) | set(dict2.keys()))
    for key in all_keys:
        if key not in dict1:
            # свойство добавлено
            val = dict2[key]
            diff.append({
                'key': key,
                'status': 'added',
                'value': '[complex value]' if isinstance(val, dict) else val
            })
        elif key not in dict2:
            # свойство удалено
            diff.append({
                'key': key,
                'status': 'removed'
            })
        else:
            val1 = dict1[key]
            val2 = dict2[key]
            if isinstance(val1, dict) and isinstance(val2, dict):
                # сравниваем вложенные словари
                children = build_diff(val1, val2)
                diff.append({
                    'key': key,
                    'status': 'nested',
                    'children': children
                })
            elif val1 != val2:
                old_value = '[complex value]' if isinstance(val1, dict) else val1
                new_value = '[complex value]' if isinstance(val2, dict) else val2
                diff.append({
                    'key': key,
                    'status': 'changed',
                    'old_value': old_value,
                    'new_value': new_value
                })
    return diff