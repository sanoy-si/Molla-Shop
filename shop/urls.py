from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

app_name = "shop"
urlpatterns = [
    path('',views.index, name = "index"),
    path('login/',views.login, name = "login"),
    path('signup/',views.signup, name = "signup"),
    path('about/',views.about, name = "about"),
    path('contact/',views.contact, name = "contact"),
    path('cart/',views.cart, name = "cart"),
    path('account/',views.account, name = "account"),
    path('checkout/',views.checkout, name = "checkout"),
    path('product/<int:product_id>',views.product, name = "product"),
    path('categories/<int:category_id>',views.categories, name = "categories"),
    path('addFromProduct/<int:productId>',views.addFromProduct, name = "addFromProduct"),
    path('setcart/',views.setcart, name = "setcart"),

    
    

]

    
urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)