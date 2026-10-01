from django.contrib import admin
from .models import (
    customer,
    Product,
    cart,
    OrderPlaced
)
# Register your models here.

@admin.register(customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','name','locality','city','zip_code','state']

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id','tittle','selling_price','discounted_price','description','brand','category','product_image']

@admin.register(cart)
class cartModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity']

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','customers','product','quantity','ordered_date','status']
