# Step 1: Define the details of an available hotel (DB)
hotel_name = "Hotel Aria"
city = "Olten"
no_rooms = 10
stars = 4
is_available = False
price_per_night = 169

def search_hotels():
    pass

def show_hotels():
    if is_available:
        # geht auch mit True == is_available oder mit is_available == True, aber ohne "== True" geht er immer von True aus.
        print("Name: %s" % hotel_name)
        print("City: %s" % city)
        print("No of rooms: %d" % no_rooms)
        print("Stars: %d" % stars)
        print("Price per night: %0.2f" % price_per_night)
        print("Availability: %s" % is_available)
    else:
        print("Sorry, we're booked out. Come back another time.")

show_hotels()
