import sqlalchemy as sq
from sqlalchemy.orm import relationship, declarative_base
from extraction.ext_cityes import rec_db_cityes
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

Base = declarative_base()


class User(Base):
    __tablename__ = 'User'
    id = sq.Column(sq.Integer, primary_key=True)
    id_tg = sq.Column(sq.Integer)
    first_name = sq.Column(sq.String(length=80))
    city = sq.Column(sq.String(length=20))
    reg_date = sq.Column(sq.TIMESTAMP, nullable=False)


    def __str__(self):
        return f'User {self.id}, {self.id_tg}: {self.first_name}'


class Notes(Base):
    __tablename__ = 'Notes'
    id = sq.Column(sq.Integer, primary_key=True)
    create_date = sq.Column(sq.TIMESTAMP, nullable=False)
    text_notes = sq.Column(sq.Text)
    user_id = sq.Column(sq.Integer, sq.ForeignKey("User.id"), nullable=False)

    publisher = relationship(User, backref="notes")

    def __str__(self):
        return f'Notes {self.id}, {self.create_date}, {self.user_id}: {self.text_notes}'


class City(Base):
    __tablename__ = 'City'
    id = sq.Column(sq.Integer, primary_key=True)
    id_city = sq.Column(sq.Integer)
    name = sq.Column(sq.String(length=80))
    url = sq.Column(sq.String(length=80))

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
    for enter_city in rec_db_cityes():
        new_city = City(id_city=enter_city['ID'], name=enter_city['Name'], url=enter_city['Url'])
        session.add(new_city)
        session.commit()


def user_entry(ids, name, cities, rdate):
    user_verification = session.query(User.id).filter(User.id_tg == ids)
    if session.query(user_verification.exists()).scalar():
        print('Its good')
    else:
        new_user = User(id_tg=ids, first_name=name, city=cities, reg_date=rdate)
        session.add(new_user)
        session.commit()


def notes_new(self, text_notes):
    new_user = Notes(text_notes=text_notes, user_id=self.first_name)
    session.add(new_user)
    session.commit()
