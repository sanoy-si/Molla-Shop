from .models import Category
def layout_context(request):
    categories = Category.objects.all()

    cartItemLength = len(request.session["cart"]) if "cart" in request.session else 0
    return {
        'categories':categories ,
        'cartItemLength':cartItemLength
    }


