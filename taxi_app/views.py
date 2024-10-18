from django.db import transaction

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination

from taxi_app.permissions import IsCustomer, IsTaxiDriver
from .models import Order, User
from .serializers import RegisterSerializer, LoginSerializer, OrderSerializer, UserSerializer
from django.contrib.auth import authenticate


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')
        user = authenticate(phone_number=phone_number, password=password)
        
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'message': 'Login successful'
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid phone number or password'}, status=status.HTTP_400_BAD_REQUEST)


class OrderTaxiView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


class OrderHistoryView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)


class PersonalInfoView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class TaxiDriverOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(status=1).order_by('-order_time')


class AcceptOrderView(generics.UpdateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsTaxiDriver]

    def get_queryset(self):
        return Order.objects.filter(status=1)  # Only allow accepting "Waiting" orders

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        order = self.get_object()

        # Ensure the order is still in "Waiting" status
        if order.status != 1:
            return Response({"error": "This order has already been accepted."}, status=status.HTTP_400_BAD_REQUEST)

        # Atomically assign the current user as the driver and set status to "Accepted"
        order.taxi_driver = request.user
        order.status = 2  # 2 is the status for "Accepted"
        order.save()

        serializer = self.get_serializer(order)
        return Response(serializer.data)
        

class CancelOrderView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsCustomer] 
    serializer_class = OrderSerializer
    queryset = Order.objects.filter(status=1)  # Only allow canceling "Waiting" orders
    lookup_field = 'pk'  

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        order = self.get_object()

        if order.status != 1:
            return Response({"error": "Only orders that are in 'Waiting' status can be canceled."}, status=status.HTTP_400_BAD_REQUEST)

        # Update the status to "Canceled"
        order.status = 3  # 3 is the status for "Canceled"
        order.save()

        return Response({"message": "Order canceled successfully."}, status=status.HTTP_200_OK)


class OrderPagination(PageNumberPagination):
    page_size = 10  # Customize the number of orders per page

class ListOrdersForDrivers(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsTaxiDriver]  # Only authenticated taxi drivers can view
    pagination_class = OrderPagination  
    
    def get_queryset(self):
        return Order.objects.filter(status=1).order_by('-order_time') 
    