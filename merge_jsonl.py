import json
import os
from pathlib import Path

def merge_jsonl_files(input_dir: str, output_file: str):
    """
    Об'єднує всі JSONL файли з вказаної директорії в один JSON файл.
    
    Args:
        input_dir (str): Шлях до директорії з JSONL файлами
        output_file (str): Шлях до вихідного JSON файлу
    """
    all_data = []
    input_path = Path(input_dir)
    
    # Отримуємо список всіх JSONL файлів
    jsonl_files = sorted([f for f in input_path.glob("*.jsonl")])
    
    print(f"Знайдено {len(jsonl_files)} файлів для об'єднання")
    
    # Читаємо дані з кожного файлу
    for file_path in jsonl_files:
        print(f"Обробка файлу: {file_path.name}")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:  # Пропускаємо порожні рядки
                        try:
                            data = json.loads(line)
                            all_data.append(data)
                        except json.JSONDecodeError as e:
                            print(f"Помилка при парсингу JSON в файлі {file_path.name}: {str(e)}")
                            continue
        except Exception as e:
            print(f"Помилка при читанні файлу {file_path.name}: {str(e)}")
            continue
    
    print(f"Загальна кількість об'єктів: {len(all_data)}")
    
    # Зберігаємо об'єднані дані
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, ensure_ascii=False, indent=2)
        print(f"Дані успішно збережено в файл: {output_file}")
    except Exception as e:
        print(f"Помилка при збереженні файлу: {str(e)}")

if __name__ == "__main__":
    input_directory = "zips"
    output_file = "merged_dataset.json"
    
    merge_jsonl_files(input_directory, output_file) 