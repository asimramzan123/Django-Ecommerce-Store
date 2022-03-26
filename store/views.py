from re import T
from django.http import JsonResponse
from django.shortcuts import render
import json, datetime
from .models import *
from .utils import cookieCart, cartData, guestOrder
from pprint import pprint


def store(request):

    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all() 
    context = {
        'products' : products,
        'cartItems':cartItems
        }
    return render(request, 'store/store.html', context)


def cart(request):
    
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']     
 
    context = {
        'items':items,
        'order': order,
        'cartItems':cartItems,
 }
    return render(request, 'store/cart.html', context)


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
    
    data = cartData(request)
    cartItems = data['carcustomertItems']
    order = data['order']
    items = data['items']
        
    context = {
        'items':items,
        'order': order,
        'cartItems':cartItems
}
    return render(request, 'store/checkout.html', context)

def process_order(request):
    
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    
    if request.user.is_authenticated:
        customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    
    else: 
        customer, order = guestOrder(request, data)
        
    total = float(data['form']['total'])
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
    return JsonResponse('Payment submitted..', safe=False)


    