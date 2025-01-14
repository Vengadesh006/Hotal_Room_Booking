from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from .models import OTP_Token
from django.core.mail import send_mail
from django.utils import timezone

@receiver(post_save, sender=settings.AUTH_USER_MODEL)

def create_token(sender, instance, created, **kwargs):

    if created:
        print('Email')

        if not instance.is_superuser:  # Only non-superusers should get OTP
            # Create OTP Token
            otp_token = OTP_Token.objects.create(
                user=instance, 
                otp_expires_at=timezone.now() + timezone.timedelta(minutes=8)
            )
            instance.is_active = False  # Deactivate the user until OTP is verified
            instance.save()

            # Get the last created OTP
            otp = OTP_Token.objects.filter(user=instance).last()
            print(otp)

            # Email content
            subject = "Email Verification"
            message = f"""
            Hi {instance.username}, here is your OTP: {otp.otp_code}.
            It expires in 5 minutes. Please use the link below to verify your email:
            http://127.0.0.1:8000/verify-email/{instance.username}
            """
            sender = settings.EMAIL_HOST
            print(sender)
            
            receiver = [instance.email]
            print(receiver)

            # Send email
            send_mail(
                subject,
                message,
                sender,
                receiver,
                fail_silently=False,
            )
            print('filnale output')
