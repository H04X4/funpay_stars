import asyncio
import asks
from tonutils.wallet.data import TransferData
from tonutils.client import ToncenterClient
from tonutils.wallet import WalletV5R1
from tonutils.wallet import WalletV4R2

qu = asyncio.Queue()

async def mai1n(chat, stars):
    from bot.cleaner import clean_and_decode
    from main import account_fragment, device_fragment, headers111, fragment_hash, toncenter_apikey, keeper_walletV4R2, keeper_walletV5R1
    for i in range(5):
        try:
            json00 = {
                "query": str(chat),
                "quantity": "",
                "method": "searchStarsRecipient"
            }
            resp = await asks.post(f"https://fragment.com/api?hash={fragment_hash}", headers=headers111, data=json00)
            nick = resp.json()
            json00 = {
                'recipient': nick["found"]["recipient"],
                'quantity': stars,
                'method': 'initBuyStarsRequest'
            }

            resp = await asks.post(f"https://fragment.com/api?hash={fragment_hash}", headers=headers111, data=json00)
            buy = resp.json()
            json00 = {
                'account': account_fragment,
                'device': device_fragment,
                'transaction': 1,
                'id': buy["req_id"],
                'show_sender': 0,
                'method': 'getBuyStarsLink'
            }

            resp = await asks.post(f"https://fragment.com/api?hash={fragment_hash}", headers=headers111, data=json00)
            transaction = resp.json()

            client = ToncenterClient(api_key=toncenter_apikey, is_testnet=False)

            if keeper_walletV5R1 != "":
                wallet, public_key, private_key, mnemonic = WalletV5R1.from_mnemonic(client=client, mnemonic=keeper_walletV5R1.split())
            else:
                wallet, public_key, private_key, mnemonic = WalletV4R2.from_mnemonic(client=client, mnemonic=keeper_walletV4R2.split())

            data_list = []
            app = clean_and_decode(transaction["transaction"]["messages"][0]["payload"])
            data_list.append(
                TransferData(
                    destination=transaction["transaction"]["messages"][0]["address"],
                    amount=int(transaction["transaction"]["messages"][0]["amount"])/1000000000,
                    body=(app)
                )
            )
            

            tx_hash = await wallet.batch_transfer(
                data_list=data_list
            )
            print(tx_hash)
            await asyncio.sleep(5)
        except Exception as e:
            await asyncio.sleep(2)
            print(e)
        else:
            return True

    return False

async def task_worker():
    while True:
        chat, star, future = await qu.get()
        result = await mai1n(chat, star)
        future.set_result(result) 
        qu.task_done()

async def give_stars(order_id, description, buyer_username):
    from FunpayAPI.funtions import send_message, get_chat_history, get_order_status, refund
    from SETTINGS import GET_NICK_TEXT, ERRROR_NICK_TEXT, ERRROR_NOTFOUNDED_NICK_TEXT, SUCCESS_SENDED_TEXT, MONEYBACK_TEXT, QUEUE_TEXT
    from SETTINGS import fragment_hash, headers111
    if "Stars" in description and "10 Stars" not in description and "15 Stars" not in description and "25 Stars" not in description:
        while True:
            try:
                await send_message(buyer_username, GET_NICK_TEXT)
                while True:
                    await asyncio.sleep(15)
                    chat = await get_chat_history(buyer_username)
                    msg = chat[-1]
                    print(f"Текущее сообщение: {msg}")
                    if str(msg)[0] == "@":
                        stars = description.split(" Stars")[0]
                        print(f"Выдаю {stars} звезд...")
                        json00 = {
                            "query": str(msg),
                            "quantity": "",
                            "method": "searchStarsRecipient"
                        }
                        try:
                            resp = await asks.post(f"https://fragment.com/api?hash={fragment_hash}", headers=headers111, data=json00)
                        except:
                            resp = await asks.post(f"https://fragment.com/api?hash={fragment_hash}", headers=headers111, data=json00)
                        n = resp.text

                        if '{"error":"No Telegram users found."}' in n:
                            await asyncio.sleep(1)
                            await send_message(buyer_username, ERRROR_NOTFOUNDED_NICK_TEXT)
                        else:
                            await asyncio.sleep(1)
                            sta = await get_order_status(order_id)
                            if sta:
                                try:
                                    result = str(description).split("Stars, ")[1].split(" ")[0]
                                    amount = int(result)
                                except:
                                    amount = 1

                                ochered = qu.qsize()
                                await asyncio.sleep(1)
                                await send_message(buyer_username, QUEUE_TEXT.replace("$$$NUMBER$$$", str(1 + int(ochered))))

                                future = asyncio.Future()
                                await qu.put((msg, str(int(stars) * amount), future))
                                star_sending = await future

                                if star_sending == True:
                                    await send_message(buyer_username, SUCCESS_SENDED_TEXT)
                                else:
                                    await send_message(buyer_username, MONEYBACK_TEXT)
                                    await asyncio.sleep(2)
                                    await refund(order_id)
                                break
                            else:
                                print(f"ЗАКАЗ МАНИБЕКНУЛИ")
                            break

                    elif GET_NICK_TEXT in str(msg) or ERRROR_NICK_TEXT in str(chat) or ERRROR_NOTFOUNDED_NICK_TEXT in str(msg):
                        print("Не найдено ника")
                    else:
                        await send_message(buyer_username, ERRROR_NICK_TEXT)
                        print("Неверно введен ник")
            except Exception as e:
                print(e)
            else:
                break
    else:
        print("Товар не из категории Stars")