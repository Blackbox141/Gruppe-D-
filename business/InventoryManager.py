import sys
from pathlib import Path
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine, select

from business.DBaseManager import BaseManager
from data_access.data_base import init_db
from data_models.models import Hotel, Address, Room

class HotelManager(BaseManager):

    def delete_hotel(self, hotel_id):
        hotel = self._session.query(Hotel).filter(Hotel.id == hotel_id).first()
        if hotel:
            for room in hotel.rooms:
                self._session.delete(room)
            self._session.delete(hotel)
            self._session.commit()
            print(f"'{hotel.name}' with ID {hotel_id} has been deleted. There are now {self._session.query(Hotel).count()} hotel(s) left in the database.")
        else:
            print(f"No hotel found with ID {hotel_id}.")

    def add_hotel(self, hotel_name, hotel_stars, street, zip, city, rooms):
        hotel = Hotel(
            name=hotel_name,
            stars=hotel_stars,
            address=Address(street=street,
                            zip=zip,
                            city=city),
            rooms=rooms
        )

        self._session.add(hotel)
        self._session.commit()

        query = select(Hotel).where(Hotel.name == hotel_name)
        result = self._session.execute(query).scalars().all()
        print(result)

    def validate(self, ask_input, error_msg, type):
        while True:
            user_input = input(ask_input)
            try:
                user_input = type(user_input)
                return user_input
            except ValueError:
                print(error_msg)

    def validate_in_range(self, ask_input, error_msg, type, min, max):
        while True:
            user_input = self.validate(ask_input, error_msg, type)
            if user_input >= min and user_input <= max:
                return user_input
            else: print(error_msg)

def validate(ask_input, error_msg, type):
    while True:
        user_input = input(ask_input)
        try:
            user_input = type(user_input)
            return user_input
        except ValueError:
            print(error_msg)

def validate_in_range(ask_input, error_msg, type, min, max):
    while True:
        user_input = validate(ask_input, error_msg, type)
        if user_input >= min and user_input <= max:
            return user_input
        else: print(error_msg)


if __name__ == "__main__":
    manager = HotelManager("../data/hotel_reservation.db")

    while True:
        print("\nOptions:")
        print("1. Add a new hotel")
        print("2. Delete an existing hotel")
        print("3. Exit")
        user_choice = input("Please select an option (1-3): ")

        if user_choice == '1':
            hotel_name_input = manager.validate("Hotel Name: ", "Invalid Hotel Name!", str)
            hotel_stars_input = manager.validate_in_range("Hotel Stars: ", "Invalid Stars!", int, 0, 5)
            street_input = manager.validate("Street: ", "Invalid Street!", str)
            zip_input = manager.validate("Zip Code: ", "Invalid Zip Code!", str)
            city_input = manager.validate("City: ", "Invalid City!", str)

            room_number_input = manager.validate_in_range("Room number: ", "Invalid Room Number!", int, 1, sys.maxsize)
            room_type_input = manager.validate("Enter room type: ", "Invalid Room Type!", str)
            room_max_guests_input = manager.validate_in_range("Room max. guests: ", "Invalid Guest Number!", int, 1,
                                                              sys.maxsize)
            room_description_input = manager.validate("Room description: ", "Invalid Room Description!", str)
            room_amenities_input = manager.validate("Amenities: ", "Invalid Amenities!", str)
            room_price_input = manager.validate_in_range("Price: ", "Invalid Price!", float, 0, sys.maxsize)

            rooms = [Room(number=room_number_input,
                          type=room_type_input,
                          max_guests=room_max_guests_input,
                          description=room_description_input,
                          amenities=room_amenities_input,
                          price=room_price_input)]

            manager.add_hotel(hotel_name_input, hotel_stars_input, street_input, zip_input, city_input, rooms)

        elif user_choice == '2':
            try:
                hotel_id_input = int(input("Please enter the Hotel ID to delete: "))
                manager.delete_hotel(hotel_id_input)
            except ValueError:
                print("Invalid input. Please enter a valid integer for the Hotel ID.")
        elif user_choice == '3':
            print("Exiting the program.")
            break
        else:
            print("Invalid option selected. Please try again.")
