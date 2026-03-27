import requests
import tkinter as tk
from tkinter import ttk, messagebox

api_url = 'https://api.github.com'

display_text = None

def get_user_profile(username):
    global display_text
    url = f'{api_url}/users/{username}'
    try:
        response = requests.get(url)
        if response.status_code != 200:
            messagebox.showerror("Ошибка", f"Не удалось получить профиль: {response.status_code}")
            return
        data = response.json()

        profile_info = {
            'name': data.get('name'),
            'profile_url': data.get('html_url'),
            'public_repos': data.get('public_repos'),
            'public_gists': data.get('public_gists'),
            'followers': data.get('followers'),
            'following': data.get('following')
        }

        info_text = (
            f"Имя: {profile_info['name']}\n"
            f"Профиль: {profile_info['profile_url']}\n"
            f"Репозитории: {profile_info['public_repos']}\n"
            f"Обсуждения: {profile_info['public_gists']}\n"
            f"Подписчики: {profile_info['followers']}\n"
            f"Подписки: {profile_info['following']}"
        )

        display_text.delete('1.0', tk.END)
        display_text.insert(tk.END, info_text)

    except requests.RequestException as error:
        messagebox.showerror("Ошибка", str(error))

def get_user_repositories(username):
    global display_text
    repositories = []
    page = 1
    while True:
        url = f'{api_url}/users/{username}/repos?per_page=100&page={page}'
        try:
            response = requests.get(url)
            if response.status_code != 200:
                messagebox.showerror("Ошибка", f"Ошибка получения репозиториев: {response.status_code}")
                return
            data = response.json()
            if not data:
                break
            for repository in data:
                repository_info = {
                    'name': repository.get('name'),
                    'html_url': repository.get('html_url'),
                    'watchers': repository.get('watchers_count'),
                    'language': repository.get('language'),
                    'private': repository.get('private'),
                    'default_branch': repository.get('default_branch')
                }
                repositories.append(repository_info)
            page += 1

        except requests.RequestException as error:
            messagebox.showerror("Ошибка", str(error))
            return
        except ValueError:
            messagebox.showerror("Ошибка", "Ошибка при разборе JSON")
            return

    if not repositories:
        display_text.delete('1.0', tk.END)
        display_text.insert(tk.END, "Репозитории не найдены.")
        return

    text = f"Репозитории пользователя:\n"
    for repository in repositories:
        text += (
            f"\nНазвание: {repository['name']}\n"
            f"Ссылка: {repository['html_url']}\n"
            f"Просмотры: {repository['watchers']}\n"
            f"Язык: {repository['language']}\n"
            f"Видимость: {'приватный' if repository['private'] else 'публичный'}\n"
            f"Ветка по умолчанию: {repository['default_branch']}\n"
        )

    display_text.delete('1.0', tk.END)
    display_text.insert(tk.END, text)

def search_repositories(query):
    global display_text
    url = f'{api_url}/search/repositories?q={query}&per_page=10'
    try:
        response = requests.get(url)
        if response.status_code != 200:
            messagebox.showerror("Ошибка", f"Ошибка поиска: {response.status_code}")
            return
        data = response.json()
        total = data.get('total_count', 0)
        items = data.get('items', [])
        text = f"Найдено репозиториев: {total}\n"
        for repo in items:
            text += (
                f"\nНазвание: {repo['name']}\n"
                f"Ссылка: {repo['html_url']}\n"
                f"Описание: {repo.get('description')}\n"
                f"Язык: {repo.get('language')}\n"
                f"Владелец: {repo['owner']['login']}\n"
            )

        display_text.delete('1.0', tk.END)
        display_text.insert(tk.END, text)

    except requests.RequestException as error:
        messagebox.showerror("Ошибка", str(error))
    except ValueError:
        messagebox.showerror("Ошибка", "Ошибка при разборе JSON")

def main():
    global display_text
    def on_show_profile():
        username = username_entry.get().strip()
        if username:
            get_user_profile(username)
        else:
            messagebox.showwarning("Внимание", "Введите имя пользователя")

    def on_show_repositories():
        username = username_entry.get().strip()
        if username:
            get_user_repositories(username)
        else:
            messagebox.showwarning("Внимание", "Введите имя пользователя")

    def on_search():
        query = search_entry.get().strip()
        if query:
            search_repositories(query)
        else:
            messagebox.showwarning("Внимание", "Введите название репозитория")

    root = tk.Tk()
    root.title("GitHub API Viewer")
    root.geometry("800x600")

    frame_top = ttk.Frame(root)
    frame_top.pack(pady=10)

    label = ttk.Label(frame_top, text="Введите имя пользователя GitHub:")
    label.pack(side=tk.LEFT, padx=5)

    username_entry = ttk.Entry(frame_top, width=30)
    username_entry.pack(side=tk.LEFT, padx=5)

    button_frame = ttk.Frame(root)
    button_frame.pack(pady=10)

    check_profile = ttk.Button(button_frame, text="Просмотр профиля", command=on_show_profile)
    check_profile.grid(row=0, column=0, padx=10, ipady=5, ipadx=5)

    list_repositories = ttk.Button(button_frame, text="Список репозиториев", command=on_show_repositories)
    list_repositories.grid(row=0, column=1, padx=10, ipady=5, ipadx=5)

    search_frame = ttk.Frame(root)
    search_frame.pack(pady=10)

    search_entry = ttk.Entry(search_frame, width=40)
    search_entry.pack(side=tk.LEFT, padx=5)

    search_repository = ttk.Button(search_frame, text="Поиск репозиториев", command=on_search)
    search_repository.pack(side=tk.LEFT, padx=5)

    display_text = tk.Text(root, wrap=tk.WORD)
    display_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    root.mainloop()


if __name__ == '__main__':
    main()


