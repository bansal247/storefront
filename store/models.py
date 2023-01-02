from django.db import models


# Promotion - Product MANY-TO-MANY
class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()


# Create your models here.
class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey('Product', 
            on_delete=models.SET_NULL, null=True, related_name='+') #+ not to create reverse relationship

class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(null=True) #a-url-separated-with-hyphen
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2) #9999.99
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT) #for one to many
    promotions = models.ManyToManyField(Promotion)


class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE,'Bronze'),
        (MEMBERSHIP_SILVER,'Silver'),
        (MEMBERSHIP_GOLD,'Gold'),
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(choices=MEMBERSHIP_CHOICES, max_length=1, default=MEMBERSHIP_BRONZE)

    class Meta:
        indexes = [
            models.Index(fields=['last_name','first_name'])
        ]

class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'

    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING,'Pending'),
        (PAYMENT_STATUS_COMPLETE,'Complete'),
        {PAYMENT_STATUS_FAILED,'Failed'}
    ]
    placed_at = models.DateTimeField(auto_now=True)
    payment_status = models.CharField(choices=PAYMENT_STATUS_CHOICES, max_length=6, default=PAYMENT_STATUS_PENDING)
    customer = customer = models.ForeignKey(Customer, on_delete=models.PROTECT) #for one to many

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT) #for one to many
    product = models.ForeignKey(Product, on_delete=models.PROTECT) #for one to many
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2) #9999.99


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    #customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True) #for one to one
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE) #for one to many

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()