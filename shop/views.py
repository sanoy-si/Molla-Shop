from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
import requests
from .forms import *

import json
from .models import *



def index(request):
    if request.method == "GET":
        products = []
        limit = 2
        for category in Category.objects.all():
            products.extend(list(Product.objects.filter(category = category,inventory__gt = 0)[:limit]))
        print(request.session.session_key)

        return render(request,"shop/index.html",{'products': products})
    
def logIn(request):
    if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            # Authenticate the user
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Log in the user

                products = {}

                try:
                    cart = Cart.objects.get(cart_id = _cart_id(request))
                    cart_item = CartItem.objects.filter(cart = cart)
                    for item in cart_item:
                        products[item.product.title] = item.id
                            
                except:
                    pass



                exisiting_products = {}
                cart_item = CartItem.objects.filter(customer__id = user.id)
                for item in cart_item:
                    exisiting_products[item.product.title] = item.id


                print(exisiting_products,products)
                for product in products.keys():
                    if product in exisiting_products:
                        print(exisiting_products,product)
                        eitem = CartItem.objects.get(id = exisiting_products[product])
                        nitem = CartItem.objects.get(id = products[product])
                        eitem.quantity += nitem.quantity
                        if eitem.product.inventory < eitem.quantity:
                            eitem.quantity = eitem.product.inventory
                        # item.customer = Customer.objects.get(pk = user.id)
                        eitem.save()
                    else:
                        cart_item = CartItem.objects.get(id = products[product])
                        item.customer = Customer.objects.get(id = user.id)
                        item.save()




                login(request, user)

                url = request.META.get("HTTP_REFERER")
                try:
                    query = requests.utils.urlparse(url).query
                    params = dict([x.split('=') for x in query.split('&')])
                    if 'next' in params:
                        return redirect(params['next'])
                except:
                    return redirect('shop:account', username = user.username)

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

def _cart_id(request):
        cart = request.session.session_key
        if  cart == None:
            request.session.create()
            cart = request.session.session_key

        return cart

def cart(request):

    if request.method != "POST":
        country_vat = 0.15
        subtotal = 0

        try:
            if request.user.is_authenticated:
                cart_items = CartItem.objects.filter(customer__id = request.user.id)

            else:
                cart = Cart.objects.get(cart_id = _cart_id(request))
                cart_items = CartItem.objects.filter(cart = cart)

            for cart_item in cart_items:
                subtotal += (float(cart_item.product.unit_price) * cart_item.quantity)
        except ObjectDoesNotExist:
            cart_items = None
            

        total = subtotal + subtotal * country_vat
        return render(request,"shop/cart.html",{'cart_items':cart_items,'total':total,'subtotal':subtotal,'vat':country_vat*subtotal})

    else:
        data = json.loads(request.body)
        productId = data['productId']
        action = data['action']

        product = Product.objects.get(id = int(productId))
        try:
            cart = Cart.objects.get(cart_id = _cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
        cart.save()

        if request.user.is_authenticated:
            if action == "add":
                try:
                    cart_item = CartItem.objects.get(product = product, customer__id = request.user.id)
                    cart_item.quantity += 1
                    cart_item.save()
                except CartItem.DoesNotExist:
                    cart_item = CartItem.objects.create(
                        product = product,
                        cart = cart,
                        quantity = 1,
                        customer = Customer.objects.get(id = request.user.id) 
                    )
                    cart_item.save()

                if cart_item.quantity>product.inventory:
                    cart_item.quantity = product.inventory
                    cart_item.save()


            elif action == "remove":
                CartItem.objects.filter(product=product,customer__id = request.user.id).delete()
                return JsonResponse("Added To Cart",safe=False)


        
        
        else:
            if action == "add":
                try:
                    cart_item = CartItem.objects.get(product = product,cart=cart)
                    cart_item.quantity += 1
                    cart_item.save()
                except CartItem.DoesNotExist:
                    cart_item = CartItem.objects.create(
                        product = product,
                        cart = cart,
                        quantity = 1
                    )
                    cart_item.save()

                    if cart_item.quantity>product.inventory:
                        cart_item.quantity = product.inventory
                        cart_item.save()

                        

            elif action == "remove":
                CartItem.objects.filter(product=product,cart=cart).delete()
                return JsonResponse("Added To Cart",safe=False)
            

def addFromProduct(request,productId):
    
    quantity = int(request.POST.get("quantity"))
    product = Product.objects.get(id = int(productId))

    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
                cart_id = _cart_id(request)
                )
        cart.save()
    if request.user.is_authenticated:
            
            try:
                cart_item = CartItem.objects.get(product = product, customer__id = request.user.id)
                cart_item.quantity += quantity
                cart_item.save()
            except CartItem.DoesNotExist:
                cart_item = CartItem.objects.create(
                    product = product,
                    cart = cart,
                    quantity = quantity,
                    customer = Customer.objects.get(id = request.user.id)
                )
                cart_item.save()

            if cart_item.quantity>product.inventory:
                cart_item.quantity = product.inventory
                cart_item.save()


    else:

        try:
            cart_item = CartItem.objects.get(product = product,cart=cart)
            cart_item.quantity += quantity
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product = product,
                cart = cart,
                quantity = quantity
            )

            cart_item.save()

        if cart_item.quantity>product.inventory:
            cart_item.quantity = product.inventory
            cart_item.save()
    

    return redirect("shop:cart")

def setcart(request):
    
    
    data = json.loads(request.body)
    productId = data['productId']
    value = data['value']

    product = Product.objects.get(id = int(productId))

    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()

    if request.user.is_authenticated:

        # try:
        cart_item = CartItem.objects.get(product = product,customer__id=request.user.id)
        cart_item.quantity = int(value)
        cart_item.save()
        if cart_item.quantity>product.inventory:
            cart_item.quantity = product.inventory
            cart_item.save()
        # except CartItem.DoesNotExist:
        #     cart_item = CartItem.objects.create(
        #         product = product,
        #         cart = cart,
        #         quantity = value
        #     )
        #     cart_item.save()

    else:
        
        # try:
        cart_item = CartItem.objects.get(product = product,cart=cart)
        cart_item.quantity = value
        cart_item.save()
        if cart_item.quantity>product.inventory:
            cart_item.quantity = product.inventory
            cart_item.save()
        # except CartItem.DoesNotExist:
        #     cart_item = CartItem.objects.create(
        #         product = product,
        #         cart = cart,
        #         quantity = value
        #     )
        #     cart_item.save()


    return JsonResponse(cart.cart_id,safe=False)


def account(request,username):
    customerInstance = get_object_or_404(Customer,id = request.user.id)

    if request.method == "POST":
        form = EditForm(request.POST,instance = customerInstance)
        if form.is_valid():
            phone = request.POST.get("phone")
            country = request.POST.get("country")
            town = request.POST.get("town")
            state = request.POST.get("state")
            postal_code = request.POST.get("postal_code")
            current_password = request.POST.get("current_password")
            new_password = request.POST.get("new_password")
            confirm_password = request.POST.get("confirm_password")

            if phone:customerInstance.phone = phone
            if country:customerInstance.country = country
            if state:customerInstance.state = state
            if town:customerInstance.town = town
            if postal_code:customerInstance.postal_code = postal_code


            if current_password:
                user = authenticate(username=form.cleaned_data["username"],password = current_password)
                if not customerInstance.check_password(current_password):
                    passmessage = "Wrong password" 
                    return render(request,"shop/account.html",{'form':form,'passmessage':passmessage,'customer':customerInstance})
            if new_password:
                if not current_password:
                    passmessage = "Enter the current password "
                    return render (request,"shop/account.html",{'form':form,'passmessage':passmessage,'customer':customerInstance})

                if new_password != confirm_password:
                    confmessage = "Password Doedn't match"
                    return render (request,"shop/account.html",{'form':form,'confmessage':confmessage,'customer':customerInstance})
                customerInstance.set_password(new_password)
                customerInstance.save()
                return redirect("shop:login")

                # login(request,customerInstance)
            customerInstance.save()
            return render (request,"shop/account.html",{'form':form,'customer':customerInstance})

    else:
        form = EditForm(instance = customerInstance)  
        orders = Order.objects.filter(customer__id = request.user.id) 
    return render(request,"shop/account.html",{'form':form,'customer':customerInstance,"orders":orders})

def myOrders(request):
    orders = Order.objects.filter(customer__id = request.user.id)
    return render(request,"shop/account.html",{"orders":orders})



@login_required(login_url='shop:login')
def checkout(request):
    # if request.method != "POST":
        country_vat = 0.15
        subtotal = 0
        total_quantitiy = 0

        try:
            if request.user.is_authenticated:
                cart_items = CartItem.objects.filter(customer__id = request.user.id)

            else:
                cart = Cart.objects.get(cart_id = _cart_id(request))
                cart_items = CartItem.objects.filter(cart = cart)

            for cart_item in cart_items:
                subtotal += (float(cart_item.product.unit_price) * cart_item.quantity)
                total_quantitiy += cart_item.quantity
        except ObjectDoesNotExist:
            cart_items = None
            
        total = subtotal + subtotal * country_vat
        
        return render(request,"shop/checkout.html",{'cart_items':cart_items,'total':total,'total_quantity':total_quantitiy,"customer":Customer.objects.get(username = request.user.username)})

@login_required
def order(request):

    if request.method == "POST":
            

        country_vat = 0.15
        subtotal = 0

        try:
            if request.user.is_authenticated:
                cart_items = CartItem.objects.filter(customer__id = request.user.id)

            else:
                cart = Cart.objects.get(cart_id = _cart_id(request))
                cart_items = CartItem.objects.filter(cart = cart)

            for cart_item in cart_items:
                subtotal += (float(cart_item.product.unit_price) * cart_item.quantity)
        except ObjectDoesNotExist:
            cart_items = None
            

        total = subtotal + subtotal * country_vat

        order = Order.objects.create(
        
            phone = request.POST.get("phone"),
            country = request.POST.get("country"),
            town = request.POST.get("town"),
            state = request.POST.get("state"),
            postal_code = request.POST.get("postal_code"),
            first_name = request.POST.get("first_name"),
            last_name = request.POST.get("last_name"),
            email = request.POST.get("email"),
            payment_status = "C",
            customer = Customer.objects.get(username = request.user.username),
            total = total
        )
        order.save()

        cart_items = CartItem.objects.filter(customer__id = request.user.id)
        for cart_item in cart_items:
            order_item = OrderItem.objects.create(
                order = order,
                product = cart_item.product,
                quantity = cart_item.quantity,
                unit_price = cart_item.product.unit_price
            )
            order_item.save()

            product = Product.objects.get(id = cart_item.product.id)
            product.inventory -= cart_item.quantity
            product.save()

        CartItem.objects.filter(customer = request.user).delete()

        return render(request,"shop/success.html")
        


def product(request,product_id):
    product = Product.objects.get(pk = product_id)
    return render(request,"shop/product.html",{"product":product})

def categories(request,category_id):
    category = Category.objects.get(pk = category_id)
    products = category.products.all()
    return render(request,"shop/categories.html",{'products': list(products), 'category':category})


    


