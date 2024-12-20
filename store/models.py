from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.
class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()

    #products
class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+')
    
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['title']

class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(null=True, blank=True)
    unit_price = models.DecimalField(validators=[MinValueValidator(5)], max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete= models.PROTECT, related_name='products')
    promotion = models.ManyToManyField(Promotion, blank=True)
    
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ["title"]
        
class Customer(models.Model):
    MEMBERSHIP_BRONZE='B'
    MEMBERSHIP_SILVER='S'
    MEMBERSHIP_GOLDEN='G'
    
    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLDEN, 'Golden'),
    ]
    
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
    
    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        ordering = ["first_name", "last_name"]

class Order(models.Model):
    payment_pending = 'p'
    payment_complete = 'C'
    payment_failed = 'F'
    PAYMENT_STATUS_CHOICES = [
        (payment_pending, 'pending'),
        (payment_complete, 'complete'),
        (payment_failed, 'failed'),
    ]
    
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES, default=payment_pending)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    
    
class Items(models.Model):
    product = models.CharField(max_length=255)
    
    
class Cart(models.Model):
    item = models.ForeignKey(Items, on_delete=models.CASCADE)

    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete= models.PROTECT, related_name='orderitems')
    quantity =models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=5, decimal_places=2)


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=6)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete= models.CASCADE)
    product = models.ForeignKey(Product, on_delete= models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
    
class Review(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)