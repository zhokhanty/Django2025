from rest_framework import generics, status
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from users.permissions import IsAdmin, IsTrader, IsSalesRep, IsCustomer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated(), IsAdmin() or IsTrader()]

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsAdmin()]