import requests

api_url = 'https://api.github.com'

def get_user_profile(username):
    try:
        url = f'{api_url}/users/{username}'
        response = requests.get(url)
        if response.status_code != 200:
            print(f'Ошибка получения профиля: {response.status_code}')
            return
    except requests.exceptions.RequestException as error:
        print(f'Ошибка соединения или HTTP: {error}')
        return
    except ValueError:
        print('Ошибка при разборе JSON')
        return

    data = response.json()
    profile_info = {
        'name': data.get('name'),
        'html_url': data.get('html_url'),
        'public_repos': data.get('public_repos'),
        'public_gists': data.get('public_gists'),
        'followers': data.get('followers'),
        'following': data.get('following')
    }
    print('Профиль пользователя:')
    for key, value in profile_info.items():
        print(f'{key}: {value}')

def get_user_repositories(username):
    repositories = []
    page = 1
    while True:
        url = f'{api_url}/users/{username}/repos?per_page=100&page={page}'
        try:
            response = requests.get(url)
            if response.status_code != 200:
                print(f'Ошибка получения репозиториев: {response.status_code}')
                return
            data = response.json()
            if not data:
                break
            for repository in data:
                repository_info = {
                    'name': repository.get('name'),
                    'html_url': repository.get('html_url'),
                    'watchers_count': repository.get('watchers_count'),
                    'language': repository.get('language'),
                    'private': repository.get('private'),
                    'default_branch': repository.get('default_branch')
                }
                repositories.append(repository_info)
            page += 1
        except requests.exceptions.RequestException as error:
            print(f'Ошибка соединения или HTTP: {error}')
            return
        except ValueError:
            print('Ошибка при разборе JSON')
            return

    print(f'Все репозитории пользователя {username}:')
    for repository in repositories:
        print(f"\nНазвание: {repository['name']}")
        print(f"Ссылка: {repository['html_url']}")
        print(f"Просмотры: {repository['watchers_count']}")
        print(f"Язык: {repository['language']}")
        print(f"Видимость: {'приватный' if repository['private'] else 'публичный'}")
        print(f"Ветка по умолчанию: {repository['default_branch']}")

def search_repositories(request):
    url = f'{api_url}/search/repositories?q={request}&per_page=10'
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f'Ошибка поиска репозиториев: {response.status_code}')
            return
        data = response.json()
        total_count = data.get('total_count', 0)
        print(f'Найдено репозиториев: {total_count}')
        for item in data.get('items', []):
            print(f"\nНазвание: {item['name']}")
            print(f"Ссылка: {item['html_url']}")
            print(f"Описание: {item.get('description')}")
            print(f"Язык: {item.get('language')}")
            print(f"Владелец: {item['owner']['login']}")

    except requests.exceptions.RequestException as error:
        print(f'Ошибка соединения или HTTP: {error}')
        return
    except ValueError:
        print('Ошибка при разборе JSON')
        return

def main():
    username = input('Введите имя пользователя GitHub: ')
    print('\n----- Просмотр профиля -----')
    get_user_profile(username)
    print('\n----- Получение репозиториев -----')
    get_user_repositories(username)
    request = input('\nВведите название репозитория для поиска: ')
    print('\n----- Поиск репозиториев -----')
    search_repositories(request)


if __name__ == '__main__':
    main()

