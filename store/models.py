from django.db import models
from django.contrib.auth.models import User



# Create your models here.

# Customer Model 
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank = True, null = True)
    name = models.CharField(null=True, blank=True, max_length=100)
    email = models.CharField(max_length = 100, blank = True, null = True)
    
    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=100, blank = True)
    price = models.FloatField()
    
    # digital product like pdf book etc , which don't need shipping
    digital = models.BooleanField(default=False, null=True, blank=True)
     
    # img field would be added later with some customization
    image = models.ImageField(null=True, blank=True)
        
    def __str__(self):
        return self.name
    
    # if image is not added in store, so prevent error
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    
    # if complete is false, it means we can continue adding items to cart, if Complete True, we can't add more.
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(blank=True, max_length=100)

    def __str__(self):
        return str(self.id)
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total 

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    
    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == 'False':
                shipping = True
        return shipping
    
    
# Items need to be added into Order with many to one relationship
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True )
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

    def __str__(self):
        return self.product.name


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True )
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True )
    address = models.CharField(max_length=254, null=False)
    city = models.CharField(max_length=254, null=False)
    state = models.CharField(max_length=254, null=False)
    zipcode = models.IntegerField(max_length=8, null=False)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.address
    
    
    
    
