
from . import views
from django.urls import path, include


urlpatterns = [

    # Leave as empty string for base url
    path('', views.store, name = 'store' ),
    path('checkout/', views.checkout, name = 'checkout' ),
    path('cart/', views.cart, name = 'cart'),
    path('update_item/', views.update_item, name = 'update_item'),
    path('process_order/', views.process_order, name = 'process_order'),
    
    
    
    
    
]
