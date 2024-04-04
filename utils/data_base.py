from sqlalchemy import create_engine, Column, Integer, String, CHAR, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class OrderList(Base):

    __tablename__ = 'list_order'

    id = Column('id', Integer, primary_key=True)
    date = Column('datetime', String)
    user_name = Column('username', String)
    first_name = Column('first', String)
    last_name = Column('last', String)
    lunch = Column('lunch', Integer)
    soup = Column('soup', Integer)


class Count(Base):
    """
    Таблиця в яку адмін бота вносить кількість товару
    """

    __tablename__ = 'lunch_count'

    id = Column(Integer, primary_key=True)
    lunch = Column('lunch', Integer, default=0)
    soup = Column('soup', Integer, default=0)
    price_lunch = Column('price_lunch', Integer, default=0)
    price_soup = Column('price_soup', Integer, default=0)


class ClientBase(Base):
    """
    Клієнтська база
    """

    __tablename__ = 'client_base'

    user_id = Column('id', Integer, primary_key=True)
    user_name = Column('username', String)
    first_name = Column('first', String)
    last_name = Column('last', String)
    phone = Column('phone', String)

engine = create_engine('sqlite:///my_database.db')

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


# Очищення таблиці
# session.query(Count).delete()
# session.commit()


