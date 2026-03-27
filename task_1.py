import requests
import tkinter as tk
from tkinter import scrolledtext, ttk

urls = [
    'https://github.com/',
    'https://www.binance.com/en',
    'https://tomtit.tomsk.ru/',
    'https://jsonplaceholder.typicode.com/',
    'https://moodle.tomtit-tomsk.ru/'
]

def check_urls():
    result_text.delete('1.0', tk.END)
    for url in urls:
        try:
            response = requests.get(url, timeout=20)
            status_code = response.status_code

            if 200 <= status_code < 300:
                status = 'успешно'
            elif 300 <= status_code < 400:
                status = 'перенаправление'
            elif 400 <= status_code < 500:
                status = 'ошибка клиента'
            elif 500 <= status_code < 600:
                status = 'ошибка сервера'
            else:
                status = 'неизвестный статус'

            result_text.insert(tk.END, f'{url} – {status} – {status_code}\n')

        except requests.exceptions.Timeout:
            result_text.insert(tk.END, f'{url} – нет ответа\n')
        except requests.exceptions.RequestException as error:
            result_text.insert(tk.END, f'{url} – ошибка - {error}\n')

root = tk.Tk()
root.title("Проверка статуса URL")
root.geometry("600x400")

check_button = ttk.Button(root, text="Проверить URL", command=check_urls)
check_button.pack(pady=10)

result_text = scrolledtext.ScrolledText(root, width=80, height=20)
result_text.pack(padx=10, pady=10)

root.mainloop()

