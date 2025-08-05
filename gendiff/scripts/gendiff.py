def main():
    import argparse
    parser = argparse.ArgumentParser(
        description='Генератор диффов'
    )
    parser.add_argument('files', nargs='*', help='Файлы для сравнения')
    args = parser.parse_args()

   
    print("Запущен gendiff с файлами:", args.files)