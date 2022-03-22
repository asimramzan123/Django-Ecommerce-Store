
from . import views
from django.urls import path, include


urlpatterns = [

    # Leave as empty string for base url
    path('', views.store, name = 'store' ),
    path('checkout/', views.checkout, name = 'checkout' ),
    path('cart/', views.cart, name = 'cart'),
    
    
    
]
