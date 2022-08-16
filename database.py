from sqlalchemy import Column, Integer, String, Float, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Caminho relativo (pode ser utilizado o caminho absoluto):
engine = create_engine('sqlite:///db.sqlite3', connect_args={'check_same_thread':False})
Session = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    role = Column('role', String(32))

    def __init__(self, id, role):
        self.id = id
        self.role = role

class Restaurant(Base):
    __tablename__ = 'restaurant'

    id = Column(Integer, primary_key=True)
    name = Column('name', String(32))
    segment = Column('segment', String(32))
    uf = Column('uf', String(2))

    def __init__(self, id, name, segment, uf):
        self.id = id
        self.name = name
        self.segment = segment
        self.uf = uf

class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    name = Column('name', String(32))
    price = Column('price', Float(2,10))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship('Restaurant')

    def __init__(self,restaurant_id, id, price, name):
        self.restaurant_id = restaurant_id
        self.id = id
        self.price = price
        self.name = name

Base.metadata.create_all(engine)