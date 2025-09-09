import json
import os

import yaml


def read_file(filepath):
    _, ext = os.path.splitext(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        if ext == '.json':
            return json.load(f)
        elif ext in ['.yml', '.yaml']:
            return yaml.safe_load(f)
        elif ext == '.txt':
            return f.read()
        else:
            raise ValueError(f"Unsupported file extension: {ext}")