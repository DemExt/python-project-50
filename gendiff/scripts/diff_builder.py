def get_all_keys(dict1, dict2):
    return sorted(set(dict1.keys()) | set(dict2.keys()))


def build_diff(dict1, dict2):
    diff = []
    all_keys = get_all_keys(dict1, dict2)

    for key in all_keys:
        if key not in dict1:
            val = dict2[key]
            diff.append({
                'action': 'added',
                'name': key,
                'new_value': val
            })
        elif key not in dict2:
            val = dict1[key]
            diff.append({
                'action': 'deleted',
                'name': key,
                'old_value': val
            })
        else:
            val1 = dict1[key]
            val2 = dict2[key]
            if isinstance(val1, dict) and isinstance(val2, dict):
                children = build_diff(val1, val2)  # ключи вычисляются заново для вложенных словарей
                diff.append({
                    'action': 'nested',
                    'name': key,
                    'children': children
                })
            elif val1 != val2:
                diff.append({
                    'action': 'modified',
                    'name': key,
                    'new_value': val2,
                    'old_value': val1
                })
            else:
                diff.append({
                    'action': 'unchanged',
                    'name': key,
                    'value': val1
                })
    return diff