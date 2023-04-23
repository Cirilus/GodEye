import json
import os
import pprint
import time

import scrapy
from dotenv import load_dotenv

pp = pprint.PrettyPrinter()
load_dotenv()


class UserSpider(scrapy.Spider):
    name = "UsersByGroup"

    def __init__(self, *args, **kwargs):
        self.api_url = "https://api.vk.com"
        self.group_id = kwargs['group']
        self.offset = kwargs.get('offset') or 0
        self.api_version = 5.131

        self.access_token = os.getenv("TOKEN")

        self.group_fields = kwargs.get("group_fields") or ""
        self.group_extended = kwargs.get("group_extended") or 0

        self.url = f"{self.api_url}/method/groups.getMembers/?group_id={self.group_id}&offset={self.offset}&v={self.api_version}" \
                   f"&access_token={self.access_token}"

        super(UserSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        yield scrapy.Request(self.url, self.parse)

    def parse(self, response, **kwargs):
        self.logger.info(f"parse users of {self.group_id} group")
        users = json.loads(response.text)['response']
        yield users
