from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as db

Base = declarative_base()


class UserVKModel(Base):
    __tablename__ = 'UserVK'

    Id = db.Column(db.Integer, primary_key=True)
    Data = db.Column(db.JSON)

