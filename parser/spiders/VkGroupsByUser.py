import json
import os
import pprint
import time

import scrapy
from dotenv import load_dotenv

pp = pprint.PrettyPrinter()
load_dotenv()


class UserSpider(scrapy.Spider):
    name = "VKGroupsByUser"

    def __init__(self, *args, **kwargs):
        self.api_url = "https://api.vk.com"
        self.user_id = kwargs['user']
        self.api_version = 5.131

        self.access_token = os.getenv("TOKEN")

        self.group_fields = kwargs.get("group_fields") or ""
        self.group_extended = kwargs.get("group_extended") or 0

        self.url = f"{self.api_url}/method/groups.get/?user_id={self.user_id}&v={self.api_version}&extended={self.group_extended}&access_token={self.access_token}"

        super(UserSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        yield scrapy.Request(self.url, self.parse)

    def parse(self, response, **kwargs):
        self.log(f"parse user's groups of user {self.user_id}")
        if "error" not in response.text:
            groups = json.loads(response.text)['response']
            groups["id"] = self.user_id
        else:
            groups = {}
        yield groups
