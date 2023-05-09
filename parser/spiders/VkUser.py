import json
import os
import pprint
import time

import scrapy
from dotenv import load_dotenv

pp = pprint.PrettyPrinter()
load_dotenv()


class UserSpider(scrapy.Spider):
    name = "VKUser"

    def __init__(self, *args, **kwargs):
        self.api_url = "https://api.vk.com"
        self.user_id = kwargs['user']
        self.api_version = 5.131
        self.access_token = os.getenv("TOKEN")
        self.user_fields = kwargs.get('user_fields') or "nickname,music,bdate,city,country,education,sex,schools"

        self.url = f"{self.api_url}/method/users.get?user_ids={self.user_id}&v={self.api_version}&fields={self.user_fields}&access_token={self.access_token}"

        super(UserSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        yield scrapy.Request(self.url, self.parse)

    def parse(self, response, **kwargs):
        self.log(f"parse info about {self.user_id}")

        user = json.loads(response.text)['response']
        yield user[0]
