import random

from sqlalchemy import ForeignKey, select, func
from sqlalchemy import String
from sqlalchemy.future import engine
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import Text
from sqlalchemy import create_engine


class Base(DeclarativeBase):
    pass
class Song(Base):
    __tablename__ = "song"
    id: Mapped[int] = mapped_column(primary_key=True)
    songName: Mapped[str] = mapped_column(String(30))
    songText: Mapped[str] = mapped_column(Text())
    author: Mapped[str] = mapped_column(String(30))
    pathMusic: Mapped[str] = mapped_column(String(50))
    genre: Mapped[str] = mapped_column(ForeignKey("genre.id"))

class Genre(Base):
    __tablename__ = "genre"
    id: Mapped[int] = mapped_column(primary_key=True)
    genre: Mapped[str] = mapped_column(String(30))

class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)
    password: Mapped[str] = mapped_column(String(30))
    wins: Mapped[int] = mapped_column()
    loses: Mapped[int] = mapped_column()


# engine = create_engine('sqlite:///myDatabase.db', echo=True)
# Base.metadata.create_all(engine)

# with Session(engine) as session:
#     genre = session.query(Genre).where(Genre.id == 1).first()
#     randomSongs = list(session.query(Song).where(Song.genre == genre.id).order_by(func.random()).limit(4))
# rightSong = randomSongs[0]
# random.shuffle(randomSongs)
# rightIndex = randomSongs.index(rightSong)
# print(rightIndex)