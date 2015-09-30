from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# Before running the program please delete database and create database with
# command: dropdb tbay && createdb tbay

# Creating foundations
engine = create_engine('postgresql://ubuntu:thinkful@localhost:5432/tbay')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


# Creating Classes, Tables and relationships
class User (Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    # Creating relationships
    bids = relationship("Bid", backref="consumer")
    items = relationship("Item", backref="owner")


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime, default=datetime.utcnow)
    # Creating relationships
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    bids = relationship("Bid", backref="item")


class Bid(Base):
    __tablename__ = "bids"
    id = Column(Integer, primary_key=True)
    price = Column(Float, nullable=False)
    # Creating relationships
    consumer_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)


Base.metadata.create_all(engine)

# Adding data
avi = User(username='Avi', password='1234')
benji = User(username='Benji', password='5678')
carol = User(username='Carol', password='abcd')
baseball = Item(name='Baseball', owner=avi)
basketball = Item(name='Basketball', owner=benji)
bid1 = Bid(price=10.5, consumer=benji, item=baseball)
bid2 = Bid(price=20.5, consumer=benji, item=baseball)
bid3 = Bid(price=30.5, consumer=carol, item=baseball)
bid4 = Bid(price=40.5, consumer=carol, item=baseball)
session.add_all([avi, benji, carol, baseball, basketball, bid1, bid2, bid3])
session.add_all([bid4])
session.commit()

# Presenting Data
print('\nWelcome To Tbay!')
print('\nLIST OF BIDS:')
bids = session.query(Bid).all()
string = 'ITEM: {}\tPRICE: {}\tCUSTOMER: {}'
for bid in bids:
    print(string.format(bid.item.name, bid.price, bid.consumer.username))

# Data Query
query = session.query(Bid).join(Bid.item).filter(Item.name == 'Baseball')
query = query.order_by(Bid.price.desc()).first().consumer.username
print('\nAnd the winner is: {}'.format(query))
