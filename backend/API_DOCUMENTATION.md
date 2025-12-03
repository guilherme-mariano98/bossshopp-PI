# 📚 BOSS SHOPP - Documentação da API

## 🔗 Base URL
```
http://localhost:8000/api/
```

## 🔐 Autenticação

### Registrar Usuário
```http
POST /api/register/
Content-Type: application/json

{
  "username": "usuario",
  "email": "usuario@email.com",
  "password": "senha123",
  "first_name": "Nome",
  "last_name": "Sobrenome"
}
```

### Login
```http
POST /api/login/
Content-Type: application/json

{
  "email": "usuario@email.com",
  "password": "senha123"
}

Response:
{
  "token": "abc123...",
  "user": { ... }
}
```

### Perfil do Usuário
```http
GET /api/profile/
Authorization: Token abc123...
```

## 📦 Produtos

### Listar Produtos
```http
GET /api/products/
GET /api/products/?category=eletronicos
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Smartphone Premium",
    "description": "...",
    "price": "1760.00",
    "final_price": "1584.00",
    "discount_percentage": "10.00",
    "category": 2,
    "category_name": "Eletrônicos",
    "brand": "Samsung",
    "stock_quantity": 50,
    "weight": "0.18",
    "dimensions": "15x7x0.8 cm",
    "is_active": true,
    "featured": true,
    "average_rating": 4.5,
    "total_reviews": 10,
    "image": "/media/products/smartphone.jpg",
    "created_at": "2025-12-03T10:00:00Z"
  }
]
```

### Detalhes do Produto
```http
GET /api/products/{id}/
```

**Response inclui:**
- Informações básicas do produto
- Todas as variações (tamanho, cor, etc)
- Todas as imagens
- Todas as avaliações
- Estatísticas de rating

### Busca Avançada
```http
GET /api/products/search/?search=smartphone&category=eletronicos&min_price=1000&max_price=2000&in_stock=true&featured=true&sort_by=price_asc
```

**Parâmetros:**
- `search` - Busca no nome e descrição
- `category` - Slug da categoria
- `min_price` - Preço mínimo
- `max_price` - Preço máximo
- `in_stock` - true/false (apenas em estoque)
- `featured` - true/false (apenas destacados)
- `sort_by` - price_asc, price_desc, name, newest

### Estatísticas do Produto
```http
GET /api/products/{id}/stats/
```

**Response:**
```json
{
  "product_id": 1,
  "product_name": "Smartphone Premium",
  "average_rating": 4.5,
  "total_reviews": 10,
  "rating_distribution": {
    "5": 6,
    "4": 3,
    "3": 1,
    "2": 0,
    "1": 0
  },
  "stock_quantity": 50,
  "in_stock": true,
  "variations": {
    "color": [
      {
        "value": "Preto",
        "price_adjustment": "0.00",
        "stock": 20,
        "available": true
      },
      {
        "value": "Branco",
        "price_adjustment": "50.00",
        "stock": 15,
        "available": true
      }
    ],
    "size": [
      {
        "value": "128GB",
        "price_adjustment": "0.00",
        "stock": 25,
        "available": true
      },
      {
        "value": "256GB",
        "price_adjustment": "200.00",
        "stock": 10,
        "available": true
      }
    ]
  },
  "total_images": 5,
  "is_featured": true,
  "discount_percentage": "10.00",
  "original_price": "1760.00",
  "final_price": "1584.00"
}
```

## 🎨 Variações de Produtos

### Listar Variações
```http
GET /api/products/{product_id}/variations/
```

**Response:**
```json
[
  {
    "id": 1,
    "product": 1,
    "variation_type": "color",
    "variation_value": "Preto",
    "price_adjustment": "0.00",
    "stock_quantity": 20,
    "sku": "SMART-PRE-BLK-128"
  },
  {
    "id": 2,
    "product": 1,
    "variation_type": "size",
    "variation_value": "256GB",
    "price_adjustment": "200.00",
    "stock_quantity": 10,
    "sku": "SMART-PRE-BLK-256"
  }
]
```

**Tipos de Variação:**
- `size` - Tamanho
- `color` - Cor
- `material` - Material
- `style` - Estilo

## 🖼️ Imagens de Produtos

### Listar Imagens
```http
GET /api/products/{product_id}/images/
```

**Response:**
```json
[
  {
    "id": 1,
    "product": 1,
    "image": "/media/products/gallery/img1.jpg",
    "alt_text": "Vista frontal",
    "is_primary": true,
    "order": 0
  },
  {
    "id": 2,
    "product": 1,
    "image": "/media/products/gallery/img2.jpg",
    "alt_text": "Vista traseira",
    "is_primary": false,
    "order": 1
  }
]
```

## ⭐ Avaliações de Produtos

### Listar Avaliações
```http
GET /api/products/{product_id}/reviews/
```

**Response:**
```json
[
  {
    "id": 1,
    "product": 1,
    "user": 5,
    "user_name": "João Silva",
    "rating": 5,
    "title": "Excelente produto!",
    "comment": "Superou minhas expectativas. Recomendo!",
    "verified_purchase": true,
    "helpful_count": 15,
    "created_at": "2025-12-01T10:00:00Z",
    "updated_at": "2025-12-01T10:00:00Z"
  }
]
```

### Criar Avaliação
```http
POST /api/products/{product_id}/reviews/
Authorization: Token abc123...
Content-Type: application/json

{
  "rating": 5,
  "title": "Produto incrível!",
  "comment": "Muito bom, recomendo!"
}
```

**Regras:**
- Usuário deve estar autenticado
- Cada usuário pode avaliar um produto apenas uma vez
- Rating de 1 a 5 estrelas
- `verified_purchase` é automático (verifica se usuário comprou)

### Atualizar Avaliação
```http
PUT /api/reviews/{id}/
Authorization: Token abc123...
Content-Type: application/json

{
  "rating": 4,
  "title": "Título atualizado",
  "comment": "Comentário atualizado"
}
```

### Deletar Avaliação
```http
DELETE /api/reviews/{id}/
Authorization: Token abc123...
```

### Marcar Avaliação como Útil
```http
POST /api/reviews/{review_id}/helpful/
Authorization: Token abc123...
```

## 📂 Categorias

### Listar Categorias
```http
GET /api/categories/
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Eletrônicos",
    "slug": "eletronicos",
    "description": "Smartphones, notebooks e mais",
    "created_at": "2025-12-01T10:00:00Z"
  }
]
```

## 🛒 Pedidos

### Listar Pedidos do Usuário
```http
GET /api/orders/
Authorization: Token abc123...
```

### Criar Pedido
```http
POST /api/orders/
Authorization: Token abc123...
Content-Type: application/json

{
  "total_amount": "1760.00",
  "shipping_address": "Rua X, 123 - Cidade/UF",
  "payment_method": "credit_card",
  "items": [
    {
      "product": 1,
      "quantity": 2,
      "price": "880.00"
    }
  ]
}
```

### Detalhes do Pedido
```http
GET /api/orders/{id}/
Authorization: Token abc123...
```

## 📊 Exemplos de Uso

### Exemplo 1: Buscar Produtos em Promoção
```javascript
fetch('http://localhost:8000/api/products/search/?featured=true&sort_by=price_desc')
  .then(res => res.json())
  .then(data => console.log(data));
```

### Exemplo 2: Ver Detalhes Completos de um Produto
```javascript
// Buscar produto
const productId = 1;
const product = await fetch(`http://localhost:8000/api/products/${productId}/`).then(r => r.json());

// Buscar estatísticas
const stats = await fetch(`http://localhost:8000/api/products/${productId}/stats/`).then(r => r.json());

console.log('Produto:', product);
console.log('Estatísticas:', stats);
console.log('Avaliação média:', stats.average_rating);
console.log('Variações disponíveis:', stats.variations);
```

### Exemplo 3: Criar Avaliação
```javascript
const token = 'seu_token_aqui';

fetch('http://localhost:8000/api/products/1/reviews/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Token ${token}`
  },
  body: JSON.stringify({
    rating: 5,
    title: 'Produto excelente!',
    comment: 'Superou minhas expectativas!'
  })
})
.then(res => res.json())
.then(data => console.log('Avaliação criada:', data));
```

### Exemplo 4: Filtrar por Variação
```javascript
// Buscar produto com variações
const product = await fetch('http://localhost:8000/api/products/1/').then(r => r.json());

// Filtrar variações de cor
const cores = product.variations.filter(v => v.variation_type === 'color');
console.log('Cores disponíveis:', cores);

// Filtrar variações de tamanho
const tamanhos = product.variations.filter(v => v.variation_type === 'size');
console.log('Tamanhos disponíveis:', tamanhos);
```

## 🔒 Códigos de Status HTTP

- `200 OK` - Sucesso
- `201 Created` - Recurso criado
- `400 Bad Request` - Dados inválidos
- `401 Unauthorized` - Não autenticado
- `403 Forbidden` - Sem permissão
- `404 Not Found` - Recurso não encontrado
- `500 Internal Server Error` - Erro no servidor

## 💡 Dicas

1. **Paginação**: A API retorna 20 itens por página por padrão
2. **Autenticação**: Use `Authorization: Token {seu_token}` no header
3. **Filtros**: Combine múltiplos filtros para busca precisa
4. **Cache**: Considere cachear dados de categorias e produtos
5. **Imagens**: URLs de imagens são relativas, adicione o domínio base

---

**Última Atualização:** 2025-12-03  
**Versão da API:** 2.0
