import base64
import random
import time
import httpx
import asyncio
import json
import logging
from nacl import signing
from tonsdk.utils import to_nano
from tonsdk.boc import Cell
from tonsdk.contract.wallet import WalletV4ContractR2
from tonsdk.provider import ToncenterClient
from tonutils.client import TonapiClient
from tonutils.wallet import WalletV4R2,WalletV5R1
# Настраиваем логирование
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def get_cookies():
    return {
      

    'stel_ssid': '00fe1e1452e5088216_1062226016582018372',
    'stel_dt': '-300',
    'stel_ton_token': 'U6UbdvxOSpJCXtyNjjqOfw-3LybhBTGAYaLzAgNZpMPpTlcqX8Blc9JlT9V6xb2WpSPqH92f4WKNvw4JME0TrIG_S4jQM03hmC_OcPtLtar9d_u6o1ifYqzRZYCwYGMRDmwD-9bFzyu0rfJPYjaxeuCGNji3mlE0ytRWSV_LgsuWFPtevP9cqXi_AuALN6hf07szpv4Z',
    'stel_token': 'd32974e2f7ecd362b49ad27f7f6db772d32974f9d3297d3a8f4021dadb2fe1a0782ce',
}

async def fetch_recipient():
    """Первый запрос: ищем recipient"""
    url = "https://fragment.com/api?hash=4d28250dc2105d832b"
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": "https://fragment.com",
        "referer": "https://fragment.com/stars/buy?quantity=50",
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "x-requested-with": "XMLHttpRequest"
    }
    data = {
        "query": "h04x4",
        "quantity": "",
        "method": "searchStarsRecipient"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, cookies=get_cookies(), data=data)
        if response.status_code == 200:
            try:
                json_data = response.json()
                logging.info(f"HTTP Response: {json_data}")  # Логируем весь ответ
                recipient = json_data.get("found", {}).get("recipient")  # Исправленный доступ к recipient
                logging.info(f"Получен recipient: {recipient}")
                return recipient
            except json.JSONDecodeError:
                logging.error("Ошибка парсинга JSON в первом запросе")
                return None
        else:
            logging.error(f"Ошибка первого запроса: {response.status_code}")
            return None

async def fetch_req_id(recipient):
    """Второй запрос: получаем req_id, используя recipient"""
    if not recipient:
        logging.error("Ошибка: recipient отсутствует")
        return None

    url = "https://fragment.com/api?hash=4d28250dc2105d832b"
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": "https://fragment.com",
            'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
    'x-requested-with': 'XMLHttpRequest',
    }
    data = {
        "recipient": recipient,
        "quantity": "50",
        "method": "initBuyStarsRequest"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, cookies=get_cookies(), data=data)
        print(response.content)
        if response.status_code == 200:
            try:
                json_data = response.json()
                print(json_data)
                req_id = json_data.get("req_id")
                logging.info(f"Получен req_id: {req_id}")
                return req_id
            except json.JSONDecodeError:
                logging.error("Ошибка парсинга JSON во втором запросе")
                return None
        else:
            logging.error(f"Ошибка второго запроса: {response.status_code}")
            return None

async def fetch_buy_link(recipient, req_id):
    """Третий запрос: получаем ссылку на покупку с подставленным recipient и req_id"""
    if not recipient or not req_id:
        logging.error("Ошибка: recipient или req_id отсутствуют")
        return
    
    url = "https://fragment.com/api?hash=4d28250dc2105d832b"
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": "https://fragment.com",
        "referer": f"https://fragment.com/stars/buy?recipient={recipient}&quantity=50",
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "x-requested-with": "XMLHttpRequest"
    }
    data = {
        "address":"0:a51960ecabdbb9b20164b72627888a6644a08dc08801a427651743e20f3f5b94","chain":"-239","walletStateInit":"te6cckECFgEAAwQAAgE0AQgBFP8A9KQT9LzyyAsCAgEgCQME+PKDCNcYINMf0x/THwL4I7vyZO1E0NMf0x/T//QE0VFDuvKhUVG68qIF+QFUEGT5EPKj+AAkpMjLH1JAyx9SMMv/UhD0AMntVPgPAdMHIcAAn2xRkyDXSpbTB9QC+wDoMOAhwAHjACHAAuMAAcADkTDjDQOkyMsfEssfy/8HBgUEAAr0AMntVABsgQEI1xj6ANM/MFIkgQEI9Fnyp4IQZHN0cnB0gBjIywXLAlAFzxZQA/oCE8tqyx8Syz/Jc/sAAHCBAQjXGPoA0z/IVCBHgQEI9FHyp4IQbm90ZXB0gBjIywXLAlAGzxZQBPoCFMtqEssfyz/Jc/sAAgBu0gf6ANTUIvkABcjKBxXL/8nQd3SAGMjLBcsCIs8WUAX6AhTLaxLMzMlz+wDIQBSBAQj0UfKnAgBRAAAAACmpoxdPFNI82DmJm8c3IexTJTeZwqMDT1jZXpkMh7Ji8F+ZEkACAUgNCgIBIAwLAFm9JCtvaiaECAoGuQ+gIYRw1AgIR6STfSmRDOaQPp/5g3gSgBt4EBSJhxWfMYQCASAREALm0AHQ0wMhcbCSXwTgItdJwSCSXwTgAtMfIYIQcGx1Z70ighBkc3RyvbCSXwXgA/pAMCD6RAHIygfL/8nQ7UTQgQFA1yH0BDBcgQEI9ApvoTGzkl8H4AXTP8glghBwbHVnupI4MOMNA4IQZHN0crqSXwbjDQ8OAIpQBIEBCPRZMO1E0IEBQNcgyAHPFvQAye1UAXKwjiOCEGRzdHKDHrFwgBhQBcsFUAPPFiP6AhPLassfyz/JgED7AJJfA+IAeAH6APQEMPgnbyIwUAqhIb7y4FCCEHBsdWeDHrFwgBhQBMsFJs8WWPoCGfQAy2kXyx9SYMs/IMmAQPsABgARuMl+1E0NcLH4AgFYFRICASAUEwAZrx32omhAEGuQ64WPwAAZrc52omhAIGuQ64X/wAA9sp37UTQgQFA1yH0BDACyMoHy//J0AGBAQj0Cm+hMYHyTjyk=","publicKey":"4f14d23cd839899bc73721ec53253799c2a3034f58d95e990c87b262f05f9912",
        "features":["SendTransaction",{"name":"SendTransaction","maxMessages":255}],"maxProtocolVersion":2,"platform":"iphone","appName":"Tonkeeper","appVersion":"5.0.14",
        "transaction": "1",
        "id": req_id,
        "show_sender": "1",
        "method": "getBuyStarsLink"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, cookies=get_cookies(), data=data)
        logging.info(f"Ответ третьего запроса: {response.content}")

        if response.status_code == 200:
            # Выполняем финальный запрос (confirmReq)
  
            json_data = response.json()
            if json_data.get("ok") and "transaction" in json_data:
                transaction = json_data["transaction"]
                amount_nano = transaction["messages"][0]["amount"]
                recipient = transaction["messages"][0]["address"]
                la = transaction["messages"][0]["payload"]
                return recipient, amount_nano, la
        
        return None, None, None


def convert_amount_to_decimal(amount_nano):
    return amount_nano / 1_000_000_000  

def generate_unique_nonce():
    """Создает уникальный идентификатор транзакции"""
    return f"{int(time.time())}_{random.randint(1000, 9999)}"

import base64
import re

def fix_base64_padding(b64_string: str) -> str:
    missing_padding = len(b64_string) % 4
    if missing_padding:
        b64_string += '=' * (4 - missing_padding)
    return b64_string



async def send_ton_transaction(recipient, amount_nano, la):

        # Создаем клиента с API ключом
        client = TonapiClient(api_key="AFJYMAGJKTK4CUAAAAAIOFCTJXRWSZCE7OYT7PQP3LBXQL77HD2W52O2OJXZ2TNYNBD5MSQ", is_testnet=False)
      
        # Загружаем кошелек из мнемоники
     
        wallet, public_key, private_key, mnemonic = WalletV5R1.from_mnemonic(client, [
            "orphan", "enroll", "fit", "shallow", "soup", "universe", "master", "estate", "evolve", "agree", "salute",
            "ability", "bargain", "hobby", "lucky", "carbon", "enable", "dolphin", "praise", "patrol", "weekend", "helmet", "kingdom", "grain"
        ])

        logging.info("Кошелек успешно загружен.")


        # Проверяем, что получатель и сумма корректны
        if not recipient:
            logging.error("Ошибка: не указан получатель.")
            return
        if amount_nano <= 0:
            logging.error("Ошибка: некорректная сумма (должна быть больше 0).")
            return

        # Декодирование Base64
    
        # Исходная строка
        encoded_str = la

        # Декодирование
        decoded_bytes = base64.b64decode(fix_base64_padding(encoded_str))

        # Преобразуем в строку, заменяя нечитаемые символы пробелами
        decoded_text = ''.join(chr(b) if 32 <= b < 127 else ' ' for b in decoded_bytes)

        # Убираем лишние пробелы и переводы строк
        clean_text = re.sub(r'\s+', ' ', decoded_text).strip()

        # Удаляем всё, что идёт до "50 Telegram Stars"
        match = re.search(r"50 Telegram Stars.*", clean_text)
        final_text = match.group(0) if match else clean_text

        print(final_text)
 
      
        tx_hash = await wallet.transfer(
            destination=recipient,
            amount=amount_nano,
            body=final_text,
        )
        logging.info(f"✅ Транзакция отправлена: {tx_hash}")
    



async def main():
    recipient = await fetch_recipient()
    if recipient:
        req_id = await fetch_req_id(recipient)
        if req_id:
            recipient, amount_nano, la = await fetch_buy_link(recipient, req_id)
            if recipient and amount_nano and la:
                # Преобразуем amount_nano в нужный формат
                amount_decimal = convert_amount_to_decimal(amount_nano)
                logging.info(f"Сумма для отправки: {amount_decimal:.4f} TON")
                await send_ton_transaction(recipient, amount_decimal, la)

asyncio.run(main())


