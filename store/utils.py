import json
from .models import *


def cookieCart(request):
    try:
        # getting cookie for cart items
        cart = json.loads(request.COOKIES['cart'])
    except:
        # if cart cookie is not available
        cart = {}
        
    print('Cart', cart)
    
    # shows this error if not logged in: local variable 'order' referenced before assignment
    items = []
    # this is what we would get without login
    order = {
        'get_cart_total':0,
        'get_cart_items':0,
        "shipping": False,
    }   
    cartItems = order["get_cart_items"]
    
    # looping through and updating cart items
    for i in cart:
        # incase product is not available in database , so to prevent error
        try:
            cartItems += cart[i]["quantity"]
            
            # query the products by id
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]["quantity"])
            
            # update cart total
            order["get_cart_total"] += total
            
            # updating for actual items
            order["get_cart_items"] += cart[i]["quantity"]
        
            # converting item dictionery data into displayable data
            item = {
                # first attribute of an item
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'imageURL':product.imageURL,    
                },
                # second and third attribute of an item
                'quantity':cart[i]['quantity'],
                'get_total':total
            }
            
            items.append(item)
            
            if product.digital == False:
                order['shipping'] = True 
                
        except:
            pass  

    
    return {
        'cartItems':cartItems, 
        'order':order,  
        'items':items
        }
    

def cartData(request):
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
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
     
    return {
        'cartItems': cartItems, 
        'order':order,  
        'items':items
        }


def guestOrder(request, data):
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created = Customer.objects.get_or_create(
			email=email,
			)
    customer.name = name
    customer.save()

    order = Order.objects.create(
		customer=customer,
		complete=False,
		)
    for item in items:
	    product = Product.objects.get(id=item['id'])
        orderItem = OrderItem.objects.create
        (
			product=product,
			order=order,
			quantity=item['quantity'],
            # if:
            #     item['quantity'] >0
            # else:
            # -1*item['quantity']) # negative quantity = freebies
		)
    return customer, order