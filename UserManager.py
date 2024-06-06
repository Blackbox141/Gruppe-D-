# In UserManager.py

from sqlalchemy.orm import joinedload
from sqlalchemy import select
from data_models.models import Login, RegisteredGuest, Guest, Booking, Room, Address
from business.BaseManager import BaseManager
import sys


class UserManager(BaseManager):
    def __init__(self, db_file):
        super(UserManager, self).__init__(db_file)
        self._attempts = 0
        self._current_user = None

    def login(self, username, password):
        query = select(Login).where(Login.username == username, Login.password == password)
        result = self._session.execute(query).scalar_one_or_none()
        self._attempts += 1
        self._current_user = result
        return result

    def has_more_attempts(self):
        return self._attempts < 3

    def logout(self):
        self._current_user = None
        self._attempts = 0

    def get_current_user(self) -> Login:
        return self._current_user

    def is_current_user_admin(self):
        return self._current_user and self._current_user.role.access_level == sys.maxsize

    def add_user(self, username, password, firstname, lastname, email, street, zip, city):
        address = Address(street=street, zip=zip, city=city)
        self._session.add(address)
        self._session.commit()

        guest = RegisteredGuest(
            login=Login(username=username, password=password, role_id=2),  # role_id 2 for regular users
            firstname=firstname,
            lastname=lastname,
            email=email,
            address_id=address.id,
            address=address
        )
        self._session.add(guest)
        self._session.commit()
        return guest.id

    def get_booking_history(self, user_id):
        guest_id_query = (
            self._session.query(RegisteredGuest.id)
            .filter(RegisteredGuest.login_id == user_id)
            .scalar_subquery()
        )
        booking_query = (
            self._session.query(Booking)
            .options(joinedload(Booking.room).joinedload(Room.hotel))
            .filter(Booking.guest_id == guest_id_query)
        )

        bookings = booking_query.all()
        return bookings

    def update_booking(self, booking_id, start_date, end_date, number_of_guests):
        booking = self._session.query(Booking).filter(Booking.id == booking_id).first()
        if not booking:
            return False

        # Check room availability excluding the current booking
        available_rooms = self._session.query(Room).join(Booking).filter(
            Booking.room_hotel_id == booking.room_hotel_id,
            Booking.start_date <= end_date,
            Booking.end_date >= start_date,
            Booking.id != booking.id  # Exclude the current booking
        ).all()

        if booking.room_number in [room.number for room in available_rooms]:
            return False

        booking.start_date = start_date
        booking.end_date = end_date
        booking.number_of_guests = number_of_guests
        self._session.commit()
        return True

    def delete_booking(self, booking_id):
        booking = self._session.query(Booking).filter(Booking.id == booking_id).first()
        if not booking:
            return False

        self._session.delete(booking)
        self._session.commit()
        return True

    def update_user(self, user_id, **kwargs):
        guest = self._session.query(RegisteredGuest).filter(RegisteredGuest.login_id == user_id).first()
        login = guest.login if guest else None
        address = guest.address if guest else None

        if not guest or not login or not address:
            return False

        # Update login credentials
        if 'username' in kwargs and kwargs['username']:
            login.username = kwargs['username']
        if 'password' in kwargs and kwargs['password']:
            login.password = kwargs['password']

        # Update personal information
        if 'firstname' in kwargs and kwargs['firstname']:
            guest.firstname = kwargs['firstname']
        if 'lastname' in kwargs and kwargs['lastname']:
            guest.lastname = kwargs['lastname']
        if 'email' in kwargs and kwargs['email']:
            guest.email = kwargs['email']

        # Update address details
        if 'street' in kwargs and kwargs['street']:
            address.street = kwargs['street']
        if 'zip' in kwargs and kwargs['zip']:
            address.zip = kwargs['zip']
        if 'city' in kwargs and kwargs['city']:
            address.city = kwargs['city']

        self._session.commit()
        return True

    def get_user_info(self, user_id):
        guest = self._session.query(RegisteredGuest).filter(RegisteredGuest.login_id == user_id).first()
        if not guest:
            return None
        return {
            'firstname': guest.firstname,
            'lastname': guest.lastname,
            'email': guest.email,
            'street': guest.address.street,
            'zip': guest.address.zip,
            'city': guest.address.city,
            'username': guest.login.username,
            'password': guest.login.password
        }