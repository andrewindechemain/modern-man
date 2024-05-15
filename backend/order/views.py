from django.views.generic import ListView, DetailView, CreateView
from django.urls import path
from rest_framework import generics, viewsets
from .models import Product, Order, Cart, CoverImages,ButtonImages
from .serializers import ProductSerializer, CartSerializer, OrderSerializer, CoverImagesSerializer, ButtonImagesSerializer

# Create your views here.
class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        queryset = self.queryset
        category_name = self.request.query_params.get('category', None)
        if category_name is not None:
            queryset = queryset.filter(category__name=category_name)
        return queryset

class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CartCreateAPIView(generics.CreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class OrderCreateAPIView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class CoverImagesViewSet(viewsets.ModelViewSet):
    queryset = CoverImages.objects.all()
    serializer_class = CoverImagesSerializer
    
class ButtonImagesViewSet(viewsets.ModelViewSet):
    queryset = ButtonImages.objects.all()
    serializer_class = ButtonImagesSerializer