# Реалізувати наступне URL
#* 127.0.0.1:5000/whoami
#  * Повертає браузер клієнта
#  * IP клієнта
#  * Поточний час на сервері


from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

@app.route('/whoami')
def whoami():

    client_ip = request.remote_addr

    client_browser = request.user_agent.string

    server_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    response = {
        "client_ip": client_ip,
        "client_browser": client_browser,
        "server_time": server_time
    }

    return response

if __name__ == '__main__':

    app.run(host='127.0.0.1', port=5000)
