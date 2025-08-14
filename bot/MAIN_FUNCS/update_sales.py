import aiohttp
from main import *
from bs4 import BeautifulSoup
import aiosqlite

headers = {
    "accept": "*/*",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "x-requested-with": "XMLHttpRequest"
}

async def get_sales():
    from SETTINGS import PROXY
    from bot.main import give_stars
    from main import Data

    data_instance = Data()
    with open("data.json", 'r') as f:
        data_dict = json.load(f)
        data_instance = Data()
        data_instance.__dict__.update(data_dict)

    async with aiohttp.ClientSession() as session:
        while True:
            await asyncio.sleep(15)
            async with session.get(f"https://funpay.com/orders/trade", headers={**data_instance.headers, **headers}, proxy=PROXY) as resp:
                reader = resp.content
                data = await reader.read()
                html_response = data.decode('utf-8')

            parser = BeautifulSoup(html_response, "lxml")

            next_order_id = parser.find("input", {"type": "hidden", "name": "continue"})
            next_order_id = next_order_id.get("value") if next_order_id else None

            order_divs = parser.find_all("a", {"class": "tc-item"})

            sales = []
            for div in order_divs:
                classname = div.get("class")
                if "info" in classname:
                    order_date_text = div.find("div", {"class": "tc-date-time"}).text
                    if any(today in order_date_text for today in ("сегодня", "сьогодні", "today")):
                        async with aiosqlite.connect('db.db') as db:
                            i = await db.execute("SELECT completed FROM orders")
                            abc = await i.fetchall()
                        
                        order_id = div.find("div", {"class": "tc-order"}).text[1:]
                        if order_id not in str(abc):
                            async with aiosqlite.connect('db.db') as db:
                                await db.execute('''
                                    INSERT INTO orders (completed)
                                    VALUES (?)
                                ''', (order_id, ))
                                await db.commit()

                            description = div.find("div", {"class": "order-desc"}).find("div").text
                            
                            buyer_div = div.find("div", {"class": "media-user-name"}).find("span")
                            buyer_username = buyer_div.text

                            print("НАЙДЕН НОВЫЙ ЗАКАЗ!!!")
                            task = asyncio.create_task(give_stars(order_id, description, buyer_username))

async def update_on_startup():
    from SETTINGS import PROXY
    from main import Data

    data_instance = Data()
    with open("data.json", 'r') as f:
        data_dict = json.load(f)
        data_instance = Data()
        data_instance.__dict__.update(data_dict)

    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://funpay.com/orders/trade", headers={**data_instance.headers, **headers}, proxy=PROXY) as resp:
            reader = resp.content
            data = await reader.read()
            html_response = data.decode('utf-8')

        parser = BeautifulSoup(html_response, "lxml")

        next_order_id = parser.find("input", {"type": "hidden", "name": "continue"})
        next_order_id = next_order_id.get("value") if next_order_id else None

        order_divs = parser.find_all("a", {"class": "tc-item"})

        for div in order_divs:
            classname = div.get("class")
            if "info" in classname:
                order_date_text = div.find("div", {"class": "tc-date-time"}).text
                if any(today in order_date_text for today in ("сегодня", "сьогодні", "today")):
                    async with aiosqlite.connect('db.db') as db:
                        i = await db.execute("SELECT completed FROM orders")
                        abc = await i.fetchall()
                    
                    order_id = div.find("div", {"class": "tc-order"}).text[1:]
                    if order_id not in str(abc):
                        async with aiosqlite.connect('db.db') as db:
                            await db.execute('''
                                INSERT INTO orders (completed)
                                VALUES (?)
                            ''', (order_id, ))
                            await db.commit()
                        print(f"Добавил старый ордер в бд: {order_id}")