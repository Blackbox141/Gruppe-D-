# include all search functions here
# accept search criteria, search by various criteria
from data_access.data_base import init_db
from data_models.models import *
from pathlib import Path
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import select


if __name__ = '__main__':
    database_file = '../data_access/data_base.py'

    engine = create_engine(f'sqlite:///{database_file}', echo=False)
    database_path = Path(database_file)
    if not database_path.is_file():
        init_db(database_file, generate_example_data=True)

    session = scoped_session(sessionmaker(bind=engine))

    query = select(Hotel)
    hotels = session.execute(query).scalars.all()
    for hotel in hotels:
        print(hotel)

'''
class SearchManager:

    def accept_search_criteria(self):
        criteria = []
        return criteria

    def show_available_hotels_by_name(self, hotel_name):
        query = select(Hotel).where(Hotel.name.like('%Amaris'))


    def search_hotel_by_stars(self, stars):
        query = select(Hotel)
        print(query)
        result = session.execute(query)
        for hotel in result:
            print(hotel)  # Notice that it will be a tuple, and not the object!
        input("Press Enter to continue...")
        print("\n")
'''