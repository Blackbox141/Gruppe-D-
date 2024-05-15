def update_hotel(self):
    hotel_id = input("Enter the Hotel ID to update: ")
    hotel = self._session.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel:
        print("No hotel found with that ID.")
        return

    print("Which attribute would you like to update?")
    print("1. Hotel Name")
    print("2. Hotel Stars")
    print("3. Hotel Address")
    print("4. Room Details")
    choice = input("Enter your choice (1-4): ")

    if choice == '1':
        new_name = input("Enter the new name for the hotel: ")
        hotel.name = new_name

    elif choice == '2':
        new_stars = input("Enter the new star rating (1-5): ")
        try:
            hotel.stars = int(new_stars)
        except ValueError:
            print("Invalid input. Stars must be an integer.")
            return

    elif choice == '3':
        new_street = input("Enter the new street: ")
        new_zip = input("Enter the new zip code: ")
        new_city = input("Enter the new city: ")
        if not hotel.address:
            hotel.address = Address()
        hotel.address.street = new_street
        hotel.address.zip = new_zip
        hotel.address.city = new_city

    elif choice == '4':
        room_number = input("Enter the room number to update: ")
        room = next((r for r in hotel.rooms if str(r.number) == room_number), None)
        if not room:
            print("No room found with that number.")
            return
        # Assuming you want to let the user update the room type and price
        new_type = input("Enter the new room type: ")
        new_price = input("Enter the new price: ")
        try:
            room.type = new_type
            room.price = float(new_price)
        except ValueError:
            print("Invalid price. Please enter a valid number.")
            return

    else:
        print("Invalid choice.")
        return

    self._session.commit()
    print("Update successful!")




if __name__ == "__main__":
    manager = HotelManager("../data/hotel_reservation.db")

    # Example call to edit a hotel
    manager.edit_hotel(
        hotel_id=1,
        new_name="New Hotel Name",
        new_stars=4,
        new_street="123 New Street",
        new_zip="10001",
        new_city="New City"
    )







def edit_hotel(self, hotel_id, new_name=None, new_stars=None, new_street=None, new_zip=None, new_city=None):
    # Fetch the hotel by ID
    hotel = self._session.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel:
        print(f"No hotel found with ID {hotel_id}.")
        return

    # Update hotel name if provided
    if new_name:
        hotel.name = new_name

    # Update hotel stars if provided
    if new_stars is not None:
        hotel.stars = new_stars

    # Update hotel address if any address component is provided
    if new_street or new_zip or new_city:
        if not hotel.address:
            hotel.address = Address()
        if new_street:
            hotel.address.street = new_street
        if new_zip:
            hotel.address.zip = new_zip
        if new_city:
            hotel.address.city = new_city

    # Commit changes to the database
    self._session.commit()
    print(f"Hotel with ID {hotel_id} has been updated.")
