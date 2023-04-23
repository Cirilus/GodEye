from uuid import uuid4

from scrapyd_api import ScrapydAPI


scrapyd = ScrapydAPI('http://localhost:6800')
unique_id = str(uuid4())
settings = {
    'unique_id': unique_id,
    'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
}

# Vk User
# task = scrapyd.schedule('default', 'VKUser',
#                         settings=settings,
#                         user=1,
#                         #user_fields=,
#                         )


#Vk Friends
# task = scrapyd.schedule('default', 'VKFriends',
#                         settings=settings,
#                         user=1,
#                         #friends_fields=,
#                         )


# VKGroupsByUser

# task = scrapyd.schedule('default', 'VKGroupsByUser',
#                         settings=settings,
#                         user=1,
#                         #group_fields=,
#                         #group_extended=,
#                         )


# UsersByGroup

task = scrapyd.schedule('default', 'UsersByGroup',
                        settings=settings,
                        group=1,
                        offset=0)