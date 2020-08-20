from django.db import models

class Shophome(models.Model):
    heading_1 = models.CharField(max_length = 35)
    heading_2 = models.CharField(max_length = 35)
    link = models.CharField(max_length = 100)
    linkname = models.CharField(max_length = 20)
    image=models.ImageField(default='default.jpg',upload_to='product_pics')

class HotDeals(models.Model):
    image = models.ImageField(default='hotdeal.png',upload_to='product_pics')
    days = models.PositiveIntegerField()
    hours = models.PositiveIntegerField()
    minutes = models.PositiveIntegerField()
    seconds = models.PositiveIntegerField()
    heading = models.CharField(max_length = 70)
    details = models.CharField(max_length = 100)
    datetime = models.DateTimeField(auto_now_add=False,blank=True,null=True)