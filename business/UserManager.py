# UserManager.py

from sqlalchemy.orm import joinedload
from sqlalchemy import select
from data_models.models import Login, RegisteredGuest, Guest, Booking, Room, Address
from business.BaseManager import BaseManager
import sys

# Verwaltung der Benutzer einschliesslich Login, Logout und Benutzerinformationen
class UserManager(BaseManager):

    # Konstruktor des UserManagers
    def __init__(self, db_file):
        super(UserManager, self).__init__(db_file)
        self._attempts = 0
        self._current_user = None

    # Einloggen eines Benutzers
    def login(self, username, password):
        query = select(Login).where(Login.username == username, Login.password == password)
        result = self._session.execute(query).scalar_one_or_none()
        self._attempts += 1
        self._current_user = result
        return result

    # Überprüfung, ob weitere Login-Versuche möglich sind
    def has_more_attempts(self):
        return self._attempts < 3

    # Ausloggen des aktuellen Benutzers
    def logout(self):
        self._current_user = None
        self._attempts = 0

    # Returned den aktuell eingeloggten Benutzers
    def get_current_user(self) -> Login:
        return self._current_user

    # Überprüfung, ob der aktuelle Benutzer ein Administrator ist
    def is_current_user_admin(self):
        return self._current_user and self._current_user.role.access_level == sys.maxsize

    # Hinzufügen eines neuen Benutzers
    def add_user(self, username, password, firstname, lastname, email, street, zip, city):
        address = Address(street=street, zip=zip, city=city)
        self._session.add(address)
        self._session.commit()

        guest = RegisteredGuest(
            login=Login(username=username, password=password, role_id=2),
            firstname=firstname,
            lastname=lastname,
            email=email,
            address_id=address.id,
            address=address
        )
        self._session.add(guest)
        self._session.commit()
        return guest.id

    # Aktualisieren der Benutzerdaten
    def update_user(self, user_id, **kwargs):
        guest = self._session.query(RegisteredGuest).filter(RegisteredGuest.login_id == user_id).first()
        login = guest.login if guest else None
        address = guest.address if guest else None

        if not guest or not login or not address:
            return False

        if 'username' in kwargs and kwargs['username']:
            login.username = kwargs['username']
        if 'password' in kwargs and kwargs['password']:
            login.password = kwargs['password']
        if 'firstname' in kwargs and kwargs['firstname']:
            guest.firstname = kwargs['firstname']
        if 'lastname' in kwargs and kwargs['lastname']:
            guest.lastname = kwargs['lastname']
        if 'email' in kwargs and kwargs['email']:
            guest.email = kwargs['email']
        if 'street' in kwargs and kwargs['street']:
            address.street = kwargs['street']
        if 'zip' in kwargs and kwargs['zip']:
            address.zip = kwargs['zip']
        if 'city' in kwargs and kwargs['city']:
            address.city = kwargs['city']

        self._session.commit()
        return True

    # Rückgabe der Benutzerinformationen
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

    # Überprüfung, ob ein Benutzername einmalig ist
    def is_username_unique(self, username):
        query = select(Login).where(Login.username == username)
        result = self._session.execute(query).scalar_one_or_none()
        return result is None