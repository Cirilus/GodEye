import json
import os

from bson import json_util
from dotenv import load_dotenv
from pymongo import MongoClient
from DTO.kafkaDTO import KafkaProducerManager

load_dotenv()

uri = os.getenv("MONGO_URI")

cluster = MongoClient(uri)

db = cluster["GodEye"]

UsersByGroupCollection = db['UsersByGroup']
VKFriendsCollection = db['VKFriends']
VKGroupsByUserCollection = db['VKGroupsByUser']
VKUserCollection = db['VKUser']


kafka = KafkaProducerManager()


class VKPipeline:
    async def process_item(self, item, spider):
        match spider.name:
            case "UsersByGroup":
                kafka.publish_message("RawId",json.dumps(item, default=json_util.default))
                # UsersByGroupCollection.insert_one(item)
            case "VKFriends":
                kafka.publish_message("VkFriends", json.dumps(item, default=json_util.default))
                # VKFriendsCollection.insert_one(item)
            case "VKGroupsByUser":
                kafka.publish_message("RawId", json.dumps(item, default=json_util.default))
                # VKGroupsByUserCollection.insert_one(item)
            case "VKUser":
                kafka.publish_message("VKUser", json.dumps(item, default=json_util.default))
                # VKUserCollection.insert_one(item)
