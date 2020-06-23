from config import DATABASE
import psycopg2
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, BigInteger, String, Boolean, Sequence
from sqlalchemy.ext.declarative import declarative_base


db = declarative_base() 

class Users(db):
    
    __tablename__ = 'subscriptions'
    
    id = Column(BigInteger, primary_key=True, autoinctement=True)
    user_id = Column(String)
    status = Column(Boolean)

    def __init__(self, user_id, status=True):

        self.user_id = user_id
        self.status = status

    def __repr__(self):
        return f'User(id={self.id}, user_id={self.user_id}, status={self.status})'


class DbLighter:

    metadata = MetaData()

    def __init__(self, database):

        self.engine = create_engine(database)
        self.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()


    def get_subscriptions(self):
        return session.query(self).all()

    def set_subscription(self, user_id, status):
        user = Users(user_id, status)

        self.session.add(user)
        self.session.commit()

