from decimal import Decimal
from django.db import transaction
from rest_framework import serializers
from store.models import Cart, CartItem, Customer, Order, OrderItem, Product, Collection, ProductImage, Review
from .signals import order_created

class CollecionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'product_count']

    product_count = serializers.IntegerField()

    # def product_with_count(self, product: Product):
    #     return None

class ProductImageSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        product_id = self.context['product_id']
        return ProductImage.objects.create(product_id=product_id, **validated_data)
    class Meta:
        model = ProductImage
        fields = ['id', 'image']


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'title', 'description','slug', 'inventory', 'unit_price', 'price_with_tax', 'collection', 'images']
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)

    # def create(self, validated_data):
    #     product = Product(**validated_data)
    #     product.other = 1
    #     product.save()
    #     return product

    # def update(self, instance, validated_data):
    #     instance = validated_data.get('unit_price')
    #     instance.save()
    #     return instance


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'date', 'name', 'description']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']
class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField(method_name="get_total_price")

    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.unit_price
    class Meta:
        model = CartItem
        fields = ['id','product', 'quantity', 'total_price']

class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    
    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No Product with the given ID was found')
        return value
    
    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        
        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id = cart_id, **self.validated_data)
        return isinstance
    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']

class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']

class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart):
       return sum( [item.quantity * item.product.unit_price for item in cart.items.all()])

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']

class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'phone', 'birth_date', 'membership']

class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'unit_price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ['id', 'customer', 'placed_at', 'payment_status', 'items']
        
class UpdatPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['payment_status']
class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()
    
    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError('No cart with the given id')
        if CartItem.objects.filter(cart_id=cart_id).count() == 0:
            raise serializers.ValidationError('The cart is Empty')
        return cart_id
    
    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data['cart_id']
            customer = Customer.objects.get(user_id = self.context['user_id'])
            order = Order.objects.create(customer=customer)
            
            cart_items = CartItem.objects\
                        .select_related('product')\
                        .filter(cart_id = cart_id)
            orderItem = [
                OrderItem(
                    order = order,
                    product = item.product,
                    unit_price = item.product.unit_price,
                    quantity = item.quantity
                ) for item in cart_items
            ]
            
            OrderItem.objects.bulk_create(orderItem)
            
            Cart.objects.filter(pk=cart_id).delete()
            
            order_created.send_robust(self.__class__, order=order)
            
            return order
