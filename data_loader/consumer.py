import json
from walrus import Database
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from AlchemyModel import UserVKModel


#wgpIaFfrQN86

def connect_postgres():
    db_url = f'postgresql://Shkolenko02-03-2004:wgpIaFfrQN86@ep-red-wave-605810.eu-central-1.aws.neon.tech/GodEye'
    engine = db.create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    # UserVKModel.__table__.create(bind=engine) # create the table
    return session


def connect_redis():
    redis = Database(host='localhost', port=6379, db=0)
    return redis




redis = connect_redis()
stream = redis.Stream("UserVK")
session = connect_postgres()
messages = stream.read()


for message in messages:
    id = message[0].decode("utf-8")
    data = json.loads(message[1][b'user'])
    new_user = UserVKModel(Id = data['id'], Data=data)
    session.add(new_user)
    session.commit()
    stream.delete(id)
    break










