import json
import hashlib
from typing import List, Dict, Any

def get_object_hash(obj: Dict) -> str:
    """
    Створює хеш об'єкта на основі його вмісту використовуючи SHA-256.
    
    Args:
        obj (Dict): Об'єкт для хешування
        
    Returns:
        str: Хеш об'єкта
    """
    # Конвертуємо об'єкт в JSON рядок з відсортованими ключами
    obj_str = json.dumps(obj, sort_keys=True)
    # Створюємо хеш використовуючи SHA-256
    return hashlib.sha256(obj_str.encode('utf-8')).hexdigest()

def remove_duplicates(input_file: str, output_file: str = None):
    """
    Видаляє дублікати з JSON файлу, використовуючи хешування SHA-256.
    
    Args:
        input_file (str): Шлях до вхідного JSON файлу
        output_file (str, optional): Шлях до вихідного JSON файлу. Якщо не вказано, перезапише вхідний файл.
    """
    if output_file is None:
        output_file = input_file
    
    print(f"Читання файлу: {input_file}")
    
    try:
        # Читаємо дані з файлу
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not isinstance(data, list):
            raise ValueError("Вхідний файл повинен містити масив JSON об'єктів")
        
        initial_count = len(data)
        print(f"Початкова кількість об'єктів: {initial_count}")
        
        # Створюємо множину для зберігання унікальних об'єктів
        unique_objects = []
        seen_hashes = set()
        
        # Проходимо по всіх об'єктах
        for obj in data:
            # Створюємо хеш об'єкта
            obj_hash = get_object_hash(obj)
            
            # Якщо такого хеша ще не було, додаємо об'єкт
            if obj_hash not in seen_hashes:
                seen_hashes.add(obj_hash)
                unique_objects.append(obj)
        
        # Зберігаємо результат
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(unique_objects, f, ensure_ascii=False, indent=2)
        
        final_count = len(unique_objects)
        removed_count = initial_count - final_count
        
        print(f"Видалено дублікатів: {removed_count}")
        print(f"Залишилось унікальних об'єктів: {final_count}")
        print(f"Результат збережено в файл: {output_file}")
        
    except json.JSONDecodeError as e:
        print(f"Помилка при парсингу JSON: {str(e)}")
    except Exception as e:
        print(f"Помилка: {str(e)}")

if __name__ == "__main__":
    input_file = "merged_dataset.json"
    output_file = "merged_dataset_unique.json"  # Зберігаємо в новий файл для безпеки
    
    remove_duplicates(input_file, output_file) 