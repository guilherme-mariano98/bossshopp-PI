from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    # Add related_name to avoid clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    
    # Novos campos
    brand = models.CharField(max_length=100, blank=True, null=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    weight = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, help_text='Peso em kg')
    dimensions = models.CharField(max_length=100, blank=True, null=True, help_text='Ex: 10x20x30 cm')
    is_active = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            return sum(r.rating for r in reviews) / len(reviews)
        return 0
    
    @property
    def total_reviews(self):
        return self.reviews.count()
    
    @property
    def final_price(self):
        if self.discount_percentage > 0:
            discount = self.price * (self.discount_percentage / 100)
            return self.price - discount
        return self.price

class ProductVariation(models.Model):
    """Variações de produto (tamanho, cor, etc)"""
    VARIATION_TYPE_CHOICES = [
        ('size', 'Tamanho'),
        ('color', 'Cor'),
        ('material', 'Material'),
        ('style', 'Estilo'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variations')
    variation_type = models.CharField(max_length=20, choices=VARIATION_TYPE_CHOICES)
    variation_value = models.CharField(max_length=100)
    price_adjustment = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text='Ajuste no preço')
    stock_quantity = models.PositiveIntegerField(default=0)
    sku = models.CharField(max_length=100, unique=True, blank=True, null=True)
    
    class Meta:
        unique_together = ['product', 'variation_type', 'variation_value']
    
    def __str__(self):
        return f"{self.product.name} - {self.get_variation_type_display()}: {self.variation_value}"

class ProductImage(models.Model):
    """Imagens adicionais do produto"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/gallery/')
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"Image for {self.product.name}"

class ProductReview(models.Model):
    """Avaliações de produtos"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])  # 1 a 5 estrelas
    title = models.CharField(max_length=200)
    comment = models.TextField()
    verified_purchase = models.BooleanField(default=False)
    helpful_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['product', 'user']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating}★)"

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    shipping_address = models.TextField()
    payment_method = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Order {self.id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"