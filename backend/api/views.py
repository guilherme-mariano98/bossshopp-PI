from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from .models import User, Category, Product, Order
from .serializers import (
    UserSerializer, 
    CategorySerializer, 
    ProductSerializer, 
    OrderSerializer, 
    OrderCreateSerializer
)

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        # Set password properly
        user.set_password(request.data['password'])
        user.save()
        
        # Create token for the user
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data,
            'message': 'Conta criada com sucesso!'
        }, status=status.HTTP_201_CREATED)
    return Response({
        'error': 'Erro ao criar conta',
        'details': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    if email and password:
        # Find user by email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({
                'error': 'Credenciais inválidas'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check password
        if user.check_password(password):
            # Create or get token
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': UserSerializer(user).data
            })
        else:
            return Response({
                'error': 'Credenciais inválidas'
            }, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({
            'error': 'Email e senha são obrigatórios'
        }, status=status.HTTP_400_BAD_REQUEST)

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = Product.objects.all()
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category__slug=category)
        return queryset

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    permission_classes = [AllowAny]
    
    def get_serializer_class(self):
        from .serializers import ProductDetailSerializer
        return ProductDetailSerializer

class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user


# ============================================
# PRODUCT VARIATIONS, IMAGES & REVIEWS
# ============================================

from .models import ProductVariation, ProductImage, ProductReview
from .serializers import ProductVariationSerializer, ProductImageSerializer, ProductReviewSerializer

class ProductVariationListView(generics.ListAPIView):
    """Lista todas as variações de um produto específico"""
    serializer_class = ProductVariationSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        return ProductVariation.objects.filter(product_id=product_id)

class ProductImageListView(generics.ListAPIView):
    """Lista todas as imagens de um produto específico"""
    serializer_class = ProductImageSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        return ProductImage.objects.filter(product_id=product_id)

class ProductReviewListCreateView(generics.ListCreateAPIView):
    """Lista e cria avaliações de produtos"""
    serializer_class = ProductReviewSerializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]
    
    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        return ProductReview.objects.filter(product_id=product_id)
    
    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        
        # Verificar se o usuário já avaliou este produto
        if ProductReview.objects.filter(product=product, user=self.request.user).exists():
            from rest_framework.exceptions import ValidationError
            raise ValidationError("Você já avaliou este produto.")
        
        # Verificar se é uma compra verificada
        verified = Order.objects.filter(
            user=self.request.user,
            items__product=product,
            status='delivered'
        ).exists()
        
        serializer.save(
            user=self.request.user,
            product=product,
            verified_purchase=verified
        )

class ProductReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Detalhes, atualização e exclusão de avaliação"""
    serializer_class = ProductReviewSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ProductReview.objects.filter(user=self.request.user)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_review_helpful(request, review_id):
    """Marcar avaliação como útil"""
    review = get_object_or_404(ProductReview, id=review_id)
    review.helpful_count += 1
    review.save()
    return Response({
        'message': 'Avaliação marcada como útil',
        'helpful_count': review.helpful_count
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def product_stats(request, product_id):
    """Estatísticas detalhadas do produto"""
    product = get_object_or_404(Product, id=product_id)
    
    # Estatísticas de avaliações
    reviews = product.reviews.all()
    rating_distribution = {
        '5': reviews.filter(rating=5).count(),
        '4': reviews.filter(rating=4).count(),
        '3': reviews.filter(rating=3).count(),
        '2': reviews.filter(rating=2).count(),
        '1': reviews.filter(rating=1).count(),
    }
    
    # Variações disponíveis
    variations_by_type = {}
    for variation in product.variations.all():
        if variation.variation_type not in variations_by_type:
            variations_by_type[variation.variation_type] = []
        variations_by_type[variation.variation_type].append({
            'value': variation.variation_value,
            'price_adjustment': str(variation.price_adjustment),
            'stock': variation.stock_quantity,
            'available': variation.stock_quantity > 0
        })
    
    return Response({
        'product_id': product.id,
        'product_name': product.name,
        'average_rating': product.average_rating,
        'total_reviews': product.total_reviews,
        'rating_distribution': rating_distribution,
        'stock_quantity': product.stock_quantity,
        'in_stock': product.stock_quantity > 0,
        'variations': variations_by_type,
        'total_images': product.images.count(),
        'is_featured': product.featured,
        'discount_percentage': str(product.discount_percentage),
        'original_price': str(product.price),
        'final_price': str(product.final_price),
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def search_products(request):
    """Busca avançada de produtos"""
    queryset = Product.objects.filter(is_active=True)
    
    # Filtros
    search = request.GET.get('search', '')
    category = request.GET.get('category', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    min_rating = request.GET.get('min_rating', '')
    in_stock = request.GET.get('in_stock', '')
    featured = request.GET.get('featured', '')
    
    if search:
        queryset = queryset.filter(name__icontains=search) | queryset.filter(description__icontains=search)
    
    if category:
        queryset = queryset.filter(category__slug=category)
    
    if min_price:
        queryset = queryset.filter(price__gte=min_price)
    
    if max_price:
        queryset = queryset.filter(price__lte=max_price)
    
    if in_stock == 'true':
        queryset = queryset.filter(stock_quantity__gt=0)
    
    if featured == 'true':
        queryset = queryset.filter(featured=True)
    
    # Ordenação
    sort_by = request.GET.get('sort_by', 'created_at')
    if sort_by == 'price_asc':
        queryset = queryset.order_by('price')
    elif sort_by == 'price_desc':
        queryset = queryset.order_by('-price')
    elif sort_by == 'name':
        queryset = queryset.order_by('name')
    elif sort_by == 'newest':
        queryset = queryset.order_by('-created_at')
    
    serializer = ProductSerializer(queryset, many=True)
    return Response(serializer.data)
