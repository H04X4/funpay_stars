from bs4 import BeautifulSoup
import json
import aiohttp
from datetime import datetime
from datetime import datetime

headers = {
    "accept": "*/*",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "x-requested-with": "XMLHttpRequest"
}

async def refund(order_id):
    from SETTINGS import PROXY
    from main import Data

    data_instance = Data()
    with open("data.json", 'r') as f:
        data_dict = json.load(f)
        data_instance = Data()
        data_instance.__dict__.update(data_dict)

    payload = {
        "id": order_id,
        "csrf_token": data_instance.csrf_token
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(f"https://funpay.com/orders/refund", headers={**data_instance.headers, **headers}, proxy=PROXY, data=payload) as resp:
            json_response = await resp.json()
            print(json_response)

async def get_order_status(order_id: str):
    from SETTINGS import PROXY
    from main import Data

    data_instance = Data()
    with open("data.json", 'r') as f:
        data_dict = json.load(f)
        data_instance = Data()
        data_instance.__dict__.update(data_dict)
    async with aiohttp.ClientSession() as session:
        async with session.post(f"https://funpay.com/orders/{order_id}", headers={**data_instance.headers, **headers}, proxy=PROXY) as resp:
            reader = resp.content
            data = await reader.read()
            html_response = data.decode('utf-8')
    parser = BeautifulSoup(html_response, "lxml")

    if (span := parser.find("span", {"class": "text-warning"})) and span.text in (
            "Возврат", "Повернення", "Refund"):
        status = False
    elif (span := parser.find("span", {"class": "text-success"})) and span.text in ("Закрыт", "Закрито", "Closed"):
        status = False
    else:
        status = True

    return status

async def get_chat_by_username(user):
    from SETTINGS import PROXY
    from main import Data

    data_instance = Data()
    with open("data.json", 'r') as f:
        data_dict = json.load(f)
        data_instance = Data()
        data_instance.__dict__.update(data_dict)

    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://funpay.com/chat/", headers={**data_instance.headers, **headers}, proxy=PROXY) as resp:
            reader = resp.content
            data = await reader.read()
            html_response = data.decode('utf-8')
    soup = BeautifulSoup(html_response, 'html.parser')
    for a in soup.find_all('a', class_='contact-item'):
        link = a['href'].split('node=')[1]
        username = a.find('div', class_='media-user-name').text.strip()
        if username == user:
            return link

async def send_message(username, text):
    from SETTINGS import PROXY
    from main import Data

    data_instance = Data()
    with open("data.json", 'r') as f:
        data_dict = json.load(f)
        data_instance = Data()
        data_instance.__dict__.update(data_dict)

    chat_id = await get_chat_by_username(username)

    leave_as_unread = False
    request = {
        "action": "chat_message",
        "data": {"node": chat_id, "last_message": -1, "content": text}
    }
    objects = [
        {
            "type": "chat_node",
            "id": chat_id,
            "tag": "00000000",
            "data": {"node": chat_id, "last_message": -1, "content": ""}
        }
    ]
    payload = {
        "objects": json.dumps(objects),
        "request": json.dumps(request),
        "csrf_token": data_instance.csrf_token
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(f"https://funpay.com/runner/", headers={**data_instance.headers, **headers}, proxy=PROXY, data=payload) as resp:
            json_response = await resp.json()

async def __parse_messages(json_messages: dict):
    messages = []

    for i in json_messages:
        author_id = i["author"]
        parser = BeautifulSoup(i["html"].replace("<br>", "\n"), "lxml")

        if author_id == 0:
            message_text = parser.find("div", role="alert").text.strip()
        else:
            message_text = parser.find("div", {"class": "chat-msg-text"}).text

        messages.append(message_text)

    return messages

async def get_chat_history(username):
    from SETTINGS import PROXY
    from main import Data

    data_instance = Data()
    with open("data.json", 'r') as f:
        data_dict = json.load(f)
        data_instance = Data()
        data_instance.__dict__.update(data_dict)

    chat_id = await get_chat_by_username(username)

    payload = {
        "node": chat_id,
        "last_message": 99999999999999999999999
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(f"https://funpay.com/chat/history?node={chat_id}&last_message=99999999999999999999999", headers={**data_instance.headers, **headers}, proxy=PROXY, data=payload) as resp:
            json_response = await resp.json()

    return await __parse_messages(json_response["chat"]["messages"])

async def get_lot(num):
    from SETTINGS import PROXY
    from main import Data

    data_instance = Data()
    with open("data.json", 'r') as f:
        data_dict = json.load(f)
        data_instance = Data()
        data_instance.__dict__.update(data_dict)

    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://funpay.com/lots/offer?id={num}", proxy=PROXY) as resp:
            reader = resp.content
            data = await reader.read()
            html_response = data.decode('utf-8')
            lot = float(html_response.split('<option value="0" class="hidden" data-content="&lt;span class=&quot;payment&quot;&gt;&lt;span class=&quot;payment-title&quot;&gt;Не выбран&lt;/span&gt;&lt;span class=&quot;payment-value&quot;&gt;от ')[1].split(' ₽&lt;')[0].replace(" ", ""))
    parser = BeautifulSoup(html_response, "lxml")
    for param_item in parser.find_all("div", class_="param-item"):
        if param_name := param_item.find("h5"):
            if param_name.text in ("Подробное описание", "Докладний опис", "Detailed description"):
                detailed_description = param_item.find("div").text
    name = html_response.split('<div class="col-xs-6"><div class="param-item"><h5>Количество Stars</h5><div class="text-bold">')[1].split('</div>')[0]
    return lot, detailed_description, name

async def update_lot(offer_node, offer_id, name, detailed_description, price_min):
    from main import Data

    data_instance = Data()
    with open("data.json", 'r') as f:
        data_dict = json.load(f)
        data_instance = Data()
        data_instance.__dict__.update(data_dict)
    now = datetime.now()
    from SETTINGS import PROXY
    data = {
        "csrf_token": data_instance.csrf_token,
        "form_created_at": int(now.timestamp()),
        "offer_id": offer_id,
        "node_id": offer_node,
        "location": "offer",
        "deleted": "",
        "fields[quantity]": detailed_description,
        "fields[desc][ru]": name,
        "fields[desc][en]": "",
        "fields[payment_msg][ru]": "",
        "fields[payment_msg][en]": "",
        "fields[images]": "",
        "price": float(str(price_min).replace(",", ".")) * 0.909 - 0.03,
        "active": "on",
        "deactivate_after_sale": ""
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(f"https://funpay.com/lots/offerSave", data=data, headers=data_instance.headers, proxy=PROXY) as resp:
            r = resp.text