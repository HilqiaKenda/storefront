from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Collection
from .serializers import ProductSerialier, CollecionSerializers

# Create your views here.

@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        queryset = Product.objects.select_related('collection').all()
        serializer = ProductSerialier(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = ProductSerialier(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # serializer.validated_data()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
        # if serializer.is_valid():
        #     serializer.validated_data
        #     return Response('ok')
        # else:
        #     return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
        
@api_view(['GET', 'PUT', 'DELETE'])
def product_details(request, id):
    product = get_object_or_404(Product, pk=id)
    if request.method == 'GET':
        serializer = ProductSerialier(product)
        return Response(serializer.data)
    if request.method == 'PUT':
        serializer = ProductSerialier(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    if request.method == 'DELETE':
        if product.orderitems.count() > 0:
            return Response({'error': 'This Product is associated with orderitem, it cannot be deleted now.'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.adelete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    # try:
    #     product = Product.objects.get(pk=id)
    #     serializer = ProductSerialier(product)
    #     return Response(serializer.data)
    # except:
    #     return Response(status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET', 'POST'])
def collection_list(request):
    if request.method == 'GET':
        queryset = Collection.objects.annotate(product_count=Count('productcollection')).all()
        serializer = CollecionSerializers(queryset, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = CollecionSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
@api_view(['GET', 'PUT', 'DELETE'])
def collection_detail(request, pk):
    collection = get_object_or_404(Collection.objects.annotate(product_count=Count('productcollection')), pk=pk)
    if request.method == 'GET':
        serializer = CollecionSerializers(collection)
        return Response(serializer.data)
    if request.method == 'PUT':
        serializer = CollecionSerializers(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    if request.method == 'DELETE':
        if collection.productcollection.count() > 0:
            return Response({'error': 'This Collection is associated with Product in orderitems, it cannot be deleted now.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)