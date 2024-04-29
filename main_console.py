# from search import SearchManager
# from register import UserManager
from sqlalchemy import select
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker


from business.SearchManager import SearchManager
from data_access import data_loader as dl
from data_access.data_base import *
from main_hotel_mgn import HotelManager


def load_db():
    # Import relevant data classes and initialize objects for hotels, registered users, admin users and other
    # required data
    pass

def show_welcome():
    print("Welcome to hotel reservation system <customize>")
    # add more instructions or information as desired


def show_menu():
    print("Menu: ")
    print("Print 0 to search hotels based on your criteria")
    print("Print 1 to register a new user")
    print("Print 2 login as a registered user or an admin")
    print("Print x to quit the hotel reservation system")


def navigate():
    choice = input("Choose an option for your desired action: ")
    match choice:
        case 'x':
            print("Goodbye, see you soon!")
            exit()
        case '0':
            print("Search")
            # call functions in SearchManager
            searchMgr = SearchManager()
            searchMgr.search_hotel_by_stars()
        case '1':
            print("Register")
            # call functions in UserManager
        case _:
            print("No such option, please enter a valid choice as shown in the Menu")
            choice = input("Choose an option for your desired action: ")

DB_FILE = './data/hotel_reservation.db'
GENERATE_EXAMPLES = False
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # later replace with load_sqlite_db()
    #load_db()
    db_path = Path(DB_FILE)
    if not db_path.parent.exists():
        db_path.parent.mkdir()

    engine = create_engine(f'sqlite:///{db_path}')

    if db_path.exists():
        if GENERATE_EXAMPLES:
            Base.metadata.drop_all(engine)
            Base.metadata.create_all(engine)
            init_db(DB_FILE, False, True, True)
    else:
        Base.metadata.create_all(engine)

    session = scoped_session(sessionmaker(bind=engine))

    hotel_mgn = HotelManager(session)

    query = select(Hotel)
    hotels = session.execute(query).scalars().all()
    print(hotels)









    # try:
    #     dl.load_data_from_sqlite()
    # except Exception as e:
    #     print("There was a problem in loading the database, please fix the error and try again: ", e)
    # later replace with logic to show the home page GUI of your hotel
    #show_welcome()

    # can be replaced by GUI control elements to create a simple menu on the home page.
    #show_menu()

    # can be replaced with individual screens for different function like register, login, search etc.
    #navigate()

    session.close()
