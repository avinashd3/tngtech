from django.db import models
from PIL import Image
from prod.models import TngProducts

class Shophome(models.Model):
    heading_1 = models.CharField(max_length = 35)
    heading_2 = models.CharField(max_length = 35)
    link = models.CharField(max_length = 100)
    linkname = models.CharField(max_length = 20)
    image=models.ImageField(upload_to='product_pics')

class HotDeals(models.Model):
    image = models.ImageField(default='hotdeal.png',upload_to='product_pics')
    heading = models.CharField(max_length = 70)
    details = models.CharField(max_length = 100)
    datetime = models.DateTimeField(auto_now_add=False,blank=True,null=True)

    def save(self,*args,**kwargs):
        super().save(self,*args,**kwargs)
        img = Image.open(self.image.path)
        if img.height < 465 or img.width < 1782:
            output_size = (1782,465)
            img.thumbnail(output_size)
            img.save(self.image.path)
    
    class Meta:
        verbose_name_plural = 'Hot Deals'

class Category(models.Model):
    name = models.CharField(max_length = 100)
    image = models.ImageField(default = 'product01.png',upload_to = 'product_pics')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'

class SubCategory(models.Model):
    name = models.CharField(max_length = 100)
    image = models.ImageField(upload_to = 'product_pics')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'SubCategories'

class Brand(models.Model):
    name = models.CharField(max_length = 100)
    image = models.ImageField(upload_to = 'product_pics')

    def __str__(self):
        return self.name

class TopSelling(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)

    def __str__(self):
        return self.category.name