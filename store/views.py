from django.http import JsonResponse
from django.shortcuts import render
import json, datetime
from .models import *
from pprint import pprint

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
        cartItems = order.get_cart_items
        
    else:
        # shows this error if not logged in: local variable 'order' referenced before assignment
        items = []
        # this is what we would get without login
        order = {
            'get_cart_total':0,
            'get_cart_items':0,
            "shipping": False,
        }   
        cartItems = order.get_cart_items
        
    
    context = {
        'items':items,
        'order': order,
        'cartItems':cartItems,
 }
    return render(request, 'store/cart.html', context)


def store(request):
    
    if request.user.is_authenticated:
        
        # get customer as user
        customer = request.user.customer
        
        # get order or create one, and use the open cart(complete=false)
        order ,created = Order.objects.get_or_create(customer=customer, complete=False)
        
        # get the items attached to that orders
        # getting orderitems with parent item order
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        # shows this error if not logged in: local variable 'order' referenced before assignment
        items = []
        # this is what we would get without login
        order = {
            'get_cart_total':0,
            'get_cart_items':0,
            "shipping": False
        }   
        cartItems = order['get_cart_items']
        
    products = Product.objects.all() 
    context = {
        'products' : products,
        'cartItems':cartItems
        }
    return render(request, 'store/store.html', context)


def update_item(request):
    print("updating---item")
    # set value of data to response
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']


    # querying the customer
    customer = request.user
    print(customer.is_authenticated)
    # print(customer.customer)
    customer=customer.customer

    product = Product.objects.get(id= productId)
    order, created  = Order.objects.get_or_create(customer = customer, complete = False)
    # change the value of order if it already exists
    orderItem, created  = OrderItem.objects.get_or_create(order = order,  product = product)
    
    # adding logic for quantity control
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()
    
    if orderItem.quantity <= 0:
        orderItem.delete() 
    
    return JsonResponse('Item was added', safe = False)


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
        cartItems = order.get_cart_items
        
    else:
        # shows this error if not logged in: local variable 'order' referenced before assignment
        items = []
        cartItems = order.get_cart_items
        
        # this is what we would get without login
        order = {
            'get_cart_total': 0,
            'get_cart_items': 0,
            "shipping": False
            
        }   
    
    context = {
        'items':items,
        'order': order,
        'cartItems':cartItems
}
    return render(request, 'store/checkout.html', context)


def process_order(request):
    print('Data',request.body)
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    
    if request.user.is_authenticated:
        
        # get customer as user
        customer = request.user.customer
        order ,created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']["total"])
        order.transaction_id = transaction_id
        
        if total == order.get_cart_total:
            order.complete = True
        order.save()
        
        if order.shipping == True:
            ShippingAddress.objects.create(
                customer = customer,
                order = order,
                address = data['shipping']['address'],
                city = data['shipping']['city'],
                state = data['shipping']['state'],
                zipcode = data['shipping']['zipcode'],

            )
    else:
        print('User is not logged in.')
    
    return JsonResponse('Payment Complete', safe = False)