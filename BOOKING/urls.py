from django.urls import path
from .views import  *

urlpatterns = [
    path("", home, name="index"),
    path("sign/", sign, name="signUp"),
    path("verify-email/<slug:username>", verify_email, name="verify-email"),
    path("resend-otp", resend_otp, name="resend-otp"),
    path('room/<str:name>/' , Room_BookingId , name='roomId') , 
    path('room/' , room , name='room'),
    path('logout/' , Logout , name = 'logout')
]