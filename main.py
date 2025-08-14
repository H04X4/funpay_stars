import asyncio
from SETTINGS import *
from bot.initialisation import main00
from bot.get_csrf import get_csrf_token
import json

def save_data(data_instance, filename):
    with open(filename, 'w') as f:
        json.dump(data_instance.__dict__, f)

class Data():
    def __init__(self):
        self.headers = {}
        self.csrf_token = ""
        self.id00 = ""
        self.username = ""
        self.orders = []
        self.chats = []

if __name__ == "__main__":
    print('Софт инициализируется...')
    data_instance = Data()
    data_instance.headers, data_instance.csrf_token, data_instance.id00, data_instance.username = get_csrf_token()
    save_data(data_instance, 'data.json')

    print(f"Получил csrf_token: {data_instance.csrf_token}, ID: {data_instance.id00}, USERNAME: {data_instance.username}")
    asyncio.run(main00())