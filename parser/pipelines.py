import json

from walrus import Database

db = Database()

VKStream = db.Stream("UserVK")

class VKPipeline:
    async def process_item(self, item, spider):
        item = json.dumps(item)
        VKStream.add({"user": item})
        return
