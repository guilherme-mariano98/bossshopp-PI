from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    User, Category, Product, Order, OrderItem,
    ProductVariation, ProductImage, ProductReview
)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

class ProductVariationInline(admin.TabularInline):
    model = ProductVariation
    extra = 1

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'final_price', 'stock_quantity', 'is_active', 'featured', 'average_rating', 'created_at')
    list_filter = ('category', 'is_active', 'featured', 'created_at')
    search_fields = ('name', 'description', 'brand')
    list_editable = ('is_active', 'featured')
    inlines = [ProductVariationInline, ProductImageInline]
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('name', 'description', 'category', 'brand', 'image')
        }),
        ('Preço e Estoque', {
            'fields': ('price', 'discount_percentage', 'stock_quantity')
        }),
        ('Detalhes Físicos', {
            'fields': ('weight', 'dimensions')
        }),
        ('Status', {
            'fields': ('is_active', 'featured')
        }),
    )

@admin.register(ProductVariation)
class ProductVariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_type', 'variation_value', 'price_adjustment', 'stock_quantity', 'sku')
    list_filter = ('variation_type', 'product__category')
    search_fields = ('product__name', 'variation_value', 'sku')

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'alt_text', 'is_primary', 'order')
    list_filter = ('is_primary', 'product__category')
    search_fields = ('product__name', 'alt_text')
    list_editable = ('is_primary', 'order')

@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'title', 'verified_purchase', 'helpful_count', 'created_at')
    list_filter = ('rating', 'verified_purchase', 'created_at')
    search_fields = ('product__name', 'user__username', 'title', 'comment')
    readonly_fields = ('verified_purchase', 'helpful_count', 'created_at', 'updated_at')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'user__email')
    inlines = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')