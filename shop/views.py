from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.urls import reverse

import json
from .models import *



def index(request):
    if request.method == "GET":
        products = []
        limit = 2
        for category in Category.objects.all():
            products.extend(list(Product.objects.filter(category = category)[:limit]))

        return render(request,"shop/index.html",{'products': products})
    
def login(request):
    products = Product.objects.all()
    return render(request,"shop/login.html",{'products': list(products)})

def signup(request):
    return render(request,"shop/signup.html")

def contact(request):
    return render(request,"shop/contact.html")

def about(request):
    return render(request,"shop/about.html")

def cart(request):
    if "cart" not in request.session:
        request.session["cart"] = dict()

    if request.method == "GET":
        country_vat = 0.15
        products = []
        cart = request.session["cart"]
        print(cart)
        for productId in cart:

            product =  Product.objects.get(id = int(productId))
            products.append((product,cart[productId]))
        subtotal = 0
        for product,quantity in products:
            subtotal += (int(quantity) * int(product.unit_price)) 
        total = subtotal + subtotal * country_vat
        return render(request,"shop/cart.html",{'products':products,'total':total,'subtotal':subtotal,'vat':f'{country_vat*100}%'})

    else:
        cart = request.session["cart"]
        data = json.loads(request.body)
        productId = data['productId']
        action = data['action']


        if action == "add":
            
            if str(productId) not in cart:
                cart[str(productId)] = 1
            else:
                cart[str(productId)] += 1
            product = Product.objects.get(pk = productId)
            if int(cart[str(productId)]) > product.inventory:
                cart[str(productId)] = int(product.inventory)

        elif action == "remove":
            cart.pop(productId)
        

        



        request.session["cart"] = cart
        

        return JsonResponse(request.session["cart"],safe=False)

def addFromProduct(request,productId):

    quantity = request.POST.get("quantity")
    if "cart" not in request.session:
        request.session["cart"] = dict()

    cart = request.session["cart"]
    if str(productId) not in cart:
                cart[str(productId)] = int(quantity)
    else:
        cart[str(productId)] += int(quantity)

    product = Product.objects.get(pk = productId)
    if int(cart[str(productId)]) > product.inventory:
        cart[str(productId)] = int(product.inventory
)
    request.session["cart"] = cart

    return redirect(reverse("shop:product",args=[int(productId)]))
    
    

    


        

def account(request):
    return HttpResponse("Coming soon!")

def checkout(request):
    return render(request,"shop/checkout.html")

def product(request,product_id):
    product = Product.objects.get(pk = product_id)
    return render(request,"shop/product.html",{"product":product})

def categories(request,category_id):
    category = Category.objects.get(pk = category_id)
    products = category.products.all()
    return render(request,"shop/categories.html",{'products': list(products), 'category':category})

def setcart(request):
    
    cart = request.session["cart"]
    data = json.loads(request.body)
    productId = data['productId']
    value = data['value']

    cart[str(productId)] = int(value)
    request.session["cart"] = cart

    return JsonResponse(request.session["cart"],safe=False)

    


