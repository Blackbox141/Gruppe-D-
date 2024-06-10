from datetime import datetime

from business.BaseManager import BaseManager
from data_models.models import Hotel, Address, Room

# Verwaltung der Hotels einschliesslich Hinzufügen, Aktualisieren und Löschen
class HotelManager(BaseManager):

    # Return eines Hotels basierend auf der ID
    def get_hotel_by_id(self, hotel_id):
        return self._session.query(Hotel).filter(Hotel.id == hotel_id).first()

    # Return eines Zimmers basierend auf der Hotel-ID und der Zimmernummer
    def get_room_by_hotel_and_number(self, hotel_id, room_number):
        return self._session.query(Room).filter(Room.hotel_id == hotel_id, Room.number == room_number).first()

    # Löschen eines Hotels
    def delete_hotel(self, hotel_id):
        hotel = self.get_hotel_by_id(hotel_id)
        if hotel:
            for room in hotel.rooms:
                self._session.delete(room)
            self._session.delete(hotel)
            self._session.commit()
            return True
        else:
            return False

    # Hinzufügen eines neuen Hotels
    def add_hotel(self, hotel_name, hotel_stars, street, zip, city, rooms):
        hotel = Hotel(
            name=hotel_name,
            stars=hotel_stars,
            address=Address(
                street=street,
                zip=zip,
                city=city),
            rooms=rooms
        )

        self._session.add(hotel)
        self._session.commit()
        return hotel

    # Return aller Hotels
    def list_hotels(self):
        return self._session.query(Hotel).all()

    # Return aller Zimmer eines Hotels
    def list_hotel_rooms(self, hotel_id):
        hotel = self._session.query(Hotel).filter(Hotel.id == hotel_id).first()
        return hotel.rooms if hotel else None

    # Aktualisierung des Hotelnamens
    def update_hotel_name(self, hotel_id, new_name):
        hotel = self.get_hotel_by_id(hotel_id)
        if hotel:
            hotel.name = new_name
            self._session.commit()
            return True
        else:
            return False

    # Aktualisierung der Hotelsterne
    def update_hotel_stars(self, hotel_id, new_stars):
        hotel = self.get_hotel_by_id(hotel_id)
        if hotel:
            hotel.stars = new_stars
            self._session.commit()
            return True
        else:
            return False


    # Aktualisierung der Hoteladresse
    def update_hotel_address(self, hotel_id, new_street, new_zip, new_city):
        hotel = self.get_hotel_by_id(hotel_id)
        if hotel:
            if not hotel.address:
                hotel.address = Address()
            hotel.address.street = new_street
            hotel.address.zip = new_zip
            hotel.address.city = new_city
            self._session.commit()
            return True
        else:
            return False

    # Aktualisierung eines Zimmers
    def update_room(self, hotel_id, room_number, new_type, new_price, new_description, new_amenities, new_max_guests):
        room = self.get_room_by_hotel_and_number(hotel_id, room_number)
        if room:
            room.type = new_type
            room.price = new_price
            room.description = new_description
            room.amenities = new_amenities
            room.max_guests = new_max_guests
            self._session.commit()
            return True
        return False

    # Hinzufügen von Zimmer zu einem Hotel
    def add_rooms_to_hotel(self, hotel_id=None):
        rooms = []
        while True:
            room_number = input("Enter room number: ")
            if hotel_id and self.room_number_exists(hotel_id, room_number):
                print("Room number already exists in this hotel. Please enter a unique room number.")
                continue

            room_type = input("Enter room type: ")
            room_price = self.validate("Enter room price: ", "Invalid price!", float)
            room_description = input("Enter room description: ")
            room_amenities = input("Enter room amenities: ")
            room_max_guests = self.validate("Enter max guests: ", "Invalid number!", int)

            room = Room(
                number=room_number,
                type=room_type,
                price=room_price,
                description=room_description,
                amenities=room_amenities,
                max_guests=room_max_guests
            )
            if hotel_id:
                room.hotel_id = hotel_id
            rooms.append(room)

            another = self.validate("Add another room? (yes/no): ", "Invalid input!", str)
            if another.lower() != 'yes':
                break

        if hotel_id:
            hotel = self.get_hotel_by_id(hotel_id)
            if hotel:
                hotel.rooms.extend(rooms)
                self._session.commit()

        return rooms

    # Überprüfung, ob eine Zimmernummer bereits existiert
    def room_number_exists(self, hotel_id, room_number):
        existing_room = self._session.query(Room).filter(Room.hotel_id == hotel_id, Room.number == room_number).first()
        return existing_room is not None

    # Validierung von Benutzereingaben, um mögliche Fehlermeldungen abzufangen
    @staticmethod
    def validate(ask_input, error_msg, type_=str, min_val=None, max_val=None, date_format=None):
        while True:
            user_input = input(ask_input)
            try:
                if date_format:
                    user_input = datetime.strptime(user_input, date_format).date()
                else:
                    user_input = type_(user_input)
                match user_input:
                    case _ if min_val is not None and user_input < min_val:
                        raise ValueError
                    case _ if max_val is not None and user_input > max_val:
                        raise ValueError
                return user_input
            except ValueError:
                print(f"\n{error_msg}\n")