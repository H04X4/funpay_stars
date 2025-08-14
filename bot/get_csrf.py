import requests
from bs4 import BeautifulSoup
import json


def get_csrf_token():
    from SETTINGS import GOLDEN_KEY, USER_AGENT, PROXY
    while True:
        headers = {}
        headers["cookie"] = f"golden_key={GOLDEN_KEY}; cookie_prefs=1"
        headers["user-agent"] = USER_AGENT
        proxy = {
            "http": PROXY,
            "https": PROXY
        }
        response = requests.get("https://funpay.com/", headers=headers, proxies=proxy)
        cookies = response.cookies.get_dict()
        
        phpsessid = ""
        phpsessid = cookies.get("PHPSESSID", phpsessid)
        headers["cookie"] += f"; PHPSESSID={phpsessid}"

        html_response = response.content.decode()
        parser = BeautifulSoup(html_response, "lxml")
        try:
            app_data = json.loads(parser.find("body").get("data-app-data"))
            csrf_token = app_data["csrf-token"]
            id = app_data["userId"]
            break
        except Exception as e:
            print(f"Не удалось получить csrf-token: {e}")
    
    response = requests.get("https://funpay.com/", headers=headers, proxies=proxy)
    html_response = response.content.decode()
    parser = BeautifulSoup(html_response, "lxml")
    username = parser.find("div", {"class": "user-link-name"})
    print(username)
    return headers, csrf_token, id, username.text