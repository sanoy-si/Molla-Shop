from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from .forms import *

import json
from .models import *



def index(request):
    if request.method == "GET":
        products = []
        limit = 2
        for category in Category.objects.all():
            products.extend(list(Product.objects.filter(category = category)[:limit]))

        return render(request,"shop/index.html",{'products': products})
    
def logIn(request):
    if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            # Authenticate the user
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Log in the user
                login(request, user)
                return redirect('shop:index')  # Replace 'home' with your desired URL

            # Authentication failed, show an error message
            else:
                message = "Username or password is Incorrect"
                return render(request, 'shop/login.html', {'message': message,'username':username,'password':password})

    return render(request, 'shop/login.html')

def signup(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            # confirmation email
            return redirect('shop:login')  # Redirect to the login page after successful signup
    else:
        form = SignUpForm()
        return render(request,"shop/signup.html",{'form':form})

    return render(request,"shop/signup.html",{'form':form})



def logOut(request):
    logout(request)
    return redirect('shop:index') 

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
        return render(request,"shop/cart.html",{'products':products,'total':total,'subtotal':subtotal,'vat':country_vat*subtotal})

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
    
    

    


        

def account(request,username):
    customer = Customer.objects.get(username = username)
    return render(request,"shop/account.html",{'customer':customer})

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

    


