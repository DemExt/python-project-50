# import pytest
import json
import os
import tempfile
import unittest

from gendiff.scripts.generate_diff import generate_diff


def compare_json_files(file_path1, file_path2):
    def load_json_or_empty(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                # Пустой файл — считаем его равным пустому словарю
                return {}
            return json.loads(content)
    data1 = load_json_or_empty(file_path1)
    data2 = load_json_or_empty(file_path2)
    return data1 == data2


class TestCompareJsonFiles(unittest.TestCase):
    def setUp(self):
        # Создаем временные файлы для тестов
        self.temp_dir = tempfile.TemporaryDirectory()
        self.file1_path = os.path.join(self.temp_dir.name, "file1.json")
        self.file2_path = os.path.join(self.temp_dir.name, "file2.json")
        self.file3_path = os.path.join(self.temp_dir.name, "file3.json")
        self.file_empty1 = os.path.join(self.temp_dir.name, "empty1.json")
        self.file_empty2 = os.path.join(self.temp_dir.name, "empty2.json")
        self.file_invalid = os.path.join(self.temp_dir.name, "invalid.json")
        self.file_valid = os.path.join(self.temp_dir.name, "valid.json")

        data1 = {
            "common": {
                "setting1": "Value 1",
                "setting2": 200,
                "setting3": True,
                "setting6": {
                    "key": "value",
                    "doge": {
                        "wow": ""
                    }
                }
            },
            "group1": {
                "baz": "bas",
                "foo": "bar",
                "nest": {
                    "key": "value"
                }
            },
            "group2": {
                "abc": 12345,
                "deep": {
                    "id": 45
                }
            }
        }

        data2 = {
            "common": {
                "follow": False,
                "setting1": "Value 1",
                "setting3": None,
                "setting4": "blah blah",
                "setting5": {
                    "key5": "value5"
                },
                "setting6": {
                    "key": "value",
                    "ops": "vops",
                    "doge": {
                        "wow": "so much"
                    }
                }
            },
            "group1": {
                "foo": "bar",
                "baz": "bars",
                "nest": "str"
            },
            "group3": {
                "deep": {
                    "id": {
                        "number": 45
                    }
                },
                "fee": 100500
            }
        }

        with open(self.file1_path, 'w', encoding='utf-8') as f:
            json.dump(data1, f)

        with open(self.file2_path, 'w', encoding='utf-8') as f:
            json.dump(data2, f)


        # Пустые файлы
        with open(self.file_empty1, 'w', encoding='utf-8') as f:
            pass
        with open(self.file_empty2, 'w', encoding='utf-8') as f:
            pass

        # Некорректный JSON
        with open(self.file_invalid, 'w', encoding='utf-8') as f:
            f.write("{ invalid json }")
        # Корректный JSON для сравнения
        with open(self.file_valid, 'w', encoding='utf-8') as f:
            json.dump({"key": "value"}, f)

    def tearDown(self):
        # Удаляем временные файлы и директорию
        self.temp_dir.cleanup()

    def test_compare_identical_files(self):
        result = compare_json_files(self.file1_path, self.file1_path)
        self.assertTrue(result)

    def test_compare_different_files(self):
        result = compare_json_files(self.file1_path, self.file2_path)
        self.assertFalse(result)

    def test_compare_with_empty_files(self):
        result = compare_json_files(self.file_empty1, self.file_empty2)
        self.assertTrue(result)

    def test_compare_with_invalid_json_raises_exception(self):
        with self.assertRaises(json.JSONDecodeError):
            compare_json_files(self.file_invalid, self.file_valid)
            
    '''def test_generate_diff_json(self):
        expected_output = {
            "common": {
                "setting1": {
                    "status": "unchanged",
                    "value": "Value 1"
                },
                "setting2": {
                    "status": "changed",
                    "old_value": 200,
                    "new_value": 250
                },
                "setting3": {
                    "status": "unchanged",
                    "value": True
                },
                "setting6": {
                    "status": "nested",
                    "children": {
                        "doge": {
                            "status": "nested",
                            "children": {
                                "wow": {
                                    "status": "changed",
                                    "old_value": "",
                                    "new_value": "such"
                                }
                            }
                        },
                        "key": {
                            "status": "unchanged",
                            "value": "value"
                        }
                    }
                }
            },
            "group1": {
                "baz": {
                    "status": "unchanged",
                    "value": "bas"
                },
                "foo": {
                    "status": "changed",
                    "old_value": "bar",
                    "new_value": "baz"
                },
                "nest": {
                    "status": "unchanged",
                    "value": {
                        "key": "value"
                    }
                }
            },
            "group2": {
                "abc": {
                    "status": "unchanged",
                    "value": 12345
                },
                "deep": {
                    "status": "nested",
                    "children": {
                        "id": {
                            "status": "changed",
                            "old_value": 45,
                            "new_value": 50
                        }
                    }
                }
            },
            "new_group": {
                "new_prop": {
                    "status": "added",
                    "value": "new_value"
                }
            }
        }
        result = generate_diff(self.file1_path, self.file2_path)
        diff = json.loads(result)
        # Если diff имеет структуру {'status': ..., 'children': {...}}
        self.assertEqual(diff, expected_output)'''


if __name__ == '__main__':
    unittest.main()