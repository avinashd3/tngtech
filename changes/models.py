from django.db import models

class Shophome(models.Model):
    heading_1 = models.CharField(max_length = 35)
    heading_2 = models.CharField(max_length = 35)
    link = models.CharField(max_length = 100)
    linkname = models.CharField(max_length = 20)
    image=models.ImageField(default='default.jpg',upload_to='product_pics')
