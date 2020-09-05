from django.contrib import admin
from .models import TngProducts,Order,OrderItem,Payment,Coupon,Refund,Address,NewsLetter,OnlineBooking
# Register your models here.

def make_refund_accepted(modeladmin,request,queryset):
    queryset.update(refund_requested=False,refund_granted=True)

make_refund_accepted.short_description='Update orders to refund granted'

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user','ordered','being_delivered','received','refund_requested','refund_granted','billing_address','shipping_address','payment','coupon']
    list_display_links=['user','billing_address','shipping_address','payment','coupon']
    list_filter = ['ordered','being_delivered','received','refund_requested','refund_granted']
    search_fields=['user__username','ref_code']
    actions=[make_refund_accepted]

class AddressAdmin(admin.ModelAdmin):
    list_display=['user','street_address','apartment_address','zip','country','address_type','default']
    list_filter=['user','country','address_type']
    search_fields=['user__username','street_address','apartment_address','zip']

class ProductsAdmin(admin.ModelAdmin):
    list_filter = ['Name','category','subcategory','brand','model','label','slug']
    search_fields=['Name','category','subcategory','brand','model','label','slug']

admin.site.register(TngProducts,ProductsAdmin)
admin.site.register(OrderItem)
admin.site.register(Order,OrderAdmin)
admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(Refund)
admin.site.register(Address,AddressAdmin)
admin.site.register(NewsLetter)
admin.site.register(OnlineBooking)