from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('collection', views.CollectionViewSet)
router.register('reviews', views.ReviewViewSet)

urlpatterns = router.urls
# urlpatterns = router.urls
# urlpatterns = [
    # path('', include(router.urls))
    # path('product/', views.ProductList.as_view()),
    # path('product/<int:pk>/', views.ProductDetails.as_view()),
    # path('collection/', views.CollectionList.as_view()),
    # path('collection/<int:pk>/', views.CollectionDetails.as_view(), name='collection-detail')
# ]
"""
    pipenv install drf-nested-routers
"""