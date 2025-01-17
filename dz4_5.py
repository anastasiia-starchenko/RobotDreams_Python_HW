# Реалізувати наступне URL
# 127.0.0.1:5000/random?length=42&specials=1&digits=0
#  * Повертає випадкову стрічку довжиною в length
#  * Приймає аргументи
#    * specials – коли 1, то до рядка може бути додано спецсимволи !"№;%:?*()_+
#    * digits - коли 1, то до рядка може бути додано числа 0123456789
#  * Передбачити перевірку валідності аргументів (specials та digits 0/1, length від 1 до 100)
#  * За замовченням якщо не надано параметрів, то specials та digits 0, a lenght 8

from flask import Flask, request, jsonify
import random
import string

app = Flask(__name__)

@app.route('/random', methods=['GET'])
def generate_random_string():

    length = request.args.get('length', default=8, type=int)
    specials = request.args.get('specials', default=0, type=int)
    digits = request.args.get('digits', default=0, type=int)

    if not (1 <= length <= 100):
        return jsonify({"error": "length must be between 1 and 100"}), 400
    if specials not in [0, 1]:
        return jsonify({"error": "specials must be 0 or 1"}), 400
    if digits not in [0, 1]:
        return jsonify({"error": "digits must be 0 or 1"}), 400

    characters = string.ascii_letters

    if digits:
        characters += string.digits
    if specials:
        characters += "!\"№;%:?*()_+"

    random_string = ''.join(random.choices(characters, k=length))

    return jsonify({"random_string": random_string})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
