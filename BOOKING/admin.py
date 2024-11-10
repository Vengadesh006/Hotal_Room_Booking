from django.contrib import admin
from .models import * 

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(OTP_Token)
admin.site.register(HomePage)
admin.site.register(Rooms)
admin.site.register(Room_info)
admin.site.register(Booking)

