from .models import Category,Cart,CartItem
from .views import _cart_id
def layout_context(request):
    categories = Category.objects.all()
    counter = 0
    if 'admin' in request.path:
        return {}
    try:
        cart = Cart.objects.filter(cart_id = _cart_id(request))
        if request.user.is_authenticated:
            cart_items =  CartItem.objects.filter(customer__id = request.user.id)
        else: 
            cart_items = CartItem.objects.filter(cart = cart[:1])
        for cart_item in cart_items:
            counter += cart_item.quantity
    except:
        pass

    return {
        'categories':categories ,
        'count':counter

    }

    

