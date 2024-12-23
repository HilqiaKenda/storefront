from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collection', views.CollectionViewSet)
# router.register('reviews', views.ReviewViewSet)

prodcut_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
prodcut_router.register('reviews', views.ReviewViewSet, basename='product-reviews')

# urlpatterns = router.urls + prodcut_router.urls
# urlpatterns = router.urls
urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(prodcut_router.urls)),
    # path('product/', views.ProductList.as_view()),
    # path('product/<int:pk>/', views.ProductDetails.as_view()),
    # path('collection/', views.CollectionList.as_view()),
    # path('collection/<int:pk>/', views.CollectionDetails.as_view(), name='collection-detail')
]
"""
    pipenv install drf-nested-routers
"""