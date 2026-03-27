import psutil
import tkinter as tk
from tkinter import scrolledtext, ttk

auto_update = False

def clear_result_text():
    result_text.delete('1.0', tk.END)

def get_cpu_usage():
    cpu_usage = psutil.cpu_percent(interval=1)
    result_text.insert(tk.END, f'Загрузка CPU: {cpu_usage}%\n')

def get_memory_usage():
    memory_usage = psutil.virtual_memory().percent
    result_text.insert(tk.END, f'Использованная оперативная память: {memory_usage}%\n')

def get_disk_usage():
    disk_usage = psutil.disk_usage('/').percent
    result_text.insert(tk.END, f'Загруженность диска (/): {disk_usage}%\n')

def all_usage():
    global auto_update
    if not auto_update:
        auto_update = True
        check_button_all.config(state='disabled')
        check_button_stop.config(state='normal')
        start_auto_update()

def start_auto_update():
    global auto_update
    if auto_update:
        clear_result_text()
        get_cpu_usage()
        get_memory_usage()
        get_disk_usage()
        root.after(1000, start_auto_update)

def stop_auto_update():
    global auto_update
    auto_update = False
    check_button_all.config(state='normal')
    check_button_stop.config(state='disabled')


root = tk.Tk()
root.title('Системный монитор')
root.geometry('800x600')

check_button_cpu = ttk.Button(root, text='Мониторинг загрузки CPU', command=get_cpu_usage)
check_button_cpu.pack(padx=10, pady=5, anchor='center', ipady=5, ipadx=5)

check_button_memory = ttk.Button(root, text='Мониторинг использованной оперативной памяти', command=get_memory_usage)
check_button_memory.pack(padx=10, pady=5, anchor='center', ipady=5, ipadx=5)

check_button_disk = ttk.Button(root, text='Процентное соотношение загруженности диска', command=get_disk_usage)
check_button_disk.pack(padx=10, pady=5, anchor='center', ipady=5, ipadx=5)

check_button_all = ttk.Button(root, text='Автоматическое обновление', command=all_usage)
check_button_all.pack(padx=10, pady=5, anchor='center', ipady=5, ipadx=5)

check_button_stop = ttk.Button(root, text='Остановить автоматическое обновление', command=stop_auto_update)
check_button_stop.pack(padx=10, pady=5, anchor='center', ipady=5, ipadx=5)
check_button_stop.config(state='disabled')

result_text = scrolledtext.ScrolledText(root, width=100, height=20)
result_text.pack(padx=10, pady=10)

root.mainloop()


