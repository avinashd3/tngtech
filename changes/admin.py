from django.contrib import admin
from .models import Shophome,HotDeals,Category,SubCategory,Brand,TopSelling,ModelofProduct
# Register your models here.

admin.site.register(Shophome)
admin.site.register(HotDeals)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Brand)
admin.site.register(TopSelling)
admin.site.register(ModelofProduct)