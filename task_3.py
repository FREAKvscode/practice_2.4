import requests
import json
import os

url = 'https://www.cbr-xml-daily.ru/daily_json.js'
save_file = 'save.json'
groups = {}

def load_groups():
    global groups
    if os.path.exists(save_file):
        with open(save_file, 'r', encoding='utf-8') as f:
            groups = json.load(f)
    else:
        groups = {}

def save_groups():
    with open(save_file, 'w', encoding='utf-8') as f:
        json.dump(groups, f, ensure_ascii=False, indent=4)

def get_currency_data():
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Ошибка при получении данных")
        return None

def show_all_currencies():
    data = get_currency_data()
    if data:
        print("Курс всех валют:")
        for valute_code, info in data['Valute'].items():
            print(f"{info['CharCode']}: {info['Name']} - {info['Value']} руб")

def get_currency_by_code(code):
    data = get_currency_data()
    if data:
        currency = data['Valute']
        if code in currency:
            info = currency[code]
            print(f"{info['CharCode']}: {info['Name']} - {info['Value']} руб")
        else:
            print("Код валюты не найден")

def create_group(name):
    if name not in groups:
        groups[name] = []
        print(f"Группа '{name}' создана")
        save_groups()
    else:
        print("Такая группа уже существует")

def show_groups():
    if not groups:
        print("Нет созданных групп")
    else:
        print("Существующие группы:")
        for name, currencies in groups.items():
            print(f"{name}: {', '.join(currencies) if currencies else 'Пусто'}")

def add_currency_to_group(group_name, currency_code):
    if group_name in groups:
        data = get_currency_data()
        if data and currency_code in data['Valute']:
            if currency_code not in groups[group_name]:
                groups[group_name].append(currency_code)
                print(f"{currency_code} добавлена в группу '{group_name}'")
                save_groups()
            else:
                print("Валюта уже есть в группе")
        else:
            print("Код валюты не найден")
    else:
        print("Группа не найдена")

def remove_currency_from_group(group_name, currency_code):
    if group_name in groups:
        if currency_code in groups[group_name]:
            groups[group_name].remove(currency_code)
            print(f"{currency_code} удалена из группы '{group_name}'")
            save_groups()
        else:
            print("Валюта не найдена в группе")
    else:
        print("Группа не найдена")

def main():
    load_groups()
    while True:
        print("\nМеню:")
        print("1. Просмотреть текущий курс всех валют")
        print("2. Посмотреть курс валюты по коду")
        print("3. Создать группу валют")
        print("4. Посмотреть все группы")
        print("5. Добавить валюту в группу")
        print("6. Удалить валюту из группы")
        print("0. Выйти")
        choice = input("Выберите действие: ")

        if choice == '1':
            show_all_currencies()
        elif choice == '2':
            code = input("Введите код валюты (например, USD): ").upper()
            get_currency_by_code(code)
        elif choice == '3':
            name = input("Введите название новой группы: ")
            create_group(name)
        elif choice == '4':
            show_groups()
        elif choice == '5':
            group_name = input("Введите название группы: ")
            code = input("Введите код валюты для добавления: ").upper()
            add_currency_to_group(group_name, code)
        elif choice == '6':
            group_name = input("Введите название группы: ")
            code = input("Введите код валюты для удаления: ").upper()
            remove_currency_from_group(group_name, code)
        elif choice == '0':
            print("Выход")
            break
        else:
            print("Некорректный выбор, попробуйте снова")

if __name__ == '__main__':
    main()

