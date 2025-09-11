import json
import yaml

def read_file(file_path):
    with open(file_path) as f:
        if file_path.endswith('.json'):
            return json.load(f)
        elif file_path.endswith(('.yaml', '.yml')):
            return yaml.safe_load(f)
        else:
            raise Exception('Unsupported format')
    

def get_all_keys(dict1, dict2):
    return sorted(set(dict1.keys()) | set(dict2.keys()))


def build_diff(dict1, dict2, all_keys):
    diff = []
    all_keys = get_all_keys(dict1, dict2)

    for key in all_keys:
        if key not in dict1:
            val = dict2[key]
            diff.append({
                'name': key,
                'action': 'added',
                'new_value': val
            })
        elif key not in dict2:
            val = dict1[key]
            diff.append({
                'name': key,
                'action': 'deleted',
                'old_value': val
            })
        else:
            val1 = dict1[key]
            val2 = dict2[key]
            if isinstance(val1, dict) and isinstance(val2, dict):
                children = build_diff(val1, val2, all_keys)
                diff.append({
                    'name': key,
                    'action': 'nested',
                    'children': children
                })
            elif val1 != val2:
                diff.append({
                    'name': key,
                    'action': 'modified',
                    'old_value': val1,
                    'new_value': val2
                })
            else:
                diff.append({
                    'name': key,
                    'action': 'unchanged',
                    'value': val1
                })
    return diff