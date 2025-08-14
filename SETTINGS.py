#_________ACCOUNT SETTINGS_________

GOLDEN_KEY = "ipxg17gqk9oj0wdhfux6x4tu6moofy0d"
PROXY = "http://bagrovni8237:7nIWIrY4Y2@23.230.158.237:50100"

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 OPR/116.0.0.0 (Edition Yx GX)"

#_________TEXTS SETTINGS_________

GET_NICK_TEXT = """✍️ Напишите имя пользователя (@username) без посторонних символов и слов, вместе с @. Если вы ранее писали его - продублируйте"""
ERRROR_NICK_TEXT = """❌ Вы неверно ввели имя пользователя (@username), введите его без посторонних символов и слов, вместе с @:"""
ERRROR_NOTFOUNDED_NICK_TEXT = """🛑 Вы написали имя пользователя (@username) неправильно"""
SUCCESS_SENDED_TEXT = """💫 Звёзды были успешно отправлены. Не забывайте подтвердить заказ и оставить отзыв"""
MONEYBACK_TEXT = """❌ Звёзды не были выданы, заказ отменен"""
QUEUE_TEXT = """🧑‍💻 Вы были поствлены в очередь, в данный момент вы №$$$NUMBER$$$ в очереди""" #Чтобы добавить номер в очередь напишите $$$NUMBER$$$ и оно автоматически заменится на номер очереди

#_________BOT SETTINGS_________

TOKEN = "7371720699:AAGuM946hQ_IzjDrqLGmCF8NgKv2Xr5jlC0"

#_________FRAGMENT SETTINGS_________

headers111 = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-encoding': 'gzip, deflate, br, zstd',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'content-length': '1572',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'cookie': 'stel_ssid=00fe1e1452e5088216_1062226016582018372; stel_dt=-300; stel_ton_token=U6UbdvxOSpJCXtyNjjqOfw-3LybhBTGAYaLzAgNZpMPpTlcqX8Blc9JlT9V6xb2WpSPqH92f4WKNvw4JME0TrIG_S4jQM03hmC_OcPtLtar9d_u6o1ifYqzRZYCwYGMRDmwD-9bFzyu0rfJPYjaxeuCGNji3mlE0ytRWSV_LgsuWFPtevP9cqXi_AuALN6hf07szpv4Z; stel_token=d32974e2f7ecd362b49ad27f7f6db772d32974f9d3297d3a8f4021dadb2fe1a0782ce',
    'origin': 'https://fragment.com',
    'priority': 'u=1, i',
    'referer': 'https://fragment.com/stars/buy',
    'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'
}

account_fragment = {"address":"0:a51960ecabdbb9b20164b72627888a6644a08dc08801a427651743e20f3f5b94","chain":"-239","walletStateInit":"te6cckECFgEAAwQAAgE0AQgBFP8A9KQT9LzyyAsCAgEgCQME+PKDCNcYINMf0x/THwL4I7vyZO1E0NMf0x/T//QE0VFDuvKhUVG68qIF+QFUEGT5EPKj+AAkpMjLH1JAyx9SMMv/UhD0AMntVPgPAdMHIcAAn2xRkyDXSpbTB9QC+wDoMOAhwAHjACHAAuMAAcADkTDjDQOkyMsfEssfy/8HBgUEAAr0AMntVABsgQEI1xj6ANM/MFIkgQEI9Fnyp4IQZHN0cnB0gBjIywXLAlAFzxZQA/oCE8tqyx8Syz/Jc/sAAHCBAQjXGPoA0z/IVCBHgQEI9FHyp4IQbm90ZXB0gBjIywXLAlAGzxZQBPoCFMtqEssfyz/Jc/sAAgBu0gf6ANTUIvkABcjKBxXL/8nQd3SAGMjLBcsCIs8WUAX6AhTLaxLMzMlz+wDIQBSBAQj0UfKnAgBRAAAAACmpoxdPFNI82DmJm8c3IexTJTeZwqMDT1jZXpkMh7Ji8F+ZEkACAUgNCgIBIAwLAFm9JCtvaiaECAoGuQ+gIYRw1AgIR6STfSmRDOaQPp/5g3gSgBt4EBSJhxWfMYQCASAREALm0AHQ0wMhcbCSXwTgItdJwSCSXwTgAtMfIYIQcGx1Z70ighBkc3RyvbCSXwXgA/pAMCD6RAHIygfL/8nQ7UTQgQFA1yH0BDBcgQEI9ApvoTGzkl8H4AXTP8glghBwbHVnupI4MOMNA4IQZHN0crqSXwbjDQ8OAIpQBIEBCPRZMO1E0IEBQNcgyAHPFvQAye1UAXKwjiOCEGRzdHKDHrFwgBhQBcsFUAPPFiP6AhPLassfyz/JgED7AJJfA+IAeAH6APQEMPgnbyIwUAqhIb7y4FCCEHBsdWeDHrFwgBhQBMsFJs8WWPoCGfQAy2kXyx9SYMs/IMmAQPsABgARuMl+1E0NcLH4AgFYFRICASAUEwAZrx32omhAEGuQ64WPwAAZrc52omhAIGuQ64X/wAA9sp37UTQgQFA1yH0BDACyMoHy//J0AGBAQj0Cm+hMYHyTjyk=","publicKey":"4f14d23cd839899bc73721ec53253799c2a3034f58d95e990c87b262f05f9912"}
device_fragment = {"appVersion":"5.0.14","maxProtocolVersion":2,"appName":"Tonkeeper","platform":"iphone","features":["SendTransaction",{"maxMessages":255,"name":"SendTransaction"}]}
toncenter_apikey = "606982b24d2a1c8734720d72a83c753ed33c4e71f959fe6173433b72507a4ccb"

keeper_walletV5R1 = "orphan  enroll  fit  shallow  soup  universe  master  estate  evolve  agree  salute  ability  bargain  hobby  lucky  carbon  enable  dolphin  praise  patrol  weekend  helmet  kingdom  grain"
keeper_walletV4R2 = ""

fragment_hash = "4d28250dc2105d832b"