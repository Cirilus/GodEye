from uuid import uuid4

from scrapyd_api import ScrapydAPI

from DTO.kafkaDTO import KafkaConsumerManager

scrapyd = ScrapydAPI('http://localhost:6800')
unique_id = str(uuid4())
settings = {
    'unique_id': unique_id,
    'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
}

kafka = KafkaConsumerManager()
messages = kafka.read_messages("RawId")
# Vk User
# for i in range(1000, 1020):
#     task = scrapyd.schedule('default', 'VKUser',
#                             settings=settings,
#                             user=i,
#                             #user_fields=,
#                             )



#Vk Friends
# for i in range(1, 100):
#     task = scrapyd.schedule('default', 'VKFriends',
#                             settings=settings,
#                             user=messages[0]['value']['items'][i],
#                             #friends_fields=,
#                             )


# VKGroupsByUser

# task = scrapyd.schedule('default', 'VKGroupsByUser',
#                         settings=settings,
#                         user=1,
#                         #group_fields=,
#                         #group_extended=,
#                         )


# UsersByGroup

# task = scrapyd.schedule('default', 'UsersByGroup',
#                         settings=settings,
#                         group=175085837,
#                         offset=0)
