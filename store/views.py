from django.db.models.aggregates import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, DjangoModelPermissions
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework import status
from core.serializers import UserSeriliazer
from store.permissinos import DjangoFullPersimissions, IsAdminOrReadOnly, ViewCustomerHistoryPermission
from .filters import ProductFilter
from .models import Cart, CartItem, Customer, Product, Collection, OrderItem, Review
from .pagination import DefaultPagination
from .serializers import AddCartItemSerializer, CartItemSerializer, CartSerializer, CustomerSerializer, ProductSerializer, CollecionSerializer, ReviewSerializer, UpdateCartItemSerializer

# Create your views here.

"""
access token:{
}
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM1NzIxMzY2LCJpYXQiOjE3MzUxMTY1NjYsImp0aSI6IjZmZjVkN2JjMzg0ODRkM2FiY2Q1YTc2YjZiMDM5M2QxIiwidXNlcl9pZCI6NH0.8C8KKMDQMVucPmWgLnNmYdf9GubY57VvPqq1_oUybj8

"""

class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    filterset_class = ProductFilter
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['title', 'description']
    ordering_fields = ['id', 'title']
    
    def get_queryset(self):
        queryset = Product.objects.all()
        collection_id = self.request.query_params.get('collection_id')
        
        if collection_id:
            try:
                collection_id = int(collection_id)
                queryset = queryset.filter(collection_id=collection_id)
            except:
                raise ValueError("Invalid collection_id. It must be an integer.")
        return queryset
    
    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': 'This Product is associated with order item, it cannot be deleted now.'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        # Orderitem.adelete()
        return super().destroy(request, *args, **kwargs)
    
class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(product_count=Count('products')).all()
    serializer_class = CollecionSerializer 
    
    def destroy(self, request, *args, **kwargs):
        # if Collection.products.count() > 0:
        if Collection.objects.filter(products = kwargs['pk']).count() > 0:
            return Response({'error': 'This Collection is associated with Product in orderitems, it cannot be deleted now.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        return Review.objects.filter(product_id = self.kwargs['product_pk'])
    
    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}
    
class CartViewSet(CreateModelMixin, 
                  RetrieveModelMixin, 
                  DestroyModelMixin, 
                  GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer
    
class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer
    
    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}
    
    def get_queryset(self):
        return CartItem.objects \
            .filter(cart_id = self.kwargs['cart_pk']) \
                .select_related('product')

class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]
    
    @action(detail=True, permission_classes=[ViewCustomerHistoryPermission])
    def history(self, request, pk):
        return Response('ok')
    
    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        (customer, created) = Customer.objects.get_or_create(user_id=request.user.id)
        if request.method == "GET":
            serialize = CustomerSerializer(customer)
            return Response(serialize.data)
        elif request.method == 'PUT':
            serialize = CustomerSerializer(customer, data=request.data)
            serialize.is_valid(raise_exception=True)
            serialize.save()
            return Response(serialize.data)
    
class UserMEViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = UserSeriliazer
