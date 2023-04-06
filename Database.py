from pprint import pprint

from sqlalchemy.orm import relationship, declarative_base
from extraction.ext_cityes import rec_db_cityes
from extraction.ext_events import event_3day
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


class Event(Base):

    __tablename__ = 'Event'

    id = sq.Column(sq.Integer, primary_key=True)
    last_update = sq.Column(sq.DateTime, default=datetime.datetime.utcnow)
    date = sq.Column(sq.String(length=80))
    tepe = sq.Column(sq.String(length=80))
    genre = sq.Column(sq.String(length=80))
    discription = sq.Column(sq.String(length=150))
    poster = sq.Column(sq.String(length=150))
    link = sq.Column(sq.String(length=150))
    cityes_id = sq.Column(sq.Integer, sq.ForeignKey("City.id"), nullable=False)
    cityes = relationship(City, backref="event")

    def __str__(self):
        return f'Event {self.id}, {self.date}, {self.tepe}, {self.genre},' \
               f' {self.discription}, {self.poster}, {self.link}'


def create_tables(engine):
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


DSN = f'postgresql+psycopg2://{os.getenv("DATABASE_USER")}:{os.getenv("DATABASE_PASSWORD")}' \
      f'@{os.getenv("HOST")}:{os.getenv("DATABASE_PORT")}/{os.getenv("DATABASE_NAME")}'
engine = sq.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()


def event_entry(ids):
    """
    Функция добавления мероприятий проводящихся в городе
    :param ids: ID пользователя
    :return: Заполнение базы данных мероприятий по определенному городу
    """
    url = return_url(ids)
    data_event = event_3day(url)
    user_ids = session.query(User.city).filter(User.id_tg == ids).all()[0][0]
    city_id = session.query(City.id).filter(City.name == user_ids).all()[0][0]
    standart_date_now = datetime.datetime.now()
    last_update_date = session.query(Event.last_update).filter(Event.cityes_id == city_id).first()
    count_city = session.query(Event.last_update).filter(Event.cityes_id == city_id).count()
    delta_list = []

    try:
        for tiiime in last_update_date:
            delta_time = standart_date_now - tiiime
            delta_list.append(delta_time.seconds)
    except TypeError:
        delta_list.append(86400)

    if delta_list[0] >= 86400 or count_city == 0:

        if count_city > 0:
            session.query(Event).filter(Event.cityes_id == city_id).delete()
            session.commit()

        for data_event_list in data_event:
            genres_list = data_event_list['genre']
            genres = ', '.join(genres_list)

            if genres == "":
                genres = "None"

            new_event = Event(last_update=standart_date_now,
                              date=data_event_list['data'][0],
                              tepe=data_event_list['type'][0],
                              genre=genres,
                              discription=data_event_list['discription'][0],
                              poster=data_event_list['poster'][0],
                              link=data_event_list['link'][0],
                              cityes_id=city_id)

            session.add(new_event)
            session.commit()

        return True

    else:
        return False


def conclusion_event(ids):
    """
    Функция вывода информации о проводимых мероприятиях в определенном городе конечному пользователю
    :param ids: Телеграм ID пользователя
    :return: Список со всеми мероприятиями
    """
    event_entry(ids)  # При каждом запросе дергаем данную функцию для обновления информации
    user_ids = session.query(User.city).filter(User.id_tg == ids).all()[0][0]
    city_id = session.query(City.id).filter(City.name == user_ids).all()[0][0]
    list_event_user = session.query(Event.date, Event.genre, Event.discription, Event.poster, Event.link) \
        .filter(Event.cityes_id == city_id).all()

    return list_event_user


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
        pass
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

            try:
                session.commit()
            except:
                session.rollback()

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
    ext_city_db = session.query(User).filter(User.id_tg == ids).first()
    url_city_db = session.query(City).filter(City.name == ext_city_db.city).first()
    return url_city_db.url


def return_city(ids):
    ext_city_db = session.query(User).filter(User.id_tg == ids).first()
    name_city_db = session.query(City.name).filter(City.name == ext_city_db.city).first()
    return name_city_db


# TODO: Заготовка под клавиатуру ввода города
def rerurn_alp_cuty():
    alphabet = ''.join([chr(i) for i in range(ord('а'), ord('а') + 32)])
    city_sort_dict = {}
    for alphabet_one in alphabet:
        cyty_for_alp = session.query(City.name).filter(City.name.ilike(alphabet_one + '%')).all()
        city_sort_list = []
        for sorting_city_alpha in cyty_for_alp:
            city_sort_list.append(sorting_city_alpha[0])

        city_sort_dict[alphabet_one] = city_sort_list

    for keys_city in city_sort_dict.copy():
        if not city_sort_dict[keys_city]:
            city_sort_dict.pop(keys_city)
    return city_sort_dict
