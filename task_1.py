import requests

urls = [
    'https://github.com/',
    'https://www.binance.com/en',
    'https://tomtit.tomsk.ru/',
    'https://jsonplaceholder.typicode.com/',
    'https://moodle.tomtit-tomsk.ru/'
]

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

        print(f'{url} – {status} – {status_code}')

    except requests.exceptions.Timeout:
        print(f'{url} – нет ответа')

    except requests.exceptions.RequestException as error:
        print(f'{url} – ошибка - {error}')

