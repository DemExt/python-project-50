import os
import tempfile
import unittest
import yaml

from gendiff.scripts.generate_diff import generate_diff


def compare_yml_files(file1_path, file2_path):
    def load_yml_or_empty(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                return {}
            return yaml.safe_load(content)
    data1 = load_yml_or_empty(file1_path)
    data2 = load_yml_or_empty(file2_path)
    return data1 == data2


class TestGenerateDiff(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.file1_path = os.path.join(self.temp_dir.name, "file1.yml")
        self.file2_path = os.path.join(self.temp_dir.name, "file2.yml")

        # Данные для теста формата stylish (словарь)
        self.content1_stylish = {
            'key1': 'value1',
            'key2': 'value2',
            'key3': {
                'subkey1': 'subvalue1'
            }
        }
        self.content2_stylish = {
            'key1': 'value1',
            'key2': 'changed_value',
            'key3': {
                'subkey1': 'subvalue1',
                'subkey2': 'subvalue2'
            },
            'key4': 'value4'
        }

        # Данные для теста формата plain (строка)
        self.content1_plain = {
            'host': 'hexlet.io',
            'timeout': 50,
            'proxy': '123.234.53.22',
            'follow': False
        }
        self.content2_plain = {
            'timeout': 20,
            'verbose': True,
            'host': 'hexlet.io'
        }

        # Записываем в файлы для stylish теста
        with open(self.file1_path, 'w', encoding='utf-8') as f:
            yaml.dump(self.content1_stylish, f)
        with open(self.file2_path, 'w', encoding='utf-8') as f:
            yaml.dump(self.content2_stylish, f)

    def tearDown(self):
        self.temp_dir.cleanup()

    '''def test_generate_diff_stylish(self):
        # Получаем словарь из generate_diff
        diff_dict = generate_diff(self.file1_path, self.file2_path, format_name='stylish')

        # Сохраняем результат во временный файл
        temp_output_path = os.path.join(self.temp_dir.name, "output.yml")
        with open(temp_output_path, 'w', encoding='utf-8') as f:
            yaml.dump(diff_dict, f)

        # Сравниваем содержимое file2.yml и output.yml
        self.assertTrue(compare_yml_files(self.file2_path, temp_output_path))'''

    def test_generate_diff_plain(self):
        # Перезаписываем файлы для plain теста
        with open(self.file1_path, 'w', encoding='utf-8') as f:
            yaml.dump(self.content1_plain, f)
        with open(self.file2_path, 'w', encoding='utf-8') as f:
            yaml.dump(self.content2_plain, f)

        expected_plain = (
            "Property 'follow' was removed\n"
            "Property 'proxy' was removed\n"
            "Property 'timeout' was updated. From 50 to 20\n"
            "Property 'verbose' was added with value: true"
        )
        result = generate_diff(self.file1_path, self.file2_path, format_name='plain')
        self.assertEqual(result.strip(), expected_plain.strip())


if __name__ == '__main__':
    unittest.main()