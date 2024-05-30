import sys

from sqlalchemy import select
from sqlalchemy.sql.functions import current_user

from data_models.models import Login, RegisteredGuest
from business.BaseManager import BaseManager

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
        if self._attempts < 3:
            return True
        else:
            return False

    def logout(self):
        self._current_user = None
        self._attempts = 0

    def get_current_user(self) -> Login:
        return self._current_user

    def get_reg_guest_of(self, login) -> RegisteredGuest:
        query = select(RegisteredGuest).where(RegisteredGuest.login_id == login.id)
        result = self._session.execute(query).scalar_one_or_none()
        return result

    def is_current_user_admin(self):
        if self._current_user:
            if self._current_user.role.access_level == sys.maxsize:
                return True
        return False

    #von Phillip