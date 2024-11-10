import datetime
from .models import Rooms, Booking


def check_availability(room, check_in, check_out):
    
    booking_list = Booking.objects.filter(room_data=room)

    for book in booking_list:
       
        if not (book.check_in > check_out or book.check_out < check_in):
            return False  

    return True  
