from pathlib import Path

from sqlalchemy import create_engine, select, Sequence
from sqlalchemy.orm import scoped_session, sessionmaker

from data_access.data_base import init_db
from data_models.models import *

class ReservationManager(object):
    def __init__(self, database_path: Path):
        self.__engine = create_engine(f'sqlite:///{database_path}', echo=False)
        self.__session = scoped_session(sessionmaker(bind=self.__engine))

    def get_all_hotels(self) -> None:
        all_hotels = self.__rm.get_all_hotels()
        self.show_hotels(all_hotels)

    def show_hotels(self, hotels: list[Hotel]) -> None:
        for hotel in hotels:
            print(f'Name: {hotel.name}, Location: {hotel.location}')


#all rooms from specific hotel?
    def get_all_rooms(self) -> list[Room]:
        query = select(Room)
        result = self.__session.execute(query).scalars().all()
        return result

#check for login
    def check_login(self, user_id: int):
        query = select(User).where(User.id == user_id)
        result = self.__session.execute(query).scalars().first()
        return result
#reservation
    def book_room(self, user_id: int, room_id: int):
        room = self.__session.get(Room, room_id)
        if not room:
            return f"Room {room_id} does not exist."

        if room.already_booked:
            return f"Room {room_id} is already booked."

        reservation = Reservation(user_id=user_id, room_id=room_id)
        room.is_booked = True
        self.__session.add(reservation)
        self.__session.commit()
        return f"Room {room_id} has been successfully booked."

    def cancel_reservation(self, user_id: int, room_id: int):

