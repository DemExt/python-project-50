# import pytest
import json
import os
import tempfile
import unittest

from gendiff.generate_diff import generate_diff


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

        # Создаем файлы с содержимым
        content = {"name": "Alice", "age": 30}
        with open(self.file1_path, 'w', encoding='utf-8') as f:
            json.dump(content, f)
        with open(self.file2_path, 'w', encoding='utf-8') as f:
            json.dump(content, f)

        content_diff = {"name": "Bob", "age": 25}
        with open(self.file3_path, 'w', encoding='utf-8') as f:
            json.dump(content_diff, f)

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
        result = compare_json_files(self.file1_path, self.file2_path)
        self.assertTrue(result)

    def test_compare_different_files(self):
        result = compare_json_files(self.file1_path, self.file3_path)
        self.assertFalse(result)

    def test_compare_with_empty_files(self):
        result = compare_json_files(self.file_empty1, self.file_empty2)
        self.assertTrue(result)

    def test_compare_with_invalid_json_raises_exception(self):
        with self.assertRaises(json.JSONDecodeError):
            compare_json_files(self.file_invalid, self.file_valid)
            
    def test_generate_diff_json(self):
        expected_output = json.dumps({
            "name": {"old": "Alice", "new": "Bob"},
            "age": {"old": 30, "new": 25}
        }, indent=4)
        result = generate_diff(self.file1_path, self.file3_path, format_name='json')
        self.assertEqual(json.loads(result), json.loads(expected_output))


if __name__ == '__main__':
    unittest.main()