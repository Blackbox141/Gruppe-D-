from pathlib import Path

from sqlalchemy import create_engine, select, Sequence
from sqlalchemy.orm import scoped_session, sessionmaker

from data_access.data_base import init_db
from data_models.models import *

class ReservationManager(object):
    def __init__(self, database_path: Path):
        self.__engine = create_engine(f'sqlite:///{database_path}', echo=False)
        self.__session = scoped_session(sessionmaker(bind=self.__engine))

    def show_all_hotels(self) -> None:
        all_hotels = self.__rm.get_all_hotels()
        self.show_hotels(all_hotels)
    def get_all_rooms(self) -> list[Room]:
        query = select(Room)
        result = self.__session.execute(query).scalars().all()
        return result
#hello

