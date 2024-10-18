from django.urls import path
from .views import CancelOrderView, ListOrdersForDrivers, RegisterView, LoginView, OrderTaxiView, PersonalInfoView, OrderHistoryView, TaxiDriverOrderListView, AcceptOrderView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('order-taxi/', OrderTaxiView.as_view(), name='order_taxi'),
    path('personal-info/', PersonalInfoView.as_view(), name='personal_info'),
    path('order-history/', OrderHistoryView.as_view(), name='order_history'),
    path('customer/orders/<int:pk>/cancel/', CancelOrderView.as_view(), name='cancel-order'),
    path('driver/orders/<int:pk>/accept/', AcceptOrderView.as_view(), name='accept-order'),
    path('driver/orders/', ListOrdersForDrivers.as_view(), name='list-orders-for-drivers'),

]
