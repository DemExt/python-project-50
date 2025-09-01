import os
import tempfile
import unittest

import yaml

from gendiff.generate_diff import generate_diff


def compare_yml_files(file_path1, file_path2):
    def load_yml_or_empty(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                return {}
            return yaml.safe_load(content)
    try:
        data1 = load_yml_or_empty(file_path1)
        data2 = load_yml_or_empty(file_path2)
    except yaml.YAMLError:
        raise
    return data1 == data2


class TestCompareYmlFiles(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.file1_path = os.path.join(self.temp_dir.name, "file.yml")
        self.file2_path = os.path.join(self.temp_dir.name, "file2.yml")
        self.file3_path = os.path.join(self.temp_dir.name, "file3.yml")
        self.file_empty1 = os.path.join(self.temp_dir.name, "empty1.yml")
        self.file_empty2 = os.path.join(self.temp_dir.name, "empty2.yml")
        self.file_invalid = os.path.join(self.temp_dir.name, "invalid.yml")
        self.file_valid = os.path.join(self.temp_dir.name, "valid.yml")
        self.file_yaml1 = os.path.join(self.temp_dir.name, "yaml1.yml")
        self.file_yaml_diff = os.path.join(self.temp_dir.name, "yaml2.yml")

        # Создаем файлы с содержимым
        content = {"name": "Alice", "age": 30}
        with open(self.file1_path, 'w', encoding='utf-8') as f:
            yaml.dump(content, f)
        with open(self.file2_path, 'w', encoding='utf-8') as f:
            yaml.dump(content, f)

        content_diff = {"name": "Bob", "age": 25}
        with open(self.file3_path, 'w', encoding='utf-8') as f:
            yaml.dump(content_diff, f)

        # Пустые файлы
        with open(self.file_empty1, 'w', encoding='utf-8') as f:
            pass
        with open(self.file_empty2, 'w', encoding='utf-8') as f:
            pass

        # Некорректный YAML (невалидный)
        with open(self.file_invalid, 'w', encoding='utf-8') as f:
            f.write("!!! this is not valid yaml !!!")  # Гарантированно вызовет ошибку при парсинге

        # Корректный YAML для сравнения
        with open(self.file_valid, 'w', encoding='utf-8') as f:
            yaml.dump({"key": "value"}, f)

        # YAML файлы для теста generate_diff
        with open(self.file_yaml1, 'w', encoding='utf-8') as f:
            yaml.dump({"name": "Alice", "age": 30}, f)
        with open(self.file_yaml_diff, 'w', encoding='utf-8') as f:
            yaml.dump({"name": "Bob", "age": 25}, f)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_compare_identical_files(self):
        result = compare_yml_files(self.file1_path, self.file2_path)
        self.assertTrue(result)

    def test_compare_different_files(self):
        result = compare_yml_files(self.file1_path, self.file3_path)
        self.assertFalse(result)

    def test_compare_with_empty_files(self):
        result = compare_yml_files(self.file_empty1, self.file_empty2)
        self.assertTrue(result)

    def test_compare_with_invalid_yml_raises_exception(self):
        with self.assertRaises(yaml.YAMLError):
            compare_yml_files(self.file_invalid, self.file_valid)

    def test_generate_diff_yaml_stylish(self):
        # Предположим, что стиль по умолчанию — stylish
        expected_output = """{
  - name: Alice
  - age: 30
  + name: Bob
  + age: 25
}"""
        result = generate_diff(self.file_yaml1, self.file_yaml_diff, format_name='stylish')
        self.assertEqual(result.strip(), expected_output)

    def test_generate_diff_yaml_plain(self):
        expected_output = (
            "Property 'name' was updated. From 'Alice' to 'Bob'\n"
            "Property 'age' was updated. From 30 to 25"
        )
        result = generate_diff(self.file_yaml1, self.file_yaml_diff, format_name='plain')
        self.assertEqual(result.strip(), expected_output)


if __name__ == '__main__':
    unittest.main()