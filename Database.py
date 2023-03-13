from sqlalchemy.orm import relationship, declarative_base
from extraction.ext_cityes import rec_db_cityes
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import sqlalchemy as sq
import datetime
import os

load_dotenv()

Base = declarative_base()


class User(Base):
    __tablename__ = 'User'
    id = sq.Column(sq.Integer, primary_key=True)
    id_tg = sq.Column(sq.Integer, nullable=False)
    first_name = sq.Column(sq.String(length=80))
    city = sq.Column(sq.String(length=20))
    reg_date = sq.Column(sq.TIMESTAMP, nullable=False)

    def __str__(self):
        return f'User {self.id}, {self.id_tg}: {self.first_name}'


class Notes(Base):
    __tablename__ = 'Notes'
    id = sq.Column(sq.Integer, primary_key=True)
    created_date = sq.Column(sq.DateTime, default=datetime.datetime.utcnow)
    text_notes = sq.Column(sq.Text)
    user_id = sq.Column(sq.Integer, sq.ForeignKey("User.id"), nullable=False)
    publisher = relationship(User, backref="notes")

    def __str__(self):
        return f'Notes {self.id}, {self.created_date}, {self.user_id}: {self.text_notes}'


class City(Base):
    __tablename__ = 'City'
    id = sq.Column(sq.Integer, primary_key=True)
    id_city = sq.Column(sq.Integer)
    name = sq.Column(sq.String(length=80))
    url = sq.Column(sq.String(length=80))
    rec_date = sq.Column(sq.TIMESTAMP, nullable=False)

    def __str__(self):
        return f'City {self.id}, {self.id_city}, {self.name}: {self.url}'


def create_tables(engine):
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


DSN = f'postgresql+psycopg2://{os.getenv("DATABASE_USER")}:{os.getenv("DATABASE_PASSWORD")}' \
      f'@{os.getenv("HOST")}:{os.getenv("DATABASE_PORT")}/{os.getenv("DATABASE_NAME")}'
engine = sq.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()


def city_entry():
    """Функция заполнения БД городов с сайта afisha.ru"""
    for enter_city in rec_db_cityes():
        new_city = City(id_city=enter_city['ID'],
                        name=enter_city['Name'],
                        url=enter_city['Url'],
                        rec_date=datetime.datetime.utcnow())
        session.add(new_city)
        session.commit()


def user_entry(ids, name, cities, rdate):
    """Функция добавления пользователя в БД.
    На вход принимает следующие параметры:
    1) ids - ID номер телеграмм
    2) name - имя пользователя
    3) cities - город пользователя
    4) rdate - дата регистрации пользователя (в формате timestamp)"""

    user_verification = session.query(User.id).filter(User.id_tg == ids)
    if session.query(user_verification.exists()).scalar():
        print('Its good')
    else:
        new_user = User(id_tg=ids,
                        first_name=name,
                        city=cities,
                        reg_date=rdate)
        session.add(new_user)
        session.commit()


def city_edit(ids, cities="Москва"):
    """Функция редактирования города пользователя.
    На вход принимает следующие параметры:
    1) ids - ID номер телеграмм
    2) cities - город на который необходимо изменить"""

    user_verification = session.query(User.id).filter(User.id_tg == ids)
    city_verification = session.query(City.id).filter(City.name == cities)
    user_ids = session.query(User.id).filter(User.id_tg == ids).all()[0][0]

    if session.query(city_verification.exists()).scalar():
        if session.query(user_verification.exists()).scalar():
            data_edit = session.query(User).get(user_ids)
            data_edit.city = cities
            session.add(data_edit)
            session.commit()
            return "Информация о городе обновлена"
        else:
            return "Данный пользователь отсутствует в базе"
    else:
        return "Данный город отсутствует в базе"


def notes_new(text_notes, user_id):
    new_user = Notes(text_notes=text_notes, user_id=user_id)
    session.add(new_user)
    session.commit()


def return_url(ids):
    ext_city_db = session.query(User.city).filter(User.id_tg == ids).all()[0][0]
    return session.query(City.url).filter(City.name == ext_city_db).all()[0][0]

