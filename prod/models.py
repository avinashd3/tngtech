from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone
from django.urls import reverse
from django_countries.fields import CountryField



LABEL_CHOICES=(
    ('P','BESTSELLER'),
    ('D','NEW'),
    ('H','HotDeals'),
    ('R','Regular')
)

ADDRESS_CHOICES=(
    ('B','Billing'),
    ('S','Shipping')
)


#Products
class TngProducts(models.Model):
    CATEGORY_CHOICES=(
        ('MA','Mobile Accessories'),
        ('LA','Laptop Accessories'),
        ('TA','Tablet Accessories'),
        ('EG','Electronic Gadgets'),
        ('LA','Latest Accessories'),
        ('MR','Mobile Repair'),
        ('LR','Laptop/Computer Repair'),
        ('TR','iPad/Tablet Repair')
    )
    Name=models.CharField(max_length=100)
    Details=models.TextField()
    Additional_Details=models.TextField(blank=True,null=True)
    Price=models.FloatField()
    Discount_Price=models.FloatField(blank=True,null=True)
    category=models.CharField(max_length=2,choices=CATEGORY_CHOICES,default='A')
    subcategory = models.CharField(max_length = 100,default='none')
    brand = models.CharField(max_length = 50,default='none')
    label=models.CharField(max_length=1,choices=LABEL_CHOICES,default='R')
    slug=models.SlugField(default='test-product')
    image=models.ImageField(default='default.jpg',upload_to='product_pics')
    image1=models.ImageField(null=True,blank=True,upload_to='product_pics')
    image2=models.ImageField(null=True,blank=True,upload_to='product_pics')
    image3=models.ImageField(null=True,blank=True,upload_to='product_pics')
    image4=models.ImageField(null=True,blank=True,upload_to='product_pics')

    def __str__(self):
        return self.Name

    def get_absolute_url(self):
        return reverse('itemlist', kwargs={
            'slug':self.slug})

    def get_add_to_cart_url(self):
        return reverse('addtocart', kwargs={
            'slug':self.slug})

    def get_remove_from_cart_url(self):
        return reverse('removefromcart', kwargs={
            'slug':self.slug})
    
    # def save(self,*args,**kwargs):
    #     super().save(self,*args,**kwargs)
    #     img = Image.open(self.image.path)
    #     if img.height > 600 or img.width > 600:
    #         output_size = (600,600)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)

    class Meta:
        verbose_name_plural = 'Products'


#It links products to cart.Once a product is added to cart it becomes an orderitem
#Intermediate model between Order and Products
class OrderItem(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    ordered=models.BooleanField(default=False)
    tngproducts=models.ForeignKey(TngProducts,on_delete=models.CASCADE,default='')
    quantity=models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.tngproducts.Name}"

    def get_total_item_price(self):
        return self.quantity * self.tngproducts.Price

    def get_total_discount_price(self):
        return self.quantity * self.tngproducts.Discount_Price

    def get_amount_save(self):
        return self.get_total_item_price() - self.get_total_discount_price()

    def get_final_price(self):
        if self.tngproducts.Discount_Price:
            return self.get_total_discount_price()
        return self.get_total_item_price()

#Adding products to Cart
class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    ref_code=models.CharField(max_length=20,blank=True,null=True)
    tngproduct=models.ManyToManyField(OrderItem)
    ordered=models.BooleanField(default=False)
    start_date=models.DateTimeField(default=timezone.now)
    ordered_date=models.DateTimeField()
    shipping_address=models.ForeignKey('Address',related_name='shipping_address',on_delete=models.SET_NULL,blank=True,null=True)
    billing_address=models.ForeignKey('Address',related_name='billing_address',on_delete=models.SET_NULL,blank=True,null=True)
    payment=models.ForeignKey('Payment',on_delete=models.SET_NULL,blank=True,null=True)
    coupon = models.ForeignKey('Coupon',on_delete=models.SET_NULL,blank=True,null=True)
    being_delivered=models.BooleanField(default=False)
    received=models.BooleanField(default=False)
    refund_requested=models.BooleanField(default=False)
    refund_granted=models.BooleanField(default=False)

    def get_total(self):
        total=0
        for order_item in self.tngproduct.all():
            total+=order_item.get_final_price()
        if self.coupon:
            total-=self.coupon.amount
        return total
#class meta is metadata ::: for more info------>https://docs.djangoproject.com/en/3.0/ref/models/options/

class Address(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    addr_code=models.CharField(max_length=10,blank=True,null=True)
    street_address=models.CharField(max_length=100)
    apartment_address=models.CharField(max_length=100)
    zip=models.CharField(max_length=100)
    country=CountryField(multiple=False)
    address_type=models.CharField(max_length=1,choices=ADDRESS_CHOICES)
    default=models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'

class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user=models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)
    amount=models.FloatField()
    timestamp=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username

class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code

class Refund(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    reason=models.TextField()
    accepted=models.BooleanField(default=False)
    email=models.EmailField()

    def __str__(self):
        return f"{self.pk}"

class NewsLetter(models.Model):
    email = models.EmailField()

class OnlineBooking(models.Model):
    Name = models.CharField(max_length=50)
    email = models.EmailField()
    brand = models.CharField(max_length=50)
    contact = models.CharField(max_length=10)
    device_type = models.CharField(max_length=50)
    device_model = models.CharField(max_length=50)
    repair_type = models.CharField(max_length=50)
    time = models.CharField(max_length=20)
