# Реалізувати наступне URL
#* 127.0.0.1:5000/source_code
#  * Повертає код вашого апплікейшну

from flask import Flask, send_file
import os

app = Flask(__name__)

@app.route('/source_code')
def source_code():

    script_path = os.path.abspath(__file__)


    with open(script_path, 'r') as file:
        code = file.read()

    return f'<pre>{code}</pre>'

if __name__ == '__main__':

    app.run(host='127.0.0.1', port=5000)
