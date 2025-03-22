from rest_framework import generics
from .models import Order, Transaction
from .serializers import OrderSerializer, TransactionSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from users.permissions import IsAdmin, IsTrader, IsSalesRep, IsCustomer

class AdminOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        return Response({"message": "This view is only accessible to Admins."})

class TraderOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsTrader]

    def get(self, request):
        return Response({"message": "This view is only accessible to Traders."})

class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsTrader]

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

class TransactionListView(generics.ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsSalesRep]    