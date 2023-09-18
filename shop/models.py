from django.db import models
from django.contrib.auth.models import AbstractUser

class Category(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT,related_name="products")
    image = models.ImageField()

    def __str__(self) -> str:
        return self.title


class Customer(AbstractUser):
    phone = models.CharField(max_length=255,null=True)
    country = models.CharField(max_length=255,null=True)
    postal_code = models.CharField(max_length=50,null=True)
    town = models.CharField(max_length=255,null=True)
    state = models.CharField(max_length=255,null=True)


    def __str__(self) -> str:
        return self.first_name + ' ' + self.last_name




class Order(models.Model):

    placed_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    complete = models.BooleanField(default=True)
    phone = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=10)


    def __str__(self) -> str:
        return self.placed_at + ' ' + self.customer




class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)




class Cart(models.Model):
    cart_id = models.CharField(max_length=250,blank=True,primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.product.title

