from sqlalchemy import create_engine, select
from sqlalchemy.orm import scoped_session, sessionmaker

from data_models import User
import os
from pathlib import Path


from data_access.data_base import init_db

from data_models.models import *

class UserManager(object):
    def __init__(self) -> None:
        self.__load_db()

    def __load_db(self):
        if not os.environ.get("DB_File"):
            raise ValueError("DB_File environment variable not set")
        self.__db_filepath = Path(os.environ.get("DB_File"))

        if not self.__db_filepath.is_file():
            init_db(str(self.__db_filepath), generate_example_data=True)

        self._engine = create_engine(f"sqlite:///{self.__db_filepath}")
        self._session = scoped_session(sessionmaker(bind=self._engine))

    def add_user(self, username, password):
        # füge einen neuen Benutzer zur Datenbank hinzu
        new_user = Login(username=username, password=password)
        self._session.add(new_user)
        self._session.commit()
        return new_user.id

    def authenticate_user(self, username, password):
        # überprüfe die Anmeldeinformationen eines Benutzers
        query = select(Login).where(Login.username == username).where(Login.password == password)
        result = self._session.execute(query).scalars().one_or_none()
        return result


if __name__ == "__main__":
    os.environ["DB_File"] = "../data/example_data.db"
    manager = UserManager()

    username = "test"
    password = "SuperSecret"
    result = manager.authenticate_user(username, password)
    if not result:
        print("Wrong Username or Password")
    else:
        print(f"Welcome {result.username}!")

#get booking history(self, user_id)
    #def get_booking_history(self,user_id):
        #session = self._session()
        #query = select(get_booking_history).where(booking.user_id == user_id)
        #result = not session.execute(query).scalars().all()
        #return result

#change_booking
