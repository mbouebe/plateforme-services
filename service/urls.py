from django.urls import path
from .views import (
    LoginView, LogoutView,
    ClientListCreate, ClientRetrieveUpdateDestroy,
    ProviderListCreate, ProviderRetrieveUpdateDestroy,
    ReservationListCreate, ReservationRetrieveUpdateDestroy
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='api_login'),
    path('logout/', LogoutView.as_view(), name='api_logout'),
    path('clients/', ClientListCreate.as_view(), name='client_list_create'),
    path('clients/<int:pk>/', ClientRetrieveUpdateDestroy.as_view(), name='client_detail'),
    path('providers/', ProviderListCreate.as_view(), name='provider_list_create'),
    path('providers/<int:pk>/', ProviderRetrieveUpdateDestroy.as_view(), name='provider_detail'),
    path('reservations/', ReservationListCreate.as_view(), name='reservation_list_create'),
    path('reservations/<int:pk>/', ReservationRetrieveUpdateDestroy.as_view(), name='reservation_detail'),
]
