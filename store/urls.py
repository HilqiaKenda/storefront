from django.urls import path, include
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)
router.register('carts', views.CartViewSet)
router.register('customers', views.CustomerViewSet)
router.register('orders', views.OrderViewSet, basename='orders')

prodcut_router = routers.NestedSimpleRouter(router, 'products', lookup='product')
prodcut_router.register('reviews', views.ReviewViewSet, basename='product-reviews')
prodcut_router.register('images', views.ProductImageViewSet, basename='product-images')

cart_router = routers.NestedSimpleRouter(router, 'carts', lookup='cart')
cart_router.register('items', views.CartItemViewSet, basename='cart-items')


urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(prodcut_router.urls)),
    path(r'', include(cart_router.urls)),
]
"""
    pipenv install drf-nested-routers
"""