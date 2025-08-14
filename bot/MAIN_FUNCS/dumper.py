import asyncio
import json

async def dumper():
    from FunpayAPI.funtions import get_lot
    from FunpayAPI.funtions import update_lot
    while True:
        with open("dump.json", 'r') as f:
            data_dict = json.load(f)
        for item in data_dict:
            if item["value"] != "-":
                price_min = 99999
                for num in item["nums"]:
                    try:
                        lot, detailed_description00, name00 = await get_lot(num)
                        print(f"[{name00}] Спарсил лот {num}: {lot}")
                        await asyncio.sleep(4)
                    except Exception as e:
                        lot = 6666
                    if lot < price_min:
                        price_min = lot
                try:
                    my_price, name, detailed_description = await get_lot(item['value'])
                except Exception as e:
                    pass
                else:
                    await asyncio.sleep(2)
                    await update_lot(2418, item["value"], name, detailed_description, price_min)
                    print(f"[{detailed_description}] Обновил цену {item['value']}: {my_price} -> {float(str(price_min - 0.03).replace(',', '.'))}")
        await asyncio.sleep(60)