from django.db.models.signals import post_save,pre_save
from Accounts.models import User
from django.dispatch import receiver
from django.core.mail import send_mail
from  MicroService import settings

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        subject = 'Account Created'
        message = f'Your account has been created successfully.'
        try:
            send_mail(
                subject, 
                message, 
                settings.EMAIL_HOST_USER, 
                [instance.email], 
                fail_silently=False
            )
            print(f"Welcome email sent to {instance.email}.")
        except Exception as e:
            print(f"Error while sending welcome email: {e}")