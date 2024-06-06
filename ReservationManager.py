from pathlib import Path
import os
from sqlalchemy import create_engine, select
from sqlalchemy.orm import scoped_session, sessionmaker, joinedload
from sqlalchemy.orm import aliased
from data_models.models import Booking, Room, Guest, Address, RegisteredGuest, Hotel
from datetime import datetime, date

class ReservationManager:
    def __init__(self, db_path: Path):
        self.__engine = create_engine(f'sqlite:///{db_path}', echo=False)
        self.__session = scoped_session(sessionmaker(bind=self.__engine))

    def book_room_registered(self, user_id: int, room_number: str, hotel_id: int, start_date, end_date, number_of_guests: int):
        room = self.__session.query(Room).filter(Room.hotel_id == hotel_id, Room.number == room_number).first()
        if not room:
            raise ValueError(f"Room {room_number} in hotel {hotel_id} not found.")

        guest = self.__session.query(Guest).join(RegisteredGuest).filter(RegisteredGuest.login_id == user_id).first()
        if not guest:
            raise ValueError(f"Guest with user ID {user_id} not found.")

        booking = Booking(
            guest_id=guest.id,
            room_hotel_id=hotel_id,
            room_number=room_number,
            start_date=start_date,
            end_date=end_date,
            number_of_guests=number_of_guests
        )
        self.__session.add(booking)
        self.__session.commit()

        total_price = self.calculate_total_price(room.price, start_date, end_date)
        self.create_booking_confirmation_file(booking, guest, room, total_price)
        return booking, total_price

    def book_room_guest(self, firstname: str, lastname: str, email: str, street: str, zip_code: str, city: str, room_number: str, hotel_id: int, start_date, end_date, number_of_guests: int):
        address = Address(street=street, zip=zip_code, city=city)
        guest = Guest(firstname=firstname, lastname=lastname, email=email, address=address)

        self.__session.add(address)
        self.__session.add(guest)
        self.__session.commit()

        room = self.__session.query(Room).filter(Room.hotel_id == hotel_id, Room.number == room_number).first()
        if not room:
            raise ValueError(f"Room {room_number} in hotel {hotel_id} not found.")

        booking = Booking(
            guest_id=guest.id,
            room_hotel_id=hotel_id,
            room_number=room_number,
            start_date=start_date,
            end_date=end_date,
            number_of_guests=number_of_guests
        )
        self.__session.add(booking)
        self.__session.commit()

        total_price = self.calculate_total_price(room.price, start_date, end_date)
        self.create_booking_confirmation_file(booking, guest, room, total_price)
        return booking, total_price

    def calculate_total_price(self, room_price, start_date, end_date):
        start_date = start_date if isinstance(start_date, (datetime, date)) else datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = end_date if isinstance(end_date, (datetime, date)) else datetime.strptime(end_date, '%Y-%m-%d').date()
        num_days = (end_date - start_date).days
        return room_price * num_days

    def create_booking_confirmation_file(self, booking, guest, room, total_price):
        hotel = self.__session.query(Hotel).filter(Hotel.id == room.hotel_id).first()
        filename = f"booking_confirmation_{booking.id}.txt"
        with open(filename, 'w') as file:
            file.write("Booking Confirmation\n")
            file.write("=====================\n\n")
            file.write(f"Booking ID: {booking.id}\n")
            file.write(f"Guest Name: {guest.firstname} {guest.lastname}\n")
            file.write(f"Guest Email: {guest.email}\n")
            file.write(f"Room: {room.number}\n")
            file.write(f"Hotel: {hotel.name}\n")
            file.write(f"Hotel Address: {hotel.address.street}, {hotel.address.zip}, {hotel.address.city}\n")
            file.write(f"Start Date: {booking.start_date}\n")
            file.write(f"End Date: {booking.end_date}\n")
            file.write(f"Number of Guests: {booking.number_of_guests}\n")
            file.write(f"Total Price: {total_price}\n")
        print(f"Booking confirmation file will be created after you exit: {filename}")

    def get_bookings_by_user(self, user_id):
        # Find the guest_id using the login_id from the RegisteredGuest table
        guest_id_query = (
            self.__session.query(RegisteredGuest.id)
            .filter(RegisteredGuest.login_id == user_id)
            .scalar_subquery()
        )

        # Use the found guest_id to get the bookings
        booking_query = (
            self.__session.query(Booking)
            .options(joinedload(Booking.room).joinedload(Room.hotel))
            .filter(Booking.guest_id == guest_id_query)
        )

        bookings = booking_query.all()
        return bookings

    def show_all_bookings(self):
        bookings = self.__session.query(Booking).options(joinedload(Booking.room)).all()
        if not bookings:
            print("No bookings found.")
        for booking in bookings:
            print(f"Booking ID: {booking.id}, Guest ID: {booking.guest_id}, Room: {booking.room.number}, Hotel ID: {booking.room.hotel_id}, Start Date: {booking.start_date}, End Date: {booking.end_date}")
