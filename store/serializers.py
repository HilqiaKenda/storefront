from decimal import Decimal
from rest_framework import serializers
from store.models import Product, Collection, Review

class CollecionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'product_count']

    product_count = serializers.IntegerField()

    # def product_with_count(self, product: Product):
    #     return None

class ProductSerialier(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description','slug', 'inventory', 'unit_price', 'price_with_tax', 'collection']
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