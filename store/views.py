from django.shortcuts import render
from .models import *
# Create your views here.


def cart(request):
    
    # check out if user is authenticated(logedin)
    if request.user.is_authenticated:
        
        # get customer as user
        customer = request.user.customer
        
        # get order or create one, and use the open cart(complete=false)
        order ,created = Order.objects.get_or_create(customer=customer, complete=False)
        
        # get the items attached to that orders
        # getting orderitems with parent item order
        items = order.orderitem_set.all()
    else:
        # shows this error if not logged in: local variable 'order' referenced before assignment
        items = []
        # this is what we would get without login
        order = {
            'get_cart_total':0,
            'get_cart_items':0
        }
        
        
    
    context = {
        'items':items,
        'order': order,
               }
    return render(request, 'store/cart.html', context)


def store(request):
    
    products = Product.objects.all()
    
    context = {
        'products' : products,
        
        }
    return render(request, 'store/store.html', context)


def checkout(request):
    # check out if user is authenticated(logedin)
    if request.user.is_authenticated:
        
        # get customer as user
        customer = request.user.customer
        
        # get order or create one, and use the open cart(complete=false)
        order ,created = Order.objects.get_or_create(customer=customer, complete=False)
        
        # get the items attached to that orders
        # getting orderitems with parent item order
        items = order.orderitem_set.all()
    else:
        # shows this error if not logged in: local variable 'order' referenced before assignment
        items = []
        # this is what we would get without login
        order = {
            'get_cart_total':0,
            'get_cart_items':0
        }   
    
    context = {
        'items':items,
        'order': order,
               }
    return render(request, 'store/checkout.html', context)