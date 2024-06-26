from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, joinedload
from datetime import datetime, date

from data_models.models import Booking, Room, Guest, Address, RegisteredGuest, Hotel


# Verwaltung der Zimmerbuchungen einschliesslich Buchung, Aktualisierung und Stornos
class ReservationManager:

    # Konstruktor des ReservationManagers
    def __init__(self, db_path: Path):
        self.__engine = create_engine(f'sqlite:///{db_path}', echo=False)
        self.__session = scoped_session(sessionmaker(bind=self.__engine))

    # Buchung eines Zimmers für registrierte Benutzer
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

    # Buchung eines Zimmers für Gäste
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

    # Berechnung des Gesamtpreises einer Buchung
    def calculate_total_price(self, room_price, start_date, end_date):
        start_date = start_date if isinstance(start_date, (datetime, date)) else datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = end_date if isinstance(end_date, (datetime, date)) else datetime.strptime(end_date, '%Y-%m-%d').date()
        num_days = (end_date - start_date).days
        return room_price * num_days

    # Erstellung einer Buchungsbestätigung
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

    # Rückgabe von Buchungen eines Benutzers
    def get_bookings_by_user(self, user_id):
        guest_id_query = (
            self.__session.query(RegisteredGuest.id)
            .filter(RegisteredGuest.login_id == user_id)
            .scalar_subquery()
        )

        booking_query = (
            self.__session.query(Booking)
            .options(joinedload(Booking.room).joinedload(Room.hotel))
            .filter(Booking.guest_id == guest_id_query)
        )

        bookings = booking_query.all()
        return bookings

    # Anzeige aller Buchungen
    def show_all_bookings(self):
        bookings = self.__session.query(Booking).options(joinedload(Booking.room)).all()
        if not bookings:
            print("No bookings found.")
        for booking in bookings:
            print(f"Booking ID: {booking.id}, Guest ID: {booking.guest_id}, Room: {booking.room.number}, Hotel ID: {booking.room.hotel_id}, Start Date: {booking.start_date}, End Date: {booking.end_date}")

    # Return von anstehender Buchungen eines Benutzers
    def get_user_future_bookings(self, user_id):
        guest_id_query = (
            self.__session.query(RegisteredGuest.id)
            .filter(RegisteredGuest.login_id == user_id)
            .scalar_subquery()
        )
        today = date.today()
        booking_query = (
            self.__session.query(Booking)
            .options(joinedload(Booking.room).joinedload(Room.hotel))
            .filter(Booking.guest_id == guest_id_query)
            .filter(Booking.start_date > today)
        )

        bookings = booking_query.all()
        return bookings

    # Aktualisierung einer Buchung mit Berücksichtigung, ob der Raum an den geänderten Daten auch verfügbar ist
    def update_booking(self, booking_id, user_id, new_start_date, new_end_date):
        booking = self.__session.query(Booking).filter(Booking.id == booking_id).first()
        if not booking:
            return False, "Booking not found."

        overlapping_bookings = (
            self.__session.query(Booking)
            .filter(Booking.room_hotel_id == booking.room_hotel_id)
            .filter(Booking.room_number == booking.room_number)
            .filter(Booking.id != booking.id)
            .filter(
                (Booking.start_date <= new_end_date) &
                (Booking.end_date >= new_start_date)
            )
            .all()
        )

        if overlapping_bookings:
            return False, "The room is not available for the selected dates."
        original_start_date = booking.start_date
        original_end_date = booking.end_date
        booking.start_date = new_start_date
        booking.end_date = new_end_date
        self.__session.flush()  # Flush anstelle von commit für temporäres Update

        return True, "Booking dates updated. Please confirm to save changes."

    # Bestätigung der Änderungen einer Buchung
    def confirm_update_booking(self, booking_id, new_start_date, new_end_date):
        booking = self.__session.query(Booking).filter(Booking.id == booking_id).first()
        if booking:
            booking.start_date = new_start_date
            booking.end_date = new_end_date
            self.__session.commit()
            return True, "Booking successfully updated."
        else:
            return False, "Booking not found."

    # Buchungsaktualisierung rückgängig machen
    def rollback_update_booking(self, booking_id, original_start_date, original_end_date):
        booking = self.__session.query(Booking).filter(Booking.id == booking_id).first()
        if booking:
            booking.start_date = original_start_date
            booking.end_date = original_end_date
            self.__session.commit()
            return True, "Booking rolled back to original dates."
        else:
            return False, "Booking not found."

    # Löschung einer Buchung
    def delete_booking(self, booking_id):
        booking = self.__session.query(Booking).filter(Booking.id == booking_id).first()
        if booking:
            self.__session.delete(booking)
            self.__session.commit()
            return True
        else:
            return False