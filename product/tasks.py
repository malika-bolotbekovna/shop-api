from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings   
from product.models import Product

@shared_task
def all_products(email):

    products = Product.objects.all().values_list("title", "price")
    product_list = "\n".join([f"{title} — {price}₽" for title, price in products])

    send_mail(
        "Список всех товаров",
        product_list,
        settings.EMAIL_HOST_USER,
        [email],
    )
    return f"Отправлено {len(products)} товаров на {email}"