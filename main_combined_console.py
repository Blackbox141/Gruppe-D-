# main_combined_console.py

from datetime import datetime
from business.UserManager import UserManager
from business.HotelManager import HotelManager
from business.SearchManager import SearchManager
from business.ReservationManager import ReservationManager
import os

def show_hotels(hotels, search_manager, start_date=None, end_date=None, number_of_guests=None):
    for hotel in hotels:
        print(f"\n\n================== Hotel ID: {hotel.id} ==================")
        print(f"\nName: {hotel.name}, Stars: {hotel.stars}, Address: {hotel.address.street}, {hotel.address.zip}, {hotel.address.city}")
        print("--------------------------------------------------------------")
        rooms = search_manager.get_available_rooms(hotel.id, start_date, end_date, number_of_guests) if start_date and end_date else hotel.rooms
        for room in rooms:
            print(f"Room Number: {room.number}, Type: {room.type}, Price: {room.price}, Max Guests: {room.max_guests}")

def main_menu():
    print("\n================== Main Menu ==================")
    print("1. Login")
    print("2. Register")
    print("3. Continue as guest")
    print("4. Exit")
    return HotelManager.validate("Please select an option (1-4): ", "Invalid option!", int, 1, 4)

def admin_menu():
    print("\n================== Admin Menu ==================")
    print("1. Add Hotel")
    print("2. Delete Hotel")
    print("3. Update Hotel")
    print("4. List Hotels")
    print("5. Show All Bookings")
    print("6. Logout")
    return HotelManager.validate("Please select an option (1-6): ", "Invalid option!", int, 1, 6)

def user_menu():
    print("\n================== User Menu ==================")
    print("1. Search for Hotels")
    print("2. View all bookings")
    print("3. Edit Account")
    print("4. Logout")
    return HotelManager.validate("Please select an option (1-4): ", "Invalid option!", int, 1, 4)

def update_booking_menu():
    print("\n================== Update Booking Menu ==================")
    print("1. Update Start Date")
    print("2. Update End Date")
    print("3. Update Both Start and End Date")
    print("4. Cancel Booking")
    print("5. Exit")
    return HotelManager.validate("Please select an option (1-5): ", "Invalid option!", int, 1, 5)

def display_booking_info(booking, reservation_manager):
    total_price = reservation_manager.calculate_total_price(booking.room.price, booking.start_date, booking.end_date)
    print(f"\nBooking ID: {booking.id}\nHotel: {booking.room.hotel.name}\nRoom Number: {booking.room.number}\nStart Date: {booking.start_date}\nEnd Date: {booking.end_date}\nTotal Price: {total_price}\n")

def display_user_info(user_info):
    print("\n================== Current User Info ==================")
    print(f"First Name: {user_info['firstname']}")
    print(f"Last Name: {user_info['lastname']}")
    print(f"Email: {user_info['email']}")
    print(f"Street: {user_info['street']}")
    print(f"Zip: {user_info['zip']}")
    print(f"City: {user_info['city']}")
    print(f"Username: {user_info['username']}")
    print(f"Password: {user_info['password']}")
    print("-------------------------------------------------------")

def update_account_menu():
    print("\n================== Update Account Menu ==================")
    print("1. Update First Name")
    print("2. Update Last Name")
    print("3. Update Email")
    print("4. Update Street")
    print("5. Update Zip")
    print("6. Update City")
    print("7. Update Username")
    print("8. Update Password")
    print("9. Exit")
    return HotelManager.validate("Please select an option (1-9): ", "Invalid option!", int, 1, 9)

def get_start_and_end_date():
    while True:
        start_date = HotelManager.validate("Enter start date (YYYY-MM-DD): ", "Invalid date!", str, date_format='%Y-%m-%d')
        end_date = HotelManager.validate("Enter end date (YYYY-MM-DD): ", "Invalid date!", str, date_format='%Y-%m-%d')
        if start_date <= datetime.now().date() or end_date <= datetime.now().date():
            print("\nStart date and end date must be in the future.\n")
            continue
        if end_date < start_date:
            start_date, end_date = end_date, start_date
        return start_date, end_date

def search_and_book_hotel(user_manager, reservation_manager, search_manager, is_guest=False):
    start_date, end_date = get_start_and_end_date()
    number_of_guests = HotelManager.validate("Enter number of guests: ", "Invalid number!", int)

    city = input("Enter city (optional): ")
    stars = input("Enter hotel stars (optional): ")

    hotels = search_manager.get_hotels(city=city if city else None, stars=int(stars) if stars else None)
    filtered_hotels = []
    for hotel in hotels:
        available_rooms = search_manager.get_available_rooms(hotel.id, start_date, end_date, number_of_guests)
        if available_rooms:
            filtered_hotels.append(hotel)
    if not filtered_hotels:
        print("\nNo hotels found matching the criteria.\n")
        return
    show_hotels(filtered_hotels, search_manager, start_date, end_date, number_of_guests)

    hotel_id = HotelManager.validate("\nEnter hotel ID to book: ", "Invalid ID!", int)
    room_number = HotelManager.validate("Enter room number to book: ", "Invalid number!", str)

    if is_guest:
        firstname = input("Enter your first name: ")
        lastname = input("Enter your last name: ")
        email = input("Enter your email: ")
        street = input("Enter your street: ")
        zip_code = input("Enter your zip code: ")
        city = input("Enter your city: ")
        booking, total_price = reservation_manager.book_room_guest(
            firstname,
            lastname,
            email,
            street,
            zip_code,
            city,
            room_number,
            hotel_id,
            start_date,
            end_date,
            number_of_guests
        )
    else:
        current_user = user_manager.get_current_user()
        if not current_user:
            print("\nYou need to be logged in to book a room.\n")
            return
        booking, total_price = reservation_manager.book_room_registered(
            current_user.id,
            room_number,
            hotel_id,
            start_date,
            end_date,
            number_of_guests
        )

    display_booking_info(booking, reservation_manager)
    confirm_booking = HotelManager.validate("Confirm booking? (yes/no): ", "Invalid input!", str)
    if confirm_booking.lower() == 'yes':
        print(f"\nBooking confirmed. Thanks for your booking!\nConfirmation file will be created after you exit: booking_confirmation_{booking.id}.txt\n")
    else:
        reservation_manager.delete_booking(booking.id)
        print("\nBooking was not confirmed and has been cancelled.\n")

if __name__ == "__main__":
    db_path = os.path.join(os.path.dirname(__file__), "data/hotel_reservation.db")
    if not os.path.exists(db_path):
        print(f"Database file not found: {db_path}")
    else:
        print(f"Using database file: {db_path}")

    user_manager = UserManager(db_path)
    hotel_manager = HotelManager(db_path)
    search_manager = SearchManager(db_path)
    reservation_manager = ReservationManager(db_path)

    def user_menu_loop():
        while True:
            user_choice = user_menu()
            match user_choice:
                case 1:
                    search_and_book_hotel(user_manager, reservation_manager, search_manager)
                case 2:
                    while True:
                        bookings = reservation_manager.get_bookings_by_user(user_manager.get_current_user().id)
                        if bookings:
                            print("\n================== Your Bookings ==================")
                            for booking in bookings:
                                display_booking_info(booking, reservation_manager)
                            modify = HotelManager.validate("Do you want to modify any future booking? (yes/no): ", "Invalid input!", str)
                            if modify.lower() == 'yes':
                                future_bookings = reservation_manager.get_user_future_bookings(user_manager.get_current_user().id)
                                if future_bookings:
                                    print("\n================== Your Future Bookings ==================")
                                    for booking in future_bookings:
                                        display_booking_info(booking, reservation_manager)
                                    booking_id = HotelManager.validate("Enter the Booking ID to modify: ", "Invalid ID!", int)
                                    selected_booking = next((b for b in future_bookings if b.id == booking_id), None)
                                    if not selected_booking:
                                        print("\nInvalid Booking ID.\n")
                                        continue

                                    while True:
                                        update_booking_choice = update_booking_menu()
                                        match update_booking_choice:
                                            case 1:
                                                new_start_date = HotelManager.validate("Enter new start date (YYYY-MM-DD): ", "Invalid date!", str, date_format='%Y-%m-%d')
                                                if new_start_date > selected_booking.end_date:
                                                    new_start_date, selected_booking.end_date = selected_booking.end_date, new_start_date
                                                success, message = reservation_manager.update_booking(booking_id, user_manager.get_current_user().id, new_start_date, selected_booking.end_date)
                                                if success:
                                                    display_booking_info(next(b for b in reservation_manager.get_user_future_bookings(user_manager.get_current_user().id) if b.id == booking_id), reservation_manager)
                                                    confirm = HotelManager.validate("Confirm the changes? (yes/no): ", "Invalid input!", str)
                                                    if confirm.lower() == 'yes':
                                                        reservation_manager.confirm_update_booking(booking_id, new_start_date, selected_booking.end_date)
                                                        print("\nBooking successfully updated.\n")
                                                    else:
                                                        reservation_manager.rollback_update_booking(booking_id, selected_booking.start_date, selected_booking.end_date)
                                                        print("\nChanges were not made.\n")
                                                    break
                                                else:
                                                    print(f"\n{message}\n")
                                            case 2:
                                                new_end_date = HotelManager.validate("Enter new end date (YYYY-MM-DD): ", "Invalid date!", str, date_format='%Y-%m-%d')
                                                if new_end_date < selected_booking.start_date:
                                                    selected_booking.start_date, new_end_date = new_end_date, selected_booking.start_date
                                                success, message = reservation_manager.update_booking(booking_id, user_manager.get_current_user().id, selected_booking.start_date, new_end_date)
                                                if success:
                                                    display_booking_info(next(b for b in reservation_manager.get_user_future_bookings(user_manager.get_current_user().id) if b.id == booking_id), reservation_manager)
                                                    confirm = HotelManager.validate("Confirm the changes? (yes/no): ", "Invalid input!", str)
                                                    if confirm.lower() == 'yes':
                                                        reservation_manager.confirm_update_booking(booking_id, selected_booking.start_date, new_end_date)
                                                        print("\nBooking successfully updated.\n")
                                                    else:
                                                        reservation_manager.rollback_update_booking(booking_id, selected_booking.start_date, selected_booking.end_date)
                                                        print("\nChanges were not made.\n")
                                                    break
                                                else:
                                                    print(f"\n{message}\n")
                                            case 3:
                                                new_start_date, new_end_date = get_start_and_end_date()
                                                success, message = reservation_manager.update_booking(booking_id, user_manager.get_current_user().id, new_start_date, new_end_date)
                                                if success:
                                                    display_booking_info(next(b for b in reservation_manager.get_user_future_bookings(user_manager.get_current_user().id) if b.id == booking_id), reservation_manager)
                                                    confirm = HotelManager.validate("Confirm the changes? (yes/no): ", "Invalid input!", str)
                                                    if confirm.lower() == 'yes':
                                                        reservation_manager.confirm_update_booking(booking_id, new_start_date, new_end_date)
                                                        print("\nBooking successfully updated.\n")
                                                    else:
                                                        reservation_manager.rollback_update_booking(booking_id, selected_booking.start_date, selected_booking.end_date)
                                                        print("\nChanges were not made.\n")
                                                    break
                                                else:
                                                    print(f"\n{message}\n")
                                            case 4:
                                                confirm_cancel = HotelManager.validate("Are you sure you want to cancel this booking? (yes/no): ", "Invalid input!", str)
                                                if confirm_cancel.lower() == 'yes':
                                                    success = reservation_manager.delete_booking(booking_id)
                                                    if success:
                                                        print("\nBooking successfully canceled.\n")
                                                    else:
                                                        print("\nFailed to cancel booking.\n")
                                                break
                                            case 5:
                                                break
                                else:
                                    print("\nNo future bookings found.\n")
                            else:
                                print("\nNo modifications made.\n")
                        else:
                            print("\nNo bookings found.\n")
                        break

                case 3:
                    current_user_info = user_manager.get_user_info(user_manager.get_current_user().id)
                    if current_user_info:
                        display_user_info(current_user_info)
                    else:
                        print("\nFailed to retrieve current user info.\n")

                    while True:
                        update_account_choice = update_account_menu()
                        match update_account_choice:
                            case 1:
                                firstname = input("Enter new first name: ")
                                success = user_manager.update_user(user_manager.get_current_user().id, firstname=firstname)
                                print("\nFirst name updated." if success else "\nFailed to update first name.\n")
                            case 2:
                                lastname = input("Enter new last name: ")
                                success = user_manager.update_user(user_manager.get_current_user().id, lastname=lastname)
                                print("\nLast name updated." if success else "\nFailed to update last name.\n")
                            case 3:
                                email = input("Enter new email: ")
                                success = user_manager.update_user(user_manager.get_current_user().id, email=email)
                                print("\nEmail updated." if success else "\nFailed to update email.\n")
                            case 4:
                                street = input("Enter new street: ")
                                success = user_manager.update_user(user_manager.get_current_user().id, street=street)
                                print("\nStreet updated." if success else "\nFailed to update street.\n")
                            case 5:
                                zip_code = input("Enter new zip code: ")
                                success = user_manager.update_user(user_manager.get_current_user().id, zip=zip_code)
                                print("\nZip code updated." if success else "\nFailed to update zip code.\n")
                            case 6:
                                city = input("Enter new city: ")
                                success = user_manager.update_user(user_manager.get_current_user().id, city=city)
                                print("\nCity updated." if success else "\nFailed to update city.\n")
                            case 7:
                                while True:
                                    username = input("Enter new username: ")
                                    if user_manager.is_username_unique(username):
                                        success = user_manager.update_user(user_manager.get_current_user().id, username=username)
                                        print("\nUsername updated." if success else "\nFailed to update username.\n")
                                        break
                                    else:
                                        print("\nUsername is already taken. Please choose another one.\n")
                            case 8:
                                password = input("Enter new password: ")
                                success = user_manager.update_user(user_manager.get_current_user().id, password=password)
                                print("\nPassword updated." if success else "\nFailed to update password.\n")
                            case 9:
                                break

                    updated_user_info = user_manager.get_user_info(user_manager.get_current_user().id)
                    if updated_user_info:
                        display_user_info(updated_user_info)
                    else:
                        print("\nFailed to retrieve updated user info.\n")

                case 4:
                    user_manager.logout()
                    break

    while True:
        choice = main_menu()

        match choice:
            case 1:
                while user_manager.has_more_attempts():
                    username = input("Enter username: ")
                    password = input("Enter password: ")
                    user = user_manager.login(username, password)
                    if user:
                        print(f"\nLogin successful!\nWelcome back, {username}!\n")
                        break
                    elif user_manager.has_more_attempts():
                        print(f"\nLogin failed. You have {3 - user_manager._attempts} attempt(s) left. Please check your username and password.\n")
                if not user_manager.has_more_attempts() and not user:
                    print("\nToo many failed attempts. Access denied.\n")
                    continue

                if user_manager.is_current_user_admin():
                    while True:
                        admin_choice = admin_menu()
                        match admin_choice:
                            case 1:
                                hotel_name = input("Enter hotel name: ")
                                hotel_stars = HotelManager.validate("Enter hotel stars (1-5): ", "Invalid stars!", int,
                                                                    1, 5)
                                street = input("Enter street: ")
                                zip_code = input("Enter zip code: ")
                                city = input("Enter city: ")

                                rooms = hotel_manager.add_rooms_to_hotel()

                                hotel = hotel_manager.add_hotel(hotel_name, hotel_stars, street, zip_code, city, rooms)
                                print(f"\nHotel '{hotel_name}' added with ID {hotel.id}\n")

                            case 2:
                                hotels = hotel_manager.list_hotels()
                                show_hotels(hotels, search_manager)
                                hotel_id = HotelManager.validate("\nEnter hotel ID to delete: ", "Invalid ID!", int)
                                confirm = HotelManager.validate("Are you sure you want to delete this hotel? (yes/no): ", "Invalid input!", str)
                                if confirm.lower() == 'yes':
                                    if hotel_manager.delete_hotel(hotel_id):
                                        print("\nHotel deleted successfully.\n")
                                    else:
                                        print("\nHotel not found.\n")

                            case 3:
                                hotels = hotel_manager.list_hotels()
                                show_hotels(hotels, search_manager)
                                hotel_id = HotelManager.validate("\nEnter hotel ID to update: ", "Invalid ID!", int)
                                hotel = hotel_manager.get_hotel(hotel_id)
                                if not hotel:
                                    print("\nHotel not found.\n")
                                    continue

                                def update_menu():
                                    print("\n================== Update Options ==================")
                                    print("1. Update Hotel Name")
                                    print("2. Update Hotel Stars")
                                    print("3. Update Hotel Address")
                                    print("4. Update Room")
                                    print("5. Add Room to Hotel")
                                    print("6. Exit")
                                    return HotelManager.validate("Please select an option (1-6): ", "Invalid option!", int, 1, 6)

                                while True:
                                    update_choice = update_menu()
                                    match update_choice:
                                        case 1:
                                            new_name = input("Enter new hotel name: ")
                                            if hotel_manager.update_hotel_name(hotel_id, new_name):
                                                print("\nHotel name updated successfully.\n")
                                            else:
                                                print("\nFailed to update hotel name.\n")

                                        case 2:
                                            new_stars = HotelManager.validate("Enter new hotel stars (1-5): ", "Invalid stars!", int, 1, 5)
                                            if hotel_manager.update_hotel_stars(hotel_id, new_stars):
                                                print("\nHotel stars updated successfully.\n")
                                            else:
                                                print("\nFailed to update hotel stars.\n")

                                        case 3:
                                            new_street = input("Enter new street: ")
                                            new_zip = input("Enter new zip code: ")
                                            new_city = input("Enter new city: ")
                                            if hotel_manager.update_hotel_address(hotel_id, new_street, new_zip, new_city):
                                                print("\nHotel address updated successfully.\n")
                                            else:
                                                print("\nFailed to update hotel address.\n")

                                        case 4:
                                            rooms = hotel_manager.list_hotel_rooms(hotel_id)
                                            for room in rooms:
                                                print(f"\nRoom Number: {room.number}\nType: {room.type}\nPrice: {room.price}\nMax Guests: {room.max_guests}\nDescription: {room.description}\nAmenities: {room.amenities}\n")
                                            room_number = input("Enter room number to update: ")
                                            new_type = input("Enter new room type: ")
                                            new_price = HotelManager.validate("Enter new room price: ", "Invalid price!", float)
                                            new_description = input("Enter new room description: ")
                                            new_amenities = input("Enter new room amenities: ")
                                            new_max_guests = HotelManager.validate("Enter new max guests: ", "Invalid number!", int)
                                            if hotel_manager.update_room(hotel_id, room_number, new_type, new_price, new_description, new_amenities, new_max_guests):
                                                print("\nRoom updated successfully.\n")
                                            else:
                                                print("\nFailed to update room.\n")

                                        case 5:
                                            rooms = hotel_manager.add_rooms_to_hotel(hotel_id)
                                            for room in rooms:
                                                print(f"\nRoom {room.number} added successfully.\n")

                                        case 6:
                                            break

                            case 4:
                                hotels = hotel_manager.list_hotels()
                                show_hotels(hotels, search_manager)

                            case 5:
                                reservation_manager.show_all_bookings()

                            case 6:
                                user_manager.logout()
                                break

                else:
                    user_menu_loop()

            case 2:
                while True:
                    username = input("Enter username: ")
                    if user_manager.is_username_unique(username):
                        break
                    else:
                        print("\nUsername is already taken. Please choose another one.\n")
                password = input("Enter password: ")
                firstname = input("Enter first name: ")
                lastname = input("Enter last name: ")
                email = input("Enter email: ")
                street = input("Enter street: ")
                zip_code = input("Enter zip code: ")
                city = input("Enter city: ")

                try:
                    user_id = user_manager.add_user(username, password, firstname, lastname, email, street, zip_code, city)
                    user = user_manager.login(username, password)
                    if user:
                        print(f"\nRegistration successful, welcome {firstname}!\n")
                        user_menu_loop()
                    else:
                        print("\nFailed to log in the new user.\n")
                except ValueError as e:
                    print(f"\n{e}\n")

            case 3:
                search_and_book_hotel(user_manager, reservation_manager, search_manager, is_guest=True)

            case 4:
                break