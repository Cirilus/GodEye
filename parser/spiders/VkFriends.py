import json
import os
import pprint
import time

import scrapy
from dotenv import load_dotenv

pp = pprint.PrettyPrinter()
load_dotenv()


class UserSpider(scrapy.Spider):
    name = "VKFriends"

    def __init__(self, *args, **kwargs):
        self.api_url = "https://api.vk.com"
        self.user_id = kwargs['user']
        self.api_version = 5.131

        self.access_token = os.getenv("TOKEN")

        self.friends_fields = kwargs.get('friends_fields') or "nickname,music,bdate,city,country,education,sex,schools"

        self.url = f"{self.api_url}/method/friends.get?user_id={self.user_id}&v={self.api_version}&access_token={self.access_token}"

        super(UserSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        yield scrapy.Request(self.url, self.parse)

    def parse(self, response, **kwargs):

        self.log(f"parse user's friends of  user {self.user_id}")

        if "error" not in response.text:
            friends = json.loads(response.text)['response']
            friends["id"] = self.user_id
        else:
            friends = {}
        yield friends
