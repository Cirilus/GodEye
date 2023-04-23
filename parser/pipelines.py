import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

uri = os.getenv("MONGO_URI")

cluster = MongoClient(uri)

db = cluster["GodEye"]

UsersByGroupCollection = db['UsersByGroup']
VKFriendsCollection = db['VKFriends']
VKGroupsByUserCollection = db['VKGroupsByUser']
VKUserCollection = db['VKUser']

class VKPipeline:
    async def process_item(self, item, spider):
        print(spider.name)
        match spider.name:
            case "UsersByGroup":
                UsersByGroupCollection.insert_one(item)
            case "VKFriends":
                VKFriendsCollection.insert_one(item)
            case "VKGroupsByUser":
                VKGroupsByUserCollection.insert_one(item)
            case "VKUser":
                print(item)
                VKUserCollection.insert_one(item)
