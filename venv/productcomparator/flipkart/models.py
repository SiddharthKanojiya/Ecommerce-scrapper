from django.db import models

# Create your models here.
class Product(models.Model):
    sinput=models.CharField(max_length=200)
    productInfo=models.CharField(max_length=500)
    price=models.CharField(max_length=20)
    link=models.URLField()
    img=models.URLField()
    rating=models.CharField(max_length=10)