from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings    
from datetime import date
from users.models import CustomUser

@shared_task
def send_otp_email(email, code):
    print("sending...")
    send_mail(
        "hello",
        f"your code: {code}",
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
    print("sent")


@shared_task
def send_daily_report():
    print("sending...")
    pochta = "malikaorozobaeva@gmail.com"
    send_mail(
        "hello, this is a new report",
        "success",
        settings.EMAIL_HOST_USER,
        [pochta],
        fail_silently=False,
    )
    print("sent")



@shared_task
def send_birthday_congratulations():
    today = date.today()
    birthday_users = CustomUser.objects.filter(
        birthday__month=today.month,
        birthday__day=today.day
    )

    for user in birthday_users:
        send_mail(
            "с днём рождения!",
            f"дорогой {user.email}, поздравляем тебя с днём рождения!",
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )


@shared_task
def send_discount_reminder(user_email, date_str):
    send_mail(
        f"поздравляем, вы получаете скидку 10% на любой товар",
        f"скидка продлится до: {date_str}, при предявлении аккаунта и данного сообщения.",
        settings.EMAIL_HOST_USER,
        [user_email],
        fail_silently=False,
    )