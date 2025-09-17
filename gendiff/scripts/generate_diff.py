import json
import os
import yaml

from .diff_builder import build_diff, get_all_keys
from gendiff.scripts.parser import read_file

# from ..formatters.stylish import format_stylish


#def get_data(file_path):
  #  with open(file_path) as f:
  #      content = f.read()
  #  ext = os.path.splitext(file_path)[1].lower()
  #  if ext == '.json':
  #      data = json.loads(content)
  #  elif ext in ('.yml', '.yaml'):
  #      data = yaml.safe_load(content)
   # else:
   #     raise ValueError(f'Unsupported file extension: {ext}')
    
   # if not isinstance(data, dict):
  #      raise TypeError(f"Parsed data from {file_path} is not a dictionary, got {type(data)}")
  #  return data


#def tree_to_obj(diff_tree):
    #result = []
    #for node in diff_tree:
    #    name = node['name']
    #    status = node['action']

    #    if status == 'nested':
    #        result.append({
     #           'action': 'nested',
      #          'name': name,
     #           'children': tree_to_obj(node['children'])
     #       })
     #   elif status == 'modified':
     #       result.append({
     #           'action': 'modified',
     #           'name': name,
     #           'new_value': node['new_value'],
     #           'old_value': node['old_value']
     #       })
     #   elif status == 'added':
            # в build_diff для added — существует ключ 'value'
      #      result.append({
      #          'action': 'added',
      #          'name': name,
      #          'new_value': node['new_value']
       #     })
       # elif status == 'deleted':
      #      # для deleted — ключ 'old_value', а не 'value'
      #      result.append({
      #          'action': 'deleted',
       #         'name': name,
       #         'old_value': node['old_value']
      #      })
      #  elif status == 'unchanged':
      #      # для unchanged — ключ 'value'
       #     result.append({
       #         'action': 'unchanged',
     #          'name': name,
      #          'value': node['value']
      #      })
      #  else:
     #       raise ValueError(f'Unknown status in diff tree: {status}')
   # return result


def generate_diff(file_path1, file_path2, formatter='stylish'):
    data1 = read_file(file_path1)
    data2 = read_file(file_path2)
    #all_keys = get_all_keys(data1, data2)
    diff_tree = build_diff(data1, data2)

    if formatter == 'json':
        #obj = tree_to_obj(diff_tree)
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