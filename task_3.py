import requests
import json
import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

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
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            messagebox.showerror("Ошибка", "Не удалось получить данные о курсах валют")
            return None
    except Exception as error:
        messagebox.showerror("Ошибка", str(error))
        return None

def show_all_currencies():
    data = get_currency_data()
    if data:
        text = "Курс всех валют:\n"
        for valute_code, info in data['Valute'].items():
            text += f"{info['CharCode']}: {info['Name']} - {info['Value']} руб\n"
        display_text.delete('1.0', tk.END)
        display_text.insert(tk.END, text)

def show_currency_by_code():
    code = simpledialog.askstring("Введите код валюты", "Например, USD\t\t\t\t\t").upper()
    if code:
        data = get_currency_data()
        if data:
            currency = data['Valute']
            if code in currency:
                info = currency[code]
                text = f"{info['CharCode']}: {info['Name']} - {info['Value']} руб"
            else:
                text = "Код валюты не найден"
            display_text.delete('1.0', tk.END)
            display_text.insert(tk.END, text)

def create_group():
    name = simpledialog.askstring("Создать группу", "Введите название группы\t\t\t")
    if name:
        if name not in groups:
            groups[name] = []
            save_groups()
            refresh_group_list()
        else:
            messagebox.showinfo("Инфо", "Такая группа уже существует")

def show_groups():
    if not groups:
        messagebox.showinfo("Группы", "Нет созданных групп")
        return
    text = "Существующие группы:\n"
    for name, currencies in groups.items():
        text += f"{name}: {', '.join(currencies) if currencies else 'Пусто'}\n"
    display_text.delete('1.0', tk.END)
    display_text.insert(tk.END, text)

def add_currency_to_group():
    group_name = simpledialog.askstring("Добавить валюту", "Введите название группы\t\t\t\t")
    if group_name and group_name in groups:
        code = simpledialog.askstring("Добавить валюту", "Введите код валюты для добавления\t\t\t").upper()
        data = get_currency_data()
        if data and code in data['Valute']:
            if code not in groups[group_name]:
                groups[group_name].append(code)
                save_groups()
                messagebox.showinfo("Успех", f"{code} добавлена в группу '{group_name}'")
            else:
                messagebox.showinfo("Инфо", "Валюта уже есть в группе")
        else:
            messagebox.showerror("Ошибка", "Код валюты не найден")
    else:
        messagebox.showerror("Ошибка", "Группа не найдена или отменена")
    refresh_group_list()

def remove_currency_from_group():
    group_name = simpledialog.askstring("Удалить валюту", "Введите название группы\t\t\t\t")
    if group_name and group_name in groups:
        code = simpledialog.askstring("Удалить валюту", "Введите код валюты для удаления\t\t\t\t").upper()
        if code in groups[group_name]:
            groups[group_name].remove(code)
            save_groups()
            messagebox.showinfo("Успех", f"{code} удалена из группы '{group_name}'")
        else:
            messagebox.showerror("Ошибка", "Валюта не найдена в группе")
    else:
        messagebox.showerror("Ошибка", "Группа не найдена или отменена")
    refresh_group_list()

def refresh_group_list():
    group_listbox.delete(0, tk.END)
    for name in groups:
        group_listbox.insert(tk.END, name)

load_groups()

root = tk.Tk()
root.title("Курс валют")
root.geometry("800x600")

button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

all_currency = ttk.Button(button_frame, text="Все валюты", command=show_all_currencies)
all_currency.grid(row=0, column=0, padx=10, ipady=5, ipadx=5)

course_for_code = ttk.Button(button_frame, text="Курс по коду", command=show_currency_by_code)
course_for_code.grid(row=0, column=1, padx=10, ipady=5, ipadx=5)

group = ttk.Button(button_frame, text="Создать группу", command=create_group)
group.grid(row=0, column=2, padx=10, ipady=5, ipadx=5)

all_group = ttk.Button(button_frame, text="Все группы", command=show_groups)
all_group.grid(row=0, column=3, padx=10, ipady=5, ipadx=5)

add_in_group = ttk.Button(button_frame, text="Добавить в группу", command=add_currency_to_group)
add_in_group.grid(row=1, column=0, padx=10, pady=10, ipady=5, ipadx=5)

delete_from_group = ttk.Button(button_frame, text="Удалить из группы", command=remove_currency_from_group)
delete_from_group.grid(row=1, column=1, padx=10, pady=10, ipady=5, ipadx=5)

display_text = tk.Text(root, wrap=tk.WORD, height=20)
display_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

group_frame = ttk.Frame(root)
group_frame.pack(pady=10, fill=tk.X)

label = ttk.Label(group_frame, text="Группы:")
label.pack(side=tk.LEFT, padx=5)

group_listbox = tk.Listbox(group_frame, height=5)
group_listbox.pack(side=tk.LEFT, fill=tk.X, expand=True)

refresh_group_list()

root.mainloop()

