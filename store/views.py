from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from .models import Product, Collection, OrderItem, Review
from .serializers import ProductSerialier, CollecionSerializer, ReviewSerializer

# Create your views here.

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerialier
    
    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': 'This Product is associated with order item, it cannot be deleted now.'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        # Orderitem.adelete()
        return super().destroy(request, *args, **kwargs)
    
    # def delete(self, request, pk):
    #     product = get_object_or_404(Product, pk=id)
    #     if product.orderitems.count() > 0:
    #         return Response({'error': 'This Product is associated with order item, it cannot be deleted now.'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     product.adelete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
        
    
# class ProductList(ListCreateAPIView):
    # queryset = Product.objects.all()
    # serializer_class = ProductSerialier
    
    # def get_queryset(self):
    #     return Product.objects.select_related('collection').all()
    
    # def get_serializer_class(self):
    #     return ProductSerialier
    
    # def get_serializer_context(self):
    #     return {'request': self.request}
    
    # def get(self, request):
    #     queryset = Product.objects.select_related('collection').all()
    #     serializer = ProductSerialier(queryset, many=True, context={'request': request})
    #     return Response(serializer.data)
        
    # def post(self, request):
    #     serializer = ProductSerialier(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     # serializer.validated_data()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        
# class ProductDetails(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerialier
#     lookup_field = 'id'
    
    # def get(self, request, id):
    #     product = get_object_or_404(Product, pk=id)
    #     serializer = ProductSerialier(product)
    #     return Response(serializer.data)
    
    # def put(self, request, id):
    #     product = get_object_or_404(Product, pk=id)
    #     serializer = ProductSerialier(product, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)
    
    # def delete(self, request, id):
    #     product = get_object_or_404(Product, pk=id)
    #     if product.orderitems.count() > 0:
    #         return Response({'error': 'This Product is associated with order item, it cannot be deleted now.'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     product.adelete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
        
        
class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(product_count=Count('products')).all()
    serializer_class = CollecionSerializer 
    
    def destroy(self, request, *args, **kwargs):
        # if Collection.products.count() > 0:
        if Collection.objects.filter(products = kwargs['pk']).count() > 0:
            return Response({'error': 'This Collection is associated with Product in orderitems, it cannot be deleted now.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
    
    # def delete(self, request, pk):
    #     collection = get_object_or_404(Collection.objects.annotate(product_count=Count('products')), pk=pk)
    #     if collection.products.count() > 0:
    #         return Response({'error': 'This Collection is associated with Product in orderitems, it cannot be deleted now.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     collection.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    
# class CollectionList(ListCreateAPIView):    
#     queryset = Collection.objects.annotate(product_count=Count('products')).all()
#     serializer_class = CollecionSerializer

# class CollectionDetails(RetrieveUpdateDestroyAPIView):
#     queryset = Collection.objects.all()
#     serializer_class = CollecionSerializer
    
    # def get(self, request, pk):
    #     collection = get_object_or_404(Collection.objects.annotate(product_count=Count('products')), pk=pk)
    #     serializer = CollecionSerializer(collection)
    #     return Response(serializer.data)
    
    # def put(self, request, pk):
    #     collection = get_object_or_404(Collection.objects.annotate(product_count=Count('products')), pk=pk)
    #     serializer = CollecionSerializer(collection, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)
        
    # def delete(self, request, pk):
    #     collection = get_object_or_404(Collection.objects.annotate(product_count=Count('products')), pk=pk)
    #     if collection.products.count() > 0:
    #         return Response({'error': 'This Collection is associated with Product in orderitems, it cannot be deleted now.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     collection.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    
class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}

    # def get_serializer_context(self):
    #     return {'product_id': self.kwargs['product_pk']}
    
    # def destroy(self, request, *args, **kwargs):
    #     return super().destroy(request, *args, **kwargs)