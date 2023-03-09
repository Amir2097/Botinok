import sqlalchemy as sq
from sqlalchemy.orm import relationship, declarative_base
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


def user_entry(self):
    new_user = User(id_tg=self.id_tg, first_name=self.first_name)
    session.add(new_user)
    session.commit()

def notes_new(self, text_notes):
    new_user = Notes(text_notes=text_notes, user_id=self.first_name)
    session.add(new_user)
    session.commit()

user_entry()

