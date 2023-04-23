import json
import os
import pprint
import time

import scrapy
from dotenv import load_dotenv

pp = pprint.PrettyPrinter()
load_dotenv()

class UserSpider(scrapy.Spider):
    name = "VK"

    def __init__(self, *args, **kwargs):
        self.api_url = "https://api.vk.com"
        self.user_id = 1
        self.api_version = 5.131

        self.access_token = "vk1.a.HR9sCHDy2uSggf4uPi8oqzoNjfMIi5_hUQ7KzDkHuy21FPitjo3L1hJwHMB6jJPrdwMovbafh91Ju5CHus953Q_rusHgHQ_4hG2lbGBa65isKPVrdaXVvzkZ4VS6httmXmFIUQKe0lV05w_m_R_xGGDRrMW2NRhfLreHhNiAGFr2dHHBLBaz65fdA0wALTkDE-nO0mHsHJNaGEPGidVzXg"

        self.info_fields = "nickname,music,bdate,city,country,education,sex,schools"
        self.friends_fields = "nickname,music,bdate,city,country,education,sex,schools"
        self.group_fields = ""
        self.group_extended = 1

        self.info_url = f"{self.api_url}/method/users.get?user_ids={self.user_id}&v={self.api_version}&fields={self.info_fields}&access_token={self.access_token}"
        self.group_url = f"{self.api_url}/method/groups.get/?user_id={self.user_id}&v={self.api_version}&extended={self.group_extended}&access_token={self.access_token}"
        self.friends_url = f"{self.api_url}/method/friends.get?user_id={self.user_id}&v={self.api_version}&fields={self.friends_fields}&access_token={self.access_token}"

        super(UserSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        yield scrapy.Request(self.info_url, self.parse_info)

    def parse_info(self, response):
        self.logger.info(f"parse info about {self.user_id}")

        user = json.loads(response.text)['response']

        self.group_url = f"{self.api_url}/method/groups.get/?user_id={self.user_id}&v={self.api_version}&extended={self.group_extended}&access_token={self.access_token}"
        yield scrapy.Request(self.group_url, self.parse_group, cb_kwargs=({"user": user}))

    def parse_group(self, response, user):

        self.logger.info(f"parse user's groups of user {self.user_id}")

        if "error" not in response.text:
            user[0]['group'] = json.loads(response.text)['response']
        else:
            user[0]['group'] = "This profile is private"

        self.friends_url = f"{self.api_url}/method/friends.get?user_id={self.user_id}&v={self.api_version}&fields={self.friends_fields}&access_token={self.access_token}"
        yield scrapy.Request(self.friends_url, self.parse_friends, cb_kwargs=({"user": user}))

    def parse_friends(self, response, user):

        self.logger.info(f"parse user's friends of  user {self.user_id}")

        if "error" not in response.text:
            user[0]['friends'] = json.loads(response.text)['response']
        else:
            user[0]['friends'] = "This profile is private"

        self.user_id += 1
        self.info_url = f"{self.api_url}/method/users.get?user_ids={self.user_id}&v={self.api_version}&fields={self.info_fields}&access_token={self.access_token}"
        yield user[0]
        time.sleep(0.5)
        yield scrapy.Request(self.info_url, self.parse_info)
