"""
Script para popular variações, imagens e avaliações de exemplo
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boss_shopp.settings')
django.setup()

from api.models import Product, ProductVariation, ProductImage, ProductReview, User
from datetime import datetime

def populate_variations():
    """Adiciona variações de exemplo aos produtos"""
    print("🎨 Adicionando variações aos produtos...")
    
    products = Product.objects.all()[:5]  # Primeiros 5 produtos
    
    variations_data = [
        # Tamanhos
        {'type': 'size', 'values': [
            ('P', 0),
            ('M', 0),
            ('G', 10),
            ('GG', 20),
        ]},
        # Cores
        {'type': 'color', 'values': [
            ('Preto', 0),
            ('Branco', 0),
            ('Azul', 5),
            ('Vermelho', 5),
        ]},
    ]
    
    count = 0
    for product in products:
        for var_data in variations_data:
            for value, adjustment in var_data['values']:
                variation, created = ProductVariation.objects.get_or_create(
                    product=product,
                    variation_type=var_data['type'],
                    variation_value=value,
                    defaults={
                        'price_adjustment': adjustment,
                        'stock_quantity': 10,
                        'sku': f"{product.id}-{var_data['type'][:3].upper()}-{value[:3].upper()}"
                    }
                )
                if created:
                    count += 1
                    print(f"  ✓ {product.name} - {var_data['type']}: {value}")
    
    print(f"\n✅ {count} variações adicionadas!")

def populate_reviews():
    """Adiciona avaliações de exemplo"""
    print("\n⭐ Adicionando avaliações aos produtos...")
    
    # Criar usuário de teste se não existir
    user, created = User.objects.get_or_create(
        email='teste@example.com',
        defaults={
            'username': 'usuario_teste',
            'first_name': 'Usuário',
            'last_name': 'Teste'
        }
    )
    if created:
        user.set_password('senha123')
        user.save()
        print(f"  ✓ Usuário de teste criado: {user.email}")
    
    products = Product.objects.all()[:5]
    
    reviews_data = [
        {
            'rating': 5,
            'title': 'Produto excelente!',
            'comment': 'Superou minhas expectativas. Qualidade muito boa e entrega rápida. Recomendo!',
        },
        {
            'rating': 4,
            'title': 'Muito bom',
            'comment': 'Produto de qualidade, apenas o prazo de entrega poderia ser melhor.',
        },
        {
            'rating': 5,
            'title': 'Adorei!',
            'comment': 'Exatamente como descrito. Muito satisfeito com a compra.',
        },
    ]
    
    count = 0
    for product in products:
        # Limpar avaliações existentes deste usuário
        ProductReview.objects.filter(product=product, user=user).delete()
        
        # Adicionar apenas uma avaliação por produto
        review_data = reviews_data[count % len(reviews_data)]
        review = ProductReview.objects.create(
            product=product,
            user=user,
            rating=review_data['rating'],
            title=review_data['title'],
            comment=review_data['comment'],
            verified_purchase=True,
            helpful_count=5
        )
        count += 1
        print(f"  ✓ {product.name} - {review.rating}⭐")
    
    print(f"\n✅ {count} avaliações adicionadas!")

def update_products():
    """Atualiza produtos com informações adicionais"""
    print("\n📦 Atualizando informações dos produtos...")
    
    products = Product.objects.all()[:10]
    
    brands = ['Nike', 'Adidas', 'Samsung', 'Apple', 'Sony', 'LG', 'Dell', 'HP']
    
    count = 0
    for i, product in enumerate(products):
        product.brand = brands[i % len(brands)]
        product.stock_quantity = 50
        product.weight = 0.5
        product.dimensions = '20x15x5 cm'
        product.is_active = True
        product.featured = i < 3  # Primeiros 3 são destaque
        product.discount_percentage = 10 if i % 2 == 0 else 0
        product.save()
        count += 1
        print(f"  ✓ {product.name} - {product.brand}")
    
    print(f"\n✅ {count} produtos atualizados!")

def main():
    print("🚀 POPULANDO DADOS DE EXEMPLO\n")
    
    try:
        update_products()
        populate_variations()
        populate_reviews()
        
        print("\n" + "="*60)
        print("✅ DADOS POPULADOS COM SUCESSO!")
        print("="*60)
        
        # Estatísticas
        print("\n📊 Estatísticas:")
        print(f"  • Produtos: {Product.objects.count()}")
        print(f"  • Variações: {ProductVariation.objects.count()}")
        print(f"  • Avaliações: {ProductReview.objects.count()}")
        print(f"  • Produtos em destaque: {Product.objects.filter(featured=True).count()}")
        print(f"  • Produtos com desconto: {Product.objects.filter(discount_percentage__gt=0).count()}")
        
        print("\n🌐 Teste a API em:")
        print("  http://localhost:8000/api/products/1/")
        print("  http://localhost:8000/api/products/1/stats/")
        print("  http://localhost:8000/api/products/search/?featured=true")
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
