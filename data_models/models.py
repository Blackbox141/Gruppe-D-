from __future__ import annotations

from datetime import date

from typing import List
from sqlalchemy import ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property


class Base(DeclarativeBase):
    '''
    Basis Klasse für unser Model. Daraus kann SQLAlchemy herleiten welche Klassen zu unserem Modell gehören.
    '''
    pass


class Address(Base):
    '''
    Adress Entitätstyp.
    '''
    __tablename__ = "address"
    __id: Mapped[int] = mapped_column("id", primary_key=True)
    __street: Mapped[str] = mapped_column("street")
    __zip: Mapped[str] = mapped_column("zip")
    __city: Mapped[str] = mapped_column("city")

    @hybrid_property
    def id(self) -> str:
        return self.__id

    @hybrid_property
    def street(self) -> str:
        return self.__street

    @street.setter
    def street(self, street: str) -> None:
        self.__street = street

    @hybrid_property
    def zip(self) -> str:
        return self.__zip

    @zip.setter
    def zip(self, zip: str) -> None:
        self.__zip = zip

    @hybrid_property
    def city(self) -> str:
        return self.__city

    @city.setter
    def city(self, city: str) -> None:
        self.__city = city

    def __repr__(self) -> str:
        return f"Address(id={self.__id!r}, street={self.street!r}, city={self.city!r}, zip={self.zip!r})"


class Role(Base):
    __tablename__ = "role"
    __id: Mapped[int] = mapped_column("id", primary_key=True)
    __name: Mapped[str] = mapped_column("name", unique=True)
    __access_level: Mapped[int] = mapped_column()

    @hybrid_property
    def id(self) -> int:
        return self.__id

    @hybrid_property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str) -> None:
        self.__name = name

    @hybrid_property
    def access_level(self) -> int:
        return self.__access_level

    @access_level.setter
    def access_level(self, access_level: int) -> None:
        self.__access_level = access_level

    def __repr__(self) -> str:
        return f"Role(id={self.id!r}, name={self.name!r}, access_level={self.access_level!r})"


class Login(Base):
    __tablename__ = "login"
    __id: Mapped[int] = mapped_column("id", primary_key=True)
    __username: Mapped[str] = mapped_column("username", unique=True)
    __password: Mapped[str] = mapped_column("password")
    __role_id: Mapped[int] = mapped_column("role_id", ForeignKey("role.id"))
    __role: Mapped[Role] = relationship()

    @hybrid_property
    def id(self) -> int:
        return self.__id

    @hybrid_property
    def username(self) -> str:
        return self.__username

    @username.setter
    def username(self, username: str) -> None:
        self.__username = username

    @hybrid_property
    def password(self) -> str:
        return self.__password

    @password.setter
    def password(self, password: str) -> None:
        self.__password = password

    @hybrid_property
    def role(self) -> Role:
        return self.__role

    @role.setter
    def role(self, role: Role) -> None:
        self.__role = role

    def __repr__(self):
        return f"Login(id={self.id!r}, username={self.username!r}, password={self.password!r}, role={self.role!r})"


class Guest(Base):
    '''
    Gast Entitätstyp.
    '''
    __tablename__ = "guest"
    __id: Mapped[int] = mapped_column("id", primary_key=True)
    __firstname: Mapped[str] = mapped_column("firstname")
    __lastname: Mapped[str] = mapped_column("lastname")
    __email: Mapped[str] = mapped_column("email")
    __address_id: Mapped[int] = mapped_column("address_id", ForeignKey("address.id"))
    __address: Mapped["Address"] = relationship()
    __bookings: Mapped[List["Booking"]] = relationship(backref="guest")

    type: Mapped[str]
    __mapper_args__ = {
        "polymorphic_identity": "guest",
        "polymorphic_on": "type",
    }

    @hybrid_property
    def id(self) -> int:
        return self.__id

    @hybrid_property
    def firstname(self) -> str:
        return self.__firstname

    @firstname.setter
    def firstname(self, firstname: str) -> None:
        self.__firstname = firstname

    @hybrid_property
    def lastname(self) -> str:
        return self.__lastname

    @lastname.setter
    def lastname(self, lastname: str) -> None:
        self.__lastname = lastname

    @hybrid_property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, email: str) -> None:
        self.__email = email

    @hybrid_property
    def address(self) -> Address:
        return self.__address

    @address.setter
    def address(self, address: Address) -> None:
        self.__address = address

    @hybrid_property
    def bookings(self) -> List["Booking"]:
        return self.__bookings

    @bookings.setter
    def bookings(self, bookings: List["Booking"]) -> None:
        self.__bookings = bookings

    def __repr__(self) -> str:
        return f"Guest(id={self.id!r}, firstname={self.firstname!r}, lastname={self.lastname!r}, address={self.address!r})"


class RegisteredGuest(Guest):
    '''
    Registrier Gast Entitätstyp.
    '''
    __tablename__ = "registred_guest"
    __id: Mapped[int] = mapped_column("id", ForeignKey("guest.id"), primary_key=True)
    __login_id: Mapped[int] = mapped_column("login_id", ForeignKey("login.id"))
    __login: Mapped[Login] = relationship()

    __mapper_args__ = {
        "polymorphic_identity": "registered"
    }

    @hybrid_property
    def id(self) -> int:
        return self.__id

    @hybrid_property
    def login(self) -> Login:
        return self.__login

    @login.setter
    def login(self, login: Login) -> None:
        self.__login = login

    def __repr__(self) -> str:
        return f"RegisteredGuest(id={self.id!r}, firstname={self.firstname!r}, lastname={self.lastname!r}, email={self.email!r}, address={self.address!r})"


class Hotel(Base):
    '''
    Hotel Entitätstyp.
    '''
    __tablename__ = "hotel"
    __id: Mapped[int] = mapped_column("id", primary_key=True)
    __name: Mapped[str] = mapped_column("name")
    __stars: Mapped[int] = mapped_column("stars", default=0)
    __address_id: Mapped[int] = mapped_column("address_id", ForeignKey("address.id"))
    __address: Mapped["Address"] = relationship()
    __rooms: Mapped[List["Room"]] = relationship(backref="hotel")

    @hybrid_property
    def id(self) -> int:
        return self.__id

    @hybrid_property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name) -> None:
        self.__name = name

    @hybrid_property
    def stars(self) -> int:
        return self.__stars

    @stars.setter
    def stars(self, stars: int) -> None:
        self.__stars = stars

    @hybrid_property
    def address(self) -> Address:
        return self.__address

    @address.setter
    def address(self, address: Address) -> None:
        self.__address = address

    @hybrid_property
    def rooms(self) -> List["Room"]:
        return self.__rooms

    @rooms.setter
    def rooms(self, rooms: List["Room"]) -> None:
        self.__rooms = rooms

    def __repr__(self) -> str:
        return f"Hotel(id={self.id!r}, name={self.name!r}, stars={self.stars}, address={self.address})"




class RoomType(Base):
    '''
    Raumtyp Entitätstyp.
    '''
    __tablename__ = "room_type"
    __id: Mapped[int] = mapped_column("id", primary_key=True)
    __description: Mapped[str] = mapped_column("description", unique=True)

    @hybrid_property
    def id(self) -> int:
        return self.__id

    @hybrid_property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, description: str) -> None:
        self.__description = description

    def __repr__(self) -> str:
        return f"RoomType(id={self.id!r}, description={self.description!r})"


class Amenity(Base):
    '''
    Einrichtung Entitätstyp.
    '''
    __tablename__ = "amenity"
    __id: Mapped[int] = mapped_column("id", primary_key=True)
    __description: Mapped[str] = mapped_column("description", unique=True)

    @hybrid_property
    def id(self) -> int:
        return self.__id

    @hybrid_property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, description: str) -> None:
        self.__description = description

    def __repr__(self) -> str:
        return f"Amenity(id={self.id!r}, description={self.description!r})"


class RoomAmenity(Base):
    __tablename__ = "room_amenity"
    __room_hotel_id: Mapped[int] = mapped_column("room_hotel_id", primary_key=True)
    __room_number: Mapped[str] = mapped_column("room_number", primary_key=True)
    __amenity_id: Mapped[int] = mapped_column(ForeignKey("amenity.id"), primary_key=True)

    __table_args__ = (
        ForeignKeyConstraint(
            ['room_hotel_id', 'room_number'],
            ['room.hotel_id', 'room.number'],
        ),
    )


class Room(Base):
    '''
    Raum Entitätstyp.
    '''
    __tablename__ = "room"
    __hotel_id: Mapped[int] = mapped_column("hotel_id", ForeignKey("hotel.id"), primary_key=True)
    __hotel: Mapped["Hotel"] = relationship(backref="rooms")
    __number: Mapped[str] = mapped_column("number", primary_key=True)
    __type_id: Mapped[str] = mapped_column("type_id", ForeignKey("room_type.id"))
    __type: Mapped["RoomType"] = relationship()
    __max_guests: Mapped[int] = mapped_column("max_guests")
    __description: Mapped[str] = mapped_column("description")
    __amenities: Mapped[List["Amenity"]] = relationship(secondary='room_amenity')
    __price: Mapped[float] = mapped_column("price")

    @hybrid_property
    def hotel(self) -> "Hotel":
        return self.__hotel

    @hotel.setter
    def hotel(self, hotel: "Hotel") -> None:
        self.__hotel = hotel

    @hybrid_property
    def number(self) -> str:
        return self.__number

    @number.setter
    def number(self, number: str) -> None:
        self.__number = number

    @hybrid_property
    def type(self) -> "RoomType":
        return self.__type

    @number.setter
    def type(self, _type: "RoomType") -> None:
        self.__type = _type

    @hybrid_property
    def max_guests(self) -> int:
        return self.__max_guests

    @max_guests.setter
    def max_guests(self, max_guests: int) -> None:
        self.__max_guests = max_guests

    @hybrid_property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, description: str) -> None:
        self.__description = description

    @hybrid_property
    def amenities(self) -> List["Amenity"]:
        return self.__amenities

    @amenities.setter
    def amenities(self, amenities:List["Amenity"]) -> None:
        self.__amenities = amenities

    @hybrid_property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, price: float) -> None:
        self.__price = price

    def __repr__(self) -> str:
        return f"Room(hotel={self.hotel!r}, room_number={self.number!r}, type={self.type!r}, description={self.description!r}, price={self.price!r})"


class Booking(Base):
    __tablename__ = "booking"

    __id: Mapped[int] = mapped_column("id", primary_key=True)
    __room_hotel_id: Mapped[int] = mapped_column("room_hotel_id")
    __room_number: Mapped[str] = mapped_column("room_number")
    __room: Mapped["Room"] = relationship()
    __guest_id: Mapped[int] = mapped_column("guest_id", ForeignKey("guest.id"))
    __guest: Mapped["Guest"] = relationship()
    __number_of_guests: Mapped[int] = mapped_column("number_of_guests")
    __start_date: Mapped[date] = mapped_column("start_date")
    __end_date: Mapped[date] = mapped_column("end_date")
    __comment: Mapped[str] = mapped_column("comment", nullable=True)

    @hybrid_property
    def id(self) -> int:
        return self.__id

    @hybrid_property
    def room(self) -> "Room":
        return self.__room

    @room.setter
    def room(self, room: Room) -> None:
        self.__room = room

    @hybrid_property
    def guest(self) -> "Guest":
        return self.__guest

    @guest.setter
    def guest(self, guest: Guest) -> None:
        self.__guest = guest

    @hybrid_property
    def number_of_guests(self) -> int:
        return self.__number_of_guests

    @number_of_guests.setter
    def number_of_guests(self, number_of_guests: int) -> None:
        self.__number_of_guests = number_of_guests

    @hybrid_property
    def start_date(self) -> date:
        return self.__start_date

    @start_date.setter
    def start_date(self, start_date: date) -> None:
        self.__start_date = start_date

    @hybrid_property
    def end_date(self) -> date:
        return self.__end_date

    @end_date.setter
    def end_date(self, end_date: date) -> None:
        self.__end_date = end_date

    @hybrid_property
    def comment(self) -> str:
        return self.__comment

    @comment.setter
    def comment(self, comment: str) -> None:
        self.__comment = comment

    __table_args__ = (
        ForeignKeyConstraint(
            ['room_hotel_id', 'room_number'],
            ['room.hotel_id', 'room.number'],
        ),
    )

    def __repr__(self) -> str:
        return f"Booking(room={self.room!r}, guest={self.guest!r}, start_date={self.start_date!r}, end_date={self.end_date!r}, comment={self.comment!r})"
