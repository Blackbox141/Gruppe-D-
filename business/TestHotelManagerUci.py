from pathlib import Path
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine, select

from data_access.data_base import init_db
from data_models.models import Hotel, Address, Room

class HotelManager:
    def __init__(self, database_file):
        database_path = Path(database_file)
        if not database_path.is_file():
            init_db(database_file, generate_example_data=True)
        self.__engine = create_engine(f'sqlite:///{database_file}', echo=False)
        self.__session = scoped_session(sessionmaker(bind=self.__engine))

    def add_hotel(self):
        hotel_name_input = input("Hotel Name: ")
        hotel_stars_input = input("Hotel Stars: ")
        street_input = input("Street: ")
        zip_input = input("Zip Code: ")
        city_input = input("City: ")
        room_number_input = input("Room number: ")
        room_type_input = input("Enter room type: ")
        room_max_guests_input = input("Room max. guests: ")
        room_description_input = input("Room description: ")
        room_amenities_input = input("Amenities: ")
        room_price_input = input("Price per night: ")

        hotel = Hotel(
            name=hotel_name_input,
            stars=hotel_stars_input,
            address=Address(street=street_input,
                            zip=zip_input,
                            city=city_input),
            rooms=[Room(number=room_number_input,
                        type=room_type_input,
                        max_guests=room_max_guests_input,
                        description=room_description_input,
                        amenities=room_amenities_input,
                        price=room_price_input)]
        )

        self.__session.add(hotel)
        self.__session.commit()

        query = select(Hotel).where(Hotel.name == hotel_name_input)
        result = self.__session.execute(query).scalars().all()
        print(result)

# Example usage:
if __name__ == "__main__":
    manager = HotelManager("../data/hotel_reservation.db")
    manager.add_hotel()
