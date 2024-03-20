from sqlalchemy import create_engine, Column, Integer, String, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class OrderCourt(Base):

    __tablename__ = 'order_court'

    id = Column(Integer, primary_key=True)
    order_court = Column('lunch_court', String)
    order_count = Column('soup_court', Integer, default=0)


class Count(Base):

    __tablename__ = 'lunch_count'

    id = Column(Integer, primary_key=True)
    lunch = Column('lunch', Integer, default=0)
    soup = Column('soup', Integer, default=0)


class ClientBase(Base):

    __tablename__ = 'client_base'

    user_id = Column('id', Integer, primary_key=True)
    user_name = Column('username', String)
    first_name = Column('first', String)
    last_name = Column('last', String)
    phone = Column('phone', Integer)


engine = create_engine('sqlite:///my_database.db')

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


# Очищення таблиці
# session.query(ClientBase).delete()
# session.commit()


