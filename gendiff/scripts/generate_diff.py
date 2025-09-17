import json

from gendiff.scripts.parser import read_file

from .diff_builder import build_diff


def generate_diff(file_path1, file_path2, formatter='stylish'):
    data1 = read_file(file_path1)
    data2 = read_file(file_path2)
    diff_tree = build_diff(data1, data2)

    if formatter == 'json':
        return json.dumps(diff_tree, indent=4)
    elif formatter == 'stylish':
        from gendiff.formatters import stylish as stylish_formatter
        return stylish_formatter.format_diff_stylish(diff_tree)
    elif formatter == 'plain':
        from gendiff.formatters import plain as plain_formatter
        return plain_formatter.format_plain(diff_tree)
    elif formatter in ('yml', 'yaml'):
        from gendiff.formatters import yaml as yaml_formatter
        return yaml_formatter.format_yaml(diff_tree)
    else:
        raise ValueError(f'Unknown format: {formatter}')