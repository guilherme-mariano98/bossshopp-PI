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


# ============================================
# PASSWORD RESET
# ============================================

from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import timedelta

# Armazenamento temporário de tokens (em produção, use Redis ou banco de dados)
password_reset_tokens = {}

@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_request(request):
    """Solicita recuperação de senha"""
    email = request.data.get('email')
    
    if not email:
        return Response({
            'error': 'Email é obrigatório'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        # Por segurança, não revelar se o email existe
        return Response({
            'message': 'Se o email existir, você receberá instruções para redefinir sua senha.'
        }, status=status.HTTP_200_OK)
    
    # Gerar token único
    token = get_random_string(64)
    expiry = timezone.now() + timedelta(hours=1)
    
    # Armazenar token (em produção, use banco de dados ou Redis)
    password_reset_tokens[token] = {
        'user_id': user.id,
        'expiry': expiry
    }
    
    # Criar link de recuperação
    reset_link = f"http://localhost:8000/reset-password.html?token={token}"
    
    # Enviar email (em desenvolvimento, apenas log)
    try:
        # Em produção, configure SMTP no settings.py
        print(f"\n{'='*60}")
        print(f"EMAIL DE RECUPERAÇÃO DE SENHA")
        print(f"{'='*60}")
        print(f"Para: {email}")
        print(f"Assunto: Recuperação de Senha - BOSS SHOPP")
        print(f"\nOlá {user.first_name},")
        print(f"\nVocê solicitou a recuperação de senha.")
        print(f"Clique no link abaixo para criar uma nova senha:")
        print(f"\n{reset_link}")
        print(f"\nEste link expira em 1 hora.")
        print(f"{'='*60}\n")
        
        # Descomentar em produção com SMTP configurado:
        # send_mail(
        #     'Recuperação de Senha - BOSS SHOPP',
        #     f'Olá {user.first_name},\n\nClique no link para redefinir sua senha:\n{reset_link}\n\nEste link expira em 1 hora.',
        #     settings.DEFAULT_FROM_EMAIL,
        #     [email],
        #     fail_silently=False,
        # )
    except Exception as e:
        print(f"Erro ao enviar email: {e}")
    
    return Response({
        'message': 'Se o email existir, você receberá instruções para redefinir sua senha.',
        'reset_link': reset_link  # Apenas para desenvolvimento
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_confirm(request):
    """Confirma e redefine a senha"""
    token = request.data.get('token')
    new_password = request.data.get('password')
    
    if not token or not new_password:
        return Response({
            'error': 'Token e senha são obrigatórios'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Verificar token
    token_data = password_reset_tokens.get(token)
    
    if not token_data:
        return Response({
            'error': 'Token inválido ou expirado'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Verificar expiração
    if timezone.now() > token_data['expiry']:
        del password_reset_tokens[token]
        return Response({
            'error': 'Token expirado. Solicite um novo link de recuperação.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Validar senha
    if len(new_password) < 8:
        return Response({
            'error': 'A senha deve ter no mínimo 8 caracteres'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Atualizar senha
    try:
        user = User.objects.get(id=token_data['user_id'])
        user.set_password(new_password)
        user.save()
        
        # Remover token usado
        del password_reset_tokens[token]
        
        return Response({
            'message': 'Senha redefinida com sucesso!'
        }, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({
            'error': 'Usuário não encontrado'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """Alterar senha (usuário autenticado)"""
    current_password = request.data.get('current_password')
    new_password = request.data.get('new_password')
    
    if not current_password or not new_password:
        return Response({
            'error': 'Senha atual e nova senha são obrigatórias'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user = request.user
    
    # Verificar senha atual
    if not user.check_password(current_password):
        return Response({
            'error': 'Senha atual incorreta'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Validar nova senha
    if len(new_password) < 8:
        return Response({
            'error': 'A nova senha deve ter no mínimo 8 caracteres'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Atualizar senha
    user.set_password(new_password)
    user.save()
    
    return Response({
        'message': 'Senha alterada com sucesso!'
    }, status=status.HTTP_200_OK)
