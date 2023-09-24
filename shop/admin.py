from django.contrib import admin
from .models import *


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','unit_price','inventory']
    list_editable = ['unit_price','inventory']
    list_per_page = 10

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','username','email','country']
    list_per_page = 10


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer','country','postal_code','payment_status','placed_at','total']
    list_per_page = 10

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title','numProducts']
    list_per_page = 10

    def numProducts(self,obj):
        return len(list(obj.products.all()))
    numProducts.short_description = "Number Of Products"


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['cart_id','created_at']
    list_per_page = 10



@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['owner','cart','product','quantity']
    list_per_page = 10

    def owner(self,obj):
        return obj.customer
    

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ['orderedBy','orderId','product','quantity'] 
    def orderedBy(self,obj):
        return obj.order.customer
    orderedBy.short_description = "Ordered By" 
    def orderId(self,obj):
        return obj.order.id
    orderId.short_description = "Order Id"



@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ['sentBy','email','subject','message']

    def sentBy(self,obj):
        return obj.first_name + ' ' + obj.last_name
    sentBy.short_description = "Sent By"

    def email(self,obj):
        return obj.email
    email.short_description = "Email"

    def subject(self,obj):
        return obj.subject
    subject.short_description = "Subject"

    def message(self,obj):
        return obj.message
    message.short_description = "Message"
 
 




