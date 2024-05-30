import sys

from business.TestUserManager import UserManager

if __name__ == '__main__':
    user_manager = UserManager("./data/hotel_reservation.db")
    while user_manager.has_more_attempts():
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        if user_manager.login(username, password):
            break
        else:
            print("Invalid username or password")
    if user_manager.get_current_user():
        print("Logged in successfully")
        print(f"Welcome {user_manager.get_current_user().username}")
        if user_manager.is_current_user_admin():
            print("You have granted admin rights")
        else:
            print("You are a registered guest")
            reg_guest = user_manager.get_reg_guest_of(user_manager.get_current_user())
            print(f"{reg_guest.firstname} {reg_guest.lastname}")
    else:
        print("Too many attempts")

    #von Phillip