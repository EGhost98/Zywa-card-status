from django.urls import path, include
from . import views

urlpatterns = [
    path('refresh/pickup', views.refresh_pickup, name='refresh_card_status'),
    path('refresh/delivered', views.refresh_delivered, name='refresh_card_status'),
    path('refresh/delivery-exceptions', views.refresh_delivery_exceptions, name='refresh_card_status'),
    path('refresh/returned', views.refresh_returned, name='refresh_card_status'),
    path('get-card-status', views.get_card_status, name='get_card_status'),
]
