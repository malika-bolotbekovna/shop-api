from django.db import models
from django.db.models import Avg
from users.models import CustomUser

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    def product_count(self):
        return self.products.count()


 
class Product(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.title
    
    def rating(self):
        rating_dict = Review.objects.all().aggregate(Avg('stars'))
        rate = rating_dict['stars__avg']
        return rate
    

STARS = (
    (i, '*' * i) for i in range(1, 6)
)    


class Review(models.Model):
    text = models.TextField(null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, 
                                related_name='reviews')
    stars = models.IntegerField(choices=STARS, default=5)

    def __str__(self):
        return self.text[:30]