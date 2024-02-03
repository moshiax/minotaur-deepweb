import requests

def filter_connected_ips(file_path, approved_file_path):
    with open(file_path, 'r') as file:
        connected_ips = file.read().splitlines()

    approved_data = []

    for ip in connected_ips:
        title = get_page_title(ip)
        if title:
            print(f"Добавляем сайт {ip} в approved.txt с заголовком: {title}")
            approved_data.append(f"{ip} - {title}")

    with open(approved_file_path, 'w') as approved_file:
        approved_file.write('\n'.join(approved_data))

def get_page_title(ip):
    try:
        response = requests.get(f'http://{ip}', timeout=1)
        title_start = response.text.find('<title>') + len('<title>')
        title_end = response.text.find('</title>', title_start)
        title = response.text[title_start:title_end].strip()
        return title
    except requests.RequestException:
        return None

if __name__ == "__main__":
    connected_ips_file = 'connected_ips.txt'
    approved_ips_file = 'approved.txt'
    filter_connected_ips(connected_ips_file, approved_ips_file)