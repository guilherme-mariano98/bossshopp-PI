from django.urls import path
from . import views

urlpatterns = [
    # Autenticação
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    
    # Categorias
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    
    # Produtos
    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('products/search/', views.search_products, name='product-search'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('products/<int:product_id>/stats/', views.product_stats, name='product-stats'),
    
    # Variações de Produtos
    path('products/<int:product_id>/variations/', views.ProductVariationListView.as_view(), name='product-variations'),
    
    # Imagens de Produtos
    path('products/<int:product_id>/images/', views.ProductImageListView.as_view(), name='product-images'),
    
    # Avaliações de Produtos
    path('products/<int:product_id>/reviews/', views.ProductReviewListCreateView.as_view(), name='product-reviews'),
    path('reviews/<int:pk>/', views.ProductReviewDetailView.as_view(), name='review-detail'),
    path('reviews/<int:review_id>/helpful/', views.mark_review_helpful, name='review-helpful'),
    
    # Pedidos
    path('orders/', views.OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
]