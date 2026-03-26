import psutil
import time

def get_cpu_usage():
    cpu_usage = psutil.cpu_percent(interval=1)
    return cpu_usage

def get_memory_usage():
    memory_usage = psutil.virtual_memory().percent
    return memory_usage

def get_disk_usage():
    disk_usage = psutil.disk_usage('/').percent
    return disk_usage

def main():
    while True:
        cpu = get_cpu_usage()
        memory = get_memory_usage()
        disk = get_disk_usage()

        print(f'\nЗагрузка CPU: {cpu}%')
        print(f'Использованная оперативная память: {memory}%')
        print(f'Загруженность диска (/): {disk}%')
        print('-' * 40)
        time.sleep(5)


if __name__ == '__main__':
    main()

