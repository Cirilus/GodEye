import json
import os

from bson import json_util
from dotenv import load_dotenv
from pymongo import MongoClient
from utils.kafkaService import KafkaProducerService

load_dotenv()

uri = os.getenv("MONGO_URI")

cluster = MongoClient(uri)

db = cluster["GodEye"]

UsersByGroupCollection = db['UsersByGroup']
VKFriendsCollection = db['VKFriends']
VKGroupsByUserCollection = db['VKGroupsByUser']
VKUserCollection = db['VKUser']


kafka = KafkaProducerService()


class VKPipeline:
    async def process_item(self, item, spider):
        match spider.name:
            case "UsersByGroup":
                kafka.publish_message("UsersByGroup", str(item["group_id"]), json.dumps(item, default=json_util.default))
                UsersByGroupCollection.insert_one(item)
            case "VKFriends":
                print(item)
                kafka.publish_message("VKFriends", str(item["id"]), json.dumps(item, default=json_util.default))
                VKFriendsCollection.insert_one(item)
            case "VKGroupsByUser":
                kafka.publish_message("VKGroupsByUser", str(item["id"]), json.dumps(item, default=json_util.default))
                VKGroupsByUserCollection.insert_one(item)
            case "VKUser":
                kafka.publish_message("VKUser", str(item["id"]), json.dumps(item, default=json_util.default))
                VKUserCollection.insert_one(item)
