import os
import socket
import random
import struct
import time
import requests
import traceback

def generate_random_ip():
    return socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))

def is_valid_ip(ip):
    try:
        socket.getaddrinfo(ip, None)
        return True
    except socket.error:
        return False

def get_website_title(ip):
    try:
        response = requests.get(f'http://{ip}', timeout=1)
        if '<title>' in response.text and '</title>' in response.text:
            return response.text.split('<title>')[1].split('</title>')[0]
        else:
            return "Title not found"
    except requests.RequestException as e:
        return None

def try_connect(ip, port=80, timeout=1):
    skip_filename = 'skip.txt'
    try:
        with open(skip_filename, 'a+') as skip_file:
            skip_list = skip_file.read().splitlines()

            if ip in skip_list:
                print(f"Пропускаем {ip}, так как он присутствует в {skip_filename}")
                return

            try:
                with socket.create_connection((ip, port), timeout=timeout):
                    website_title = get_website_title(ip)
                    if website_title is not None:
                        print(f"Успешное подключение - Заголовок сайта: {website_title}")
                        with open('connected_ips.txt', 'a') as file:
                            file.write(f"{ip}:{port} - {website_title}\n")
            except socket.timeout:
                print(f"Timeout при подключении")
                skip_file.write(f"{ip}\n")
            except ConnectionRefusedError:
                print(f"Соединение отклонено")
                skip_file.write(f"{ip}\n")
            except OSError as e:
                print(f"Не удалось подключиться: {e}")
                skip_file.write(f"{ip}\n")
            except Exception as ex:
                print(f"Unexpected error: {ex}")
                with open('error.txt', 'a') as error_file:
                    error_file.write(f"Unexpected error connecting: {ex}\n")
                traceback.print_exc(file=open('error.txt', 'a'))

    except IOError as e:
        print(f"IOError: {e}")
        with open('error.txt', 'a') as error_file:
            error_file.write(f"IOError: {e}\n")

def read_calculation_count():
    try:
        count_file_path = os.path.join('templates', 'calculation_count.txt')
        with open(count_file_path, 'r', encoding='utf-8') as count_file:
            count_str = count_file.read().strip()
            return int(count_str) if count_str else 0
    except FileNotFoundError:
        return 0

def update_calculation_count(count):
    try:
        count_file_path = os.path.join('templates', 'calculation_count.txt')
        with open(count_file_path, 'w', encoding='utf-8') as count_file:
            count_file.write(str(count))
    except Exception as ex:
        print(f"Error updating calculation count: {ex}")

if __name__ == "__main__":
    while True:
        try:
            random_ip = generate_random_ip()
            if is_valid_ip(random_ip):
                # Обновление номера вычислений
                calculation_count = read_calculation_count() + 1
                update_calculation_count(calculation_count)

                try_connect(random_ip)

        except Exception as ex:
            print(f"Exception: {ex}")
            with open('error.txt', 'a', encoding='utf-8') as error_file:
                error_file.write(f"Unexpected error: {ex}\n")
            traceback.print_exc(file=open('error.txt', 'a'))
        time.sleep(0.1)