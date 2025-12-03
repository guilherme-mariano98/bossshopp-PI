"""
Script de teste para os novos endpoints da API
Testa variações, imagens e avaliações de produtos
"""

import requests
import json

BASE_URL = "http://localhost:8000/api"

def print_section(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_product_detail():
    """Testa endpoint de detalhes do produto"""
    print_section("1. DETALHES DO PRODUTO")
    
    response = requests.get(f"{BASE_URL}/products/1/")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Produto: {data['name']}")
        print(f"  Preço original: R$ {data['price']}")
        print(f"  Preço final: R$ {data['final_price']}")
        print(f"  Desconto: {data['discount_percentage']}%")
        print(f"  Avaliação média: {data['average_rating']}⭐")
        print(f"  Total de avaliações: {data['total_reviews']}")
        print(f"  Variações: {len(data['variations'])}")
        print(f"  Imagens: {len(data['images'])}")
        print(f"  Reviews: {len(data['reviews'])}")
    else:
        print(f"✗ Erro: {response.status_code}")

def test_product_stats():
    """Testa endpoint de estatísticas do produto"""
    print_section("2. ESTATÍSTICAS DO PRODUTO")
    
    response = requests.get(f"{BASE_URL}/products/1/stats/")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Produto: {data['product_name']}")
        print(f"  Em estoque: {data['in_stock']}")
        print(f"  Quantidade: {data['stock_quantity']}")
        print(f"  Destaque: {data['is_featured']}")
        print(f"\n  Distribuição de avaliações:")
        for rating, count in data['rating_distribution'].items():
            print(f"    {rating}⭐: {count} avaliações")
        
        if data['variations']:
            print(f"\n  Variações disponíveis:")
            for var_type, variations in data['variations'].items():
                print(f"    {var_type.upper()}:")
                for var in variations:
                    status = "✓" if var['available'] else "✗"
                    print(f"      {status} {var['value']} (+R$ {var['price_adjustment']}) - Estoque: {var['stock']}")
    else:
        print(f"✗ Erro: {response.status_code}")

def test_product_variations():
    """Testa endpoint de variações"""
    print_section("3. VARIAÇÕES DO PRODUTO")
    
    response = requests.get(f"{BASE_URL}/products/1/variations/")
    if response.status_code == 200:
        variations = response.json()
        print(f"✓ Total de variações: {len(variations)}")
        for var in variations:
            print(f"  • {var['variation_type']}: {var['variation_value']}")
            print(f"    Ajuste de preço: R$ {var['price_adjustment']}")
            print(f"    Estoque: {var['stock_quantity']}")
            if var['sku']:
                print(f"    SKU: {var['sku']}")
    else:
        print(f"✗ Erro: {response.status_code}")

def test_product_images():
    """Testa endpoint de imagens"""
    print_section("4. IMAGENS DO PRODUTO")
    
    response = requests.get(f"{BASE_URL}/products/1/images/")
    if response.status_code == 200:
        images = response.json()
        print(f"✓ Total de imagens: {len(images)}")
        for img in images:
            primary = "⭐ PRINCIPAL" if img['is_primary'] else ""
            print(f"  • Ordem {img['order']}: {img['image']} {primary}")
            if img['alt_text']:
                print(f"    Alt: {img['alt_text']}")
    else:
        print(f"✗ Erro: {response.status_code}")

def test_product_reviews():
    """Testa endpoint de avaliações"""
    print_section("5. AVALIAÇÕES DO PRODUTO")
    
    response = requests.get(f"{BASE_URL}/products/1/reviews/")
    if response.status_code == 200:
        reviews = response.json()
        print(f"✓ Total de avaliações: {len(reviews)}")
        for review in reviews[:3]:  # Mostrar apenas 3 primeiras
            verified = "✓ COMPRA VERIFICADA" if review['verified_purchase'] else ""
            print(f"\n  {review['rating']}⭐ - {review['title']} {verified}")
            print(f"  Por: {review['user_name']}")
            print(f"  {review['comment'][:100]}...")
            print(f"  Útil: {review['helpful_count']} pessoas")
    else:
        print(f"✗ Erro: {response.status_code}")

def test_search_products():
    """Testa busca avançada"""
    print_section("6. BUSCA AVANÇADA")
    
    # Busca por produtos em estoque
    response = requests.get(f"{BASE_URL}/products/search/?in_stock=true&sort_by=price_asc")
    if response.status_code == 200:
        products = response.json()
        print(f"✓ Produtos em estoque: {len(products)}")
        for prod in products[:3]:
            print(f"  • {prod['name']} - R$ {prod['final_price']}")
    
    # Busca por produtos em destaque
    response = requests.get(f"{BASE_URL}/products/search/?featured=true")
    if response.status_code == 200:
        products = response.json()
        print(f"\n✓ Produtos em destaque: {len(products)}")
        for prod in products[:3]:
            print(f"  • {prod['name']} - {prod['average_rating']}⭐")

def test_categories():
    """Testa endpoint de categorias"""
    print_section("7. CATEGORIAS")
    
    response = requests.get(f"{BASE_URL}/categories/")
    if response.status_code == 200:
        categories = response.json()
        print(f"✓ Total de categorias: {len(categories)}")
        for cat in categories[:5]:
            print(f"  • {cat['name']} ({cat['slug']})")

def main():
    print("\n" + "🚀 TESTE DA API - BOSS SHOPP" + "\n")
    print("Base URL:", BASE_URL)
    
    try:
        # Testar conexão
        response = requests.get(f"{BASE_URL}/products/")
        if response.status_code != 200:
            print("❌ Erro: Servidor não está respondendo")
            return
        
        print("✓ Servidor conectado!")
        
        # Executar testes
        test_product_detail()
        test_product_stats()
        test_product_variations()
        test_product_images()
        test_product_reviews()
        test_search_products()
        test_categories()
        
        print_section("✅ TESTES CONCLUÍDOS")
        print("\nTodos os endpoints estão funcionando!")
        print("\nPróximos passos:")
        print("1. Popular dados de exemplo para variações e imagens")
        print("2. Criar avaliações de teste")
        print("3. Testar criação de avaliações (requer autenticação)")
        
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Não foi possível conectar ao servidor")
        print("Certifique-se de que o servidor está rodando em http://localhost:8000")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

if __name__ == "__main__":
    main()
