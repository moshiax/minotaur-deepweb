import requests

def filter_connected_ips(file_path, approved_file_path):
    with open(file_path, 'r') as file:
        connected_ips = file.read().splitlines()

    approved_ips = []

    for ip in connected_ips:
        keyword_found = is_filtered_content(ip)
        if keyword_found:
            print(f"Добавляем сайт {ip} в approved.txt (содержит ключевое слово: {keyword_found})")
            approved_ips.append(f"{ip} ({keyword_found})")

    with open(approved_file_path, 'w') as approved_file:
        approved_file.write('\n'.join(approved_ips))

def is_filtered_content(ip):
    try:
        response = requests.get(f'http://{ip}', timeout=1)
        content = response.text.lower()  # Преобразование к нижнему регистру
        for keyword in ["audio", "video", "loli", "porn", "hentai", "порно", "child", "цп", "file", "archive", "zip", "rar", "exe", "audio", "mp3", "mp4", "png", "jpg", "porno", "sex"]:
            if keyword in content:
                return keyword
        return None
    except requests.RequestException:
        return None

if __name__ == "__main__":
    connected_ips_file = 'connected_ips.txt'
    approved_ips_file = 'approved.txt'
    filter_connected_ips(connected_ips_file, approved_ips_file)
