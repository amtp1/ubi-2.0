import requests 
from requests.exceptions import ConnectionError
import random
from loguru import logger

from datetime import datetime as dt
from datetime import timedelta
from dateutil.tz import tzlocal

from config import config

cfg = config.Config()

DateTime = dt.now(tz=tzlocal()) + timedelta(hours=7,minutes=15)
DT = DateTime.strftime("%Y-%m-%dT%H:%M:%S+03:00")

class Payment:
    headers:dict
    params:dict
    count:float

    def __init__(self, count=None):
        self.count = count
        self.headers = {
                "Authorization":f"Bearer {cfg.qiwi_private_key}", 
                "Content-Type":"application/json", 
                "Accept":"application/json", 
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
                }

        self.params = { 
                "amount":{"value":self.count, "currency":"RUB"}, 
                "comment":"ubi", "expirationDateTime":DT
                }

        self.check_headers = {
                "Authorization":f"Bearer {cfg.qiwi_private_key}", 
                "Accept":"application/json"
                }

    def generate_id(self, id=None) -> str:
        rdm_lst = list("1234567890ABCDEFGHIJKLMNOPQRSTUVWQXYZabcdefghijklmnopqrstuvwxyz")
        random.shuffle(rdm_lst)
        res_1 = "".join([random.choice(rdm_lst) for x in range(8)])
        res_2 = "".join([random.choice(rdm_lst) for x in range(4)])
        res_3 = "".join([random.choice(rdm_lst) for x in range(4)])
        res_4 = "".join([random.choice(rdm_lst) for x in range(4)])
        res_5 = "".join([random.choice(rdm_lst) for x in range(8)])

        return f"{res_1}-{res_2}-{res_3}-{res_4}-{res_5}"

    def create_url(self) -> str:
        self.last_id = self.generate_id()
        return r"https://api.qiwi.com/partner/bill/v1/bills/%s" % self.generate_id()
    
    def create_invoice(self) -> dict:
        try:
            return requests.put(url=self.create_url(), json=self.params, headers=self.headers, timeout=5).json()
        except ConnectionError:return False

    def check_payment(self, last_id=None) -> dict:
        return requests.get(url="https://api.qiwi.com/partner/bill/v1/bills/%s" % last_id, headers=self.check_headers).json()