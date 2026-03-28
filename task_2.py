import requests
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from io import BytesIO

def get_random_cat():
    try:
        url_cat = "https://api.thecatapi.com/v1/images/search"
        response = requests.get(url_cat, timeout=10)
        if response.status_code == 200:
            data = response.json()
            image_url = data[0]['url']
            image_response = requests.get(image_url)
            if image_response.status_code == 200:
                image_data = image_response.content
                image = Image.open(BytesIO(image_data))
                image.thumbnail((500, 400), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                label_image.config(image=photo)
                label_image.image = photo
                label_caption.config(text="Кот")

    except requests.exceptions.Timeout:
        messagebox.showerror("Ошибка", "Превышено время ожидания")
    except Exception as error:
        messagebox.showerror("Ошибка", f"Не удалось получить кота:\n{error}")

def get_random_dog():
    try:
        url_dog = "https://dog.ceo/api/breeds/image/random"
        response = requests.get(url_dog, timeout=10)
        if response.status_code == 200:
            data = response.json()
            image_url = data['message']
            image_response = requests.get(image_url)
            if image_response.status_code == 200:
                image_data = image_response.content
                image = Image.open(BytesIO(image_data))
                image.thumbnail((500, 400), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                label_image.config(image=photo)
                label_image.image = photo
                label_caption.config(text="Собака")

    except requests.exceptions.Timeout:
        messagebox.showerror("Ошибка", "Превышено время ожидания")
    except Exception as error:
        messagebox.showerror("Ошибка", f"Не удалось получить собаку:\n{error}")


root = tk.Tk()
root.title("Случайные фотографии котов и собак")
root.geometry("800x600")

frame = tk.Frame(root)
frame.grid(row=0, column=0, pady=10)

random_cat = ttk.Button(frame, text="Получить кота", command=get_random_cat)
random_cat.grid(column=0, row=0, padx=10, ipady=5, ipadx=5)

random_dog = ttk.Button(frame, text="Получить собаку", command=get_random_dog)
random_dog.grid(column=1, row=0, padx=10, ipady=5, ipadx=5)

label_image = tk.Label(root)
label_image.grid(row=1, column=0, pady=10)

label_caption = tk.Label(root, text="", font=("Times New Roman", 14))
label_caption.grid(row=2, column=0, pady=5)

root.grid_columnconfigure(0, weight=1)

root.mainloop()


