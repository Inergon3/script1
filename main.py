import datetime
import logging
import os
import time

import requests
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, filename="logs.log",filemode="a")
urls = ["http://localhost:8000/secret/"]
data = {
    "secret": "secret",
    "passphrase": "1234",
    "ttl_seconds": 60
}
#нужна информацию что в себя принемает endpoint на который отправляется post запрос


def get_message_tg(message):
    load_dotenv()
    url_bot = f"https://api.telegram.org/bot{os.getenv("tocken_bot")}/sendMessage?chat_id={os.getenv("chat_id")}&text={message}"
    response = requests.get(url_bot)
    print(response.json())


while True:
    for url in urls:
        count_401 = 0
        count_500 = 0
        for i in range(1, 6):
            response = requests.post(url, json=data)
            status = response.status_code
            text = f"\n time= {datetime.datetime.now()},\n URL= {response.url},\n status_code= {response.status_code},\n time_response= {response.elapsed.total_seconds()}\n"
            if str(status)[0] == "2":
                logging.info(text)
            if str(status)[0] != "2" or response.elapsed.total_seconds() >= 2:
                logging.warning(text)
            if response.status_code == 401:
                count_401 += 1
            else:
                count_401 = 0
            if response.status_code == 500:
                count_500 += 1
            else:
                count_500 = 0
            if str(status)[0] == "5" or count_401 >= 3 or count_500 >= 3:
                text_error = "Critical_error: " + text
                logging.critical(text)
                get_message_tg(text_error)
    time.sleep(300)
