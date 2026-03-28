import requests
import tkinter as tk
from tkinter import messagebox, ttk
from io import BytesIO
from PIL import Image, ImageTk

api_key = '9c6d9545427ecb4adbcaee4dad0da408'

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_icon(icon_code):
    url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
    response = requests.get(url)
    if response.status_code == 200:
        image_data = response.content
        image = Image.open(BytesIO(image_data))
        return ImageTk.PhotoImage(image)
    return None

def show_weather():
    city = city_entry.get()
    data = get_weather(city)
    if data:
        temperature = data['main']['temp']
        weather_icon_code = data['weather'][0]['icon']
        icon_image = get_icon(weather_icon_code)

        temperature_label.config(text=f"Температура: {temperature}°C")
        if icon_image:
            weather_icon.config(image=icon_image)
            weather_icon.image = icon_image
        else:
            weather_icon.config(image='')
        city_label.config(text=f"Погода в {city}")
    else:
        messagebox.showerror("Ошибка", "Город не найден или произошла ошибка при запросе.")


root = tk.Tk()
root.title("Погода в городе")
root.geometry("600x400")

city_entry = ttk.Entry(root)
city_entry.pack(pady=10)
city_entry.insert(0, "Москва")

button = ttk.Button(root, text="Показать погоду", command=show_weather)
button.pack(ipadx=5, ipady=5)

city_label = ttk.Label(root, text="")
city_label.pack()

temperature_label = ttk.Label(root, text="")
temperature_label.pack()

weather_icon = ttk.Label(root)
weather_icon.pack()

root.mainloop()


