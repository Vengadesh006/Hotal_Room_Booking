from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from .singals import create_token
import logging
from datetime import datetime
from django.shortcuts import HttpResponse
from .availability import check_availability


logger = logging.getLogger(__name__)

# Create your views here.

def home(request):

    if request.method == 'POST':

        username = request.POST['username']

        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        
        if user is not None: 

            login(request, user)

            return redirect("/")
        
        else:
            messages.warning(request, "Invalid credentials")

            return redirect("/")
    else :

        return render(request, "home.html" , {'view' : HomePage.objects.all()} )

def room(request) : 
    if request.method == 'POST':
        
        username = request.POST['username']

        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        
        if user is not None: 

            login(request, user)

            return redirect("/room/")
        
        else:
            messages.warning(request, "Invalid credentials")

            return redirect("/room/")
    else :

        context = {'room' : Rooms.objects.all() }

        return render(request , 'room.html' , context)

def sign(request):

    form = User_form()

    if request.method == 'POST':

        form = User_form(request.POST)

        if form.is_valid():

            form.save()

            messages.success(request, "Account created successfully! An OTP was sent to your Email")

            return redirect("verify-email", username=request.POST['username'])

    return render(request, "sign.html" , {'forms' : form})

def Room_BookingId(request, name) :

    if request.method == 'POST' :

        room_list = Rooms.objects.filter(head=name)

        str_login = request.POST['check_in']

        login_date= datetime.strptime(str_login, '%Y-%m-%d').date()
        
        str_out = request.POST['check_out']

        logout_date= datetime.strptime(str_out, '%Y-%m-%d').date()
        
        available_room = []

        for room in room_list : 
            print(room)
            if check_availability(room , login_date , logout_date) : 
                available_room.append(room)
                
        if len(available_room) > 0 : 

            room = available_room[0] 

            booking = Booking(
                user_data_id=request.user.id , 
                room_data= room , 
                types_id=request.POST['types'] ,
                check_in=login_date , 
                check_out=logout_date
            )
            if not booking.time : 
                booking.time = datetime.time(12, 0) 
            booking.save()
            messages.success(request , 'Your is Booking Successfull 😉' )

            return redirect('/')

        else : 

            messages.error(request , 'Room has been already Booking ! 😔')
            
            return redirect('/')

    else : 

        if request.user.is_authenticated :

            data = Rooms.objects.filter(head=name)
            print(data)

            context = {"forms" : Booking_Form , 'details' : data}

            return render(request , 'roomDetails.html' , context)
        else : 

            messages.error(request , 'Pleses Going To Loggin 🤭')

            return redirect('/room/')



def verify_email(request, username):

    user = get_user_model().objects.get(username=username)

    user_otp = OTP_Token.objects.filter(user=user).last()
    
    
    if request.method == 'POST':
        # valid token
        if user_otp.otp_code == request.POST['otp_code']:
            
            # checking for expired token
            if user_otp.otp_expires_at > timezone.now():

                user.is_active=True

                user.save()

                messages.success(request, "Account activated successfully!! You can Login.")

                return redirect("/")
            
            # expired token
            else:
                messages.warning(request, "The OTP has expired, get a new OTP!")
                return redirect("verify-email", username=user.username)
        
        
        # invalid otp code
        else:
            messages.warning(request, "Invalid OTP entered, enter a valid OTP!")
            return redirect("verify-email", username=user.username)
        
    context = {}
    return render(request, "verify_token.html", context)



def resend_otp(request):

    if request.method == 'POST':

        user_email = request.POST.get("otp_email")
        
        if get_user_model().objects.filter(email=user_email).exists():

            user = get_user_model().objects.get(email=user_email)

            otp = OTP_Token.objects.create(
                user=user,
                otp_expires_at=timezone.now() + timezone.timedelta(minutes=8)
            )
            
            # email variables
            subject = "Email Verification"
            message = f"""
                        Hi {user.username}, here is your OTP: {otp.otp_code}
                        It expires in 5 minutes. Use the URL below to return to the website:
                        http://127.0.0.1:8000/verify-email/{user.username}
                        """
            sender = "your_gmail_address@gmail.com"
            receiver = [user.email]
        
            try:
                # Send email
                send_mail(subject, message, sender, receiver, fail_silently=False)
                messages.success(request, "A new OTP has been sent to your email address.")
                return redirect("verify-email", username=user.username)
            except Exception as e:
                logger.error(f"Error sending email: {e}")
                messages.error(request, "Failed to send OTP email. Please try again.")
                return redirect("resend-otp")
        
        else:
            messages.warning(request, "This email doesn't exist in the database.")
            return redirect("resend-otp")
    
    return render(request, "resend_otp.html")



def Logout(request) : 
    logout(request)
    return redirect('/')



    