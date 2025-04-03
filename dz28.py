from fastapi import FastAPI, Request
from datetime import datetime
import random
import string
import os

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Привіт! Це головна сторінка FastAPI."}


@app.get("/whoami")
def whoami(request: Request):
    client_ip = request.client.host
    client_browser = request.headers.get("user-agent")
    server_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return {
        "client_ip": client_ip,
        "client_browser": client_browser,
        "server_time": server_time,
    }


@app.get("/source_code")
def source_code():
    script_path = os.path.abspath(__file__)

    with open(script_path, "r") as file:
        code = file.read()

    return f'<pre style="background-color: #f4f4f4; padding: 10px; font-family: monospace;">{code}</pre>'


@app.get("/random")
def generate_random_string(length: int = 8, specials: int = 0, digits: int = 0):
    if not (1 <= length <= 100):
        return {"error": "length must be between 1 and 100"}
    if specials not in [0, 1]:
        return {"error": "specials must be 0 or 1"}
    if digits not in [0, 1]:
        return {"error": "digits must be 0 or 1"}

    characters = string.ascii_letters

    if digits:
        characters += string.digits
    if specials:
        characters += '!"№;%:?*()_+'

    random_string = "".join(random.choices(characters, k=length))

    return {"random_string": random_string}