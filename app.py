from flask import Flask, render_template, request

app = Flask(__name__)

def read_connected_ips():

    with open('connected_ips.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        ips_data = [line.strip().split(' - ') for line in lines if ' - ' in line]
    return ips_data

@app.route('/')
def home():
    ips_data = read_connected_ips()
    return render_template('index.html', ips_data=ips_data)

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query').lower()
    ips_data = read_connected_ips()


    search_results = [ip_data for ip_data in ips_data if len(ip_data) == 2 and (query in ip_data[0].lower() or query in ip_data[1].lower())]

    return render_template('search_result.html', query=query, search_results=search_results)

if __name__ == '__main__':
    app.run()
