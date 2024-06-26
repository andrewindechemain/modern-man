import random
from rest_framework import generics, viewsets,status
from django.utils import timezone
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Product, Order, Cart, CartItem, CoverImages,ProductDiscountFilter, Customer
from .serializers import ProductSerializer, CustomTokenObtainPairSerializer, CartSerializer, OrderSerializer,RegisterSerializer, FavoriteCountSerializer
from .serializers import CoverImagesSerializer,EmailSerializer, ChargeSerializer, MpesaTransactionSerializer, AddToCartSerializer
from .utils.mpesa_utils import lipa_na_mpesa_online 
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from .utils.mpesa_utils import process_mpesa_callback
from django.core.mail import send_mail
from .serializers import EmailSerializer


stripe.api_key = settings.STRIPE_SECRET_KEY

class ProductListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        queryset = Product.objects.all()
        category_name = self.request.query_params.get('category', None)
        if category_name is not None:
            queryset = queryset.filter(category__name=category_name)
        return queryset


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
class ProductSearchView(generics.GenericAPIView):
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        query = request.GET.get('query', '')
        products = Product.objects.filter(name__icontains=query)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
    
class DiscountedProductListAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_class = ProductDiscountFilter

    def get_queryset(self):
        return Product.objects.filter(discount_percentage__gt=0)
    
class FavoriteListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return user.favorites.all()
    
class FavoriteCountView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FavoriteCountSerializer

    def get_queryset(self):
        return Customer.objects.filter(id=self.request.user.id).annotate(count=Count('favorites'))

    def list(self, request, *args, **kwargs):
        user = self.get_queryset().first()
        count = user.count if user else 0
        serializer = self.get_serializer({'count': count})
        return Response(serializer.data)
        
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class CartCreateAPIView(generics.CreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class AddToCartView(generics.GenericAPIView):
    serializer_class = AddToCartSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data['product_id']
            quantity = serializer.validated_data['quantity']

            try:
                product = Product.objects.get(id=product_id)
                cart, created = Cart.objects.get_or_create(user=request.user)
                cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
                if created:
                    cart_item.quantity = quantity
                else:
                    cart_item.quantity += quantity
                cart_item.subtotal = cart_item.quantity * product.price
                cart_item.save()
                return Response({'message': 'Item added to cart'}, status=status.HTTP_200_OK)
            except Product.DoesNotExist:
                return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderCreateAPIView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class CoverImagesViewSet(viewsets.ModelViewSet):
    queryset = CoverImages.objects.all()
    serializer_class = CoverImagesSerializer
    
class StripeChargeView(generics.GenericAPIView):
    serializer_class = ChargeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        stripe_token = serializer.validated_data['stripe_token']
        amount = serializer.validated_data['amount']
        currency = serializer.validated_data['currency']
        description = serializer.validated_data.get('description', 'A Django charge')

        try:
            charge = stripe.Charge.create(
                amount=amount,
                currency=currency,
                description=description,
                source=stripe_token,
            )
            return Response({'charge': charge}, status=status.HTTP_200_OK)
        except stripe.error.StripeError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class SearchSuggestionsView(generics.GenericAPIView):
    serializer_class = ProductSerializer
    
    def get(self, request, *args, **kwargs):
        query = request.GET.get('query', '')
        if query:
            suggestions = Product.objects.filter(name__istartswith=query).order_by('name')[:10]
            serializer = self.get_serializer(suggestions, many=True)
            return Response(serializer.data)
        return Response([])
    
class MpesaChargeView(generics.GenericAPIView):
    serializer_class = MpesaTransactionSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data.get('phone_number')
            amount = serializer.validated_data.get('amount')
            account_reference = serializer.validated_data.get('account_reference', 'Test123')
            transaction_desc = serializer.validated_data.get('transaction_desc', 'Payment for XYZ')

            # Initiate the M-Pesa transaction
            response = lipa_na_mpesa_online(phone_number, amount, account_reference, transaction_desc)

            # Save transaction in the database
            if response.get('ResponseCode') == '0':  # assuming '0' is success
                serializer.save(status='Success')
            else:
                serializer.save(status='Failed')

            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def send_email(request):
    if request.method == 'POST':
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            try:
                send_mail(serializer.validated_data['subject'],
                          serializer.validated_data['text'],
                          'sender@example.com',
                          [serializer.validated_data['to']])
                return Response({'message': 'Email sent successfully'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Only POST requests are allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

def get_stripe_public_key(request):
    return JsonResponse({'publicKey': settings.STRIPE_PUBLISHABLE_KEY})

def get_mpesa_public_key(request):
    return JsonResponse({'publicKey': settings.MPESA_CONSUMER_KEY})
    
@csrf_exempt
def mpesa_callback(request):
    return process_mpesa_callback(request)
