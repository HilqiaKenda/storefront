from django.urls import path
from . import views

urlpatterns = [
    path('product/', views.product_list),
    path('product/<int:id>/', views.product_details),
    path('collection/', views.collection_list),
    path('collection/<int:pk>/', views.collection_detail, name='collection-detail')
]
