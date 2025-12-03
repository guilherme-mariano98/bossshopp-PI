# 🗄️ BOSS SHOPP - Documentação do Banco de Dados SQLite

## 📋 Visão Geral

Este documento descreve a estrutura completa do banco de dados SQLite do sistema BOSS SHOPP E-commerce.

## 🏗️ Estrutura do Banco de Dados

### Tabelas Principais

#### 1. **api_user** - Usuários do Sistema
Armazena informações dos usuários cadastrados.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | INTEGER | ID único do usuário |
| username | VARCHAR(150) | Nome de usuário único |
| email | VARCHAR(254) | Email único |
| password | VARCHAR(128) | Hash da senha |
| first_name | VARCHAR(150) | Primeiro nome |
| last_name | VARCHAR(150) | Sobrenome |
| is_active | BOOLEAN | Conta ativa |
| is_staff | BOOLEAN | Acesso ao admin |
| is_superuser | BOOLEAN | Superusuário |
| date_joined | DATETIME | Data de registro |
| created_at | DATETIME | Data de criação |

#### 2. **api_category** - Categorias de Produtos
Categorias para organização dos produtos.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | INTEGER | ID único da categoria |
| name | VARCHAR(100) | Nome da categoria |
| slug | VARCHAR(50) | Slug único para URLs |
| description | TEXT | Descrição da categoria |
| created_at | DATETIME | Data de criação |

**Categorias Disponíveis:**
- Moda
- Eletrônicos
- Casa
- Games
- Esportes
- Infantil
- Beleza
- Livros
- Automotivo
- Pet Shop
- Alimentos
- Ferramentas
- Música
- Papelaria
- Saúde
- Brinquedos

#### 3. **api_product** - Produtos
Catálogo de produtos disponíveis na loja.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | INTEGER | ID único do produto |
| name | VARCHAR(200) | Nome do produto |
| description | TEXT | Descrição detalhada |
| price | DECIMAL(10,2) | Preço do produto |
| category_id | INTEGER | ID da categoria |
| image | VARCHAR(100) | Caminho da imagem |
| created_at | DATETIME | Data de criação |
| updated_at | DATETIME | Data de atualização |

#### 4. **api_order** - Pedidos
Pedidos realizados pelos usuários.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | INTEGER | ID único do pedido |
| user_id | INTEGER | ID do usuário |
| total_amount | DECIMAL(10,2) | Valor total |
| status | VARCHAR(20) | Status do pedido |
| shipping_address | TEXT | Endereço de entrega |
| payment_method | VARCHAR(50) | Método de pagamento |
| created_at | DATETIME | Data de criação |
| updated_at | DATETIME | Data de atualização |

**Status Possíveis:**
- `pending` - Pendente
- `processing` - Processando
- `shipped` - Enviado
- `delivered` - Entregue
- `cancelled` - Cancelado

#### 5. **api_orderitem** - Itens do Pedido
Itens individuais de cada pedido.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | INTEGER | ID único do item |
| order_id | INTEGER | ID do pedido |
| product_id | INTEGER | ID do produto |
| quantity | INTEGER | Quantidade |
| price | DECIMAL(10,2) | Preço unitário |

### Tabelas de Autenticação

#### **authtoken_token** - Tokens de API
Tokens para autenticação da API REST.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| key | VARCHAR(40) | Token único |
| created | DATETIME | Data de criação |
| user_id | INTEGER | ID do usuário |

## 📊 Views (Consultas Pré-definidas)

### 1. **vw_products_with_category**
Lista produtos com informações da categoria.

```sql
SELECT * FROM vw_products_with_category;
```

### 2. **vw_orders_complete**
Lista pedidos completos com informações do usuário.

```sql
SELECT * FROM vw_orders_complete;
```

### 3. **vw_sales_by_category**
Estatísticas de vendas por categoria.

```sql
SELECT * FROM vw_sales_by_category;
```

### 4. **vw_top_products**
Produtos mais vendidos.

```sql
SELECT * FROM vw_top_products LIMIT 10;
```

### 5. **vw_active_users**
Usuários ativos com estatísticas de compras.

```sql
SELECT * FROM vw_active_users;
```

## 🔧 Como Usar

### Aplicar o Schema

1. **Via Python:**
```bash
cd backend
python apply_schema.py
```

2. **Via SQLite CLI:**
```bash
cd backend
sqlite3 db.sqlite3 < database_schema_sqlite.sql
```

### Consultas Úteis

#### Listar todas as categorias:
```sql
SELECT * FROM api_category ORDER BY name;
```

#### Listar produtos de uma categoria:
```sql
SELECT p.* 
FROM api_product p
JOIN api_category c ON p.category_id = c.id
WHERE c.slug = 'eletronicos';
```

#### Buscar produtos por nome:
```sql
SELECT * FROM api_product 
WHERE name LIKE '%smartphone%';
```

#### Ver pedidos de um usuário:
```sql
SELECT o.*, u.username, u.email
FROM api_order o
JOIN api_user u ON o.user_id = u.id
WHERE u.email = 'usuario@email.com';
```

#### Produtos mais caros:
```sql
SELECT name, price, category_id
FROM api_product
ORDER BY price DESC
LIMIT 10;
```

#### Total de vendas por categoria:
```sql
SELECT * FROM vw_sales_by_category
ORDER BY total_revenue DESC;
```

## 🔐 Índices

O banco possui índices otimizados para:
- Busca por email e username de usuários
- Busca por slug de categorias
- Filtros por categoria de produtos
- Consultas de pedidos por usuário e status
- Ordenação por data de criação

## 🚀 Triggers Automáticos

### 1. **trg_product_update_timestamp**
Atualiza automaticamente o campo `updated_at` quando um produto é modificado.

### 2. **trg_order_update_timestamp**
Atualiza automaticamente o campo `updated_at` quando um pedido é modificado.

## 📈 Estatísticas

Para ver estatísticas do banco de dados:

```python
python apply_schema.py
```

Ou via SQL:

```sql
-- Contar registros por tabela
SELECT 
    'Usuários' as Tabela, COUNT(*) as Total FROM api_user
UNION ALL SELECT 'Categorias', COUNT(*) FROM api_category
UNION ALL SELECT 'Produtos', COUNT(*) FROM api_product
UNION ALL SELECT 'Pedidos', COUNT(*) FROM api_order
UNION ALL SELECT 'Itens de Pedido', COUNT(*) FROM api_orderitem;
```

## 🔄 Backup e Restauração

### Criar Backup:
```bash
# Windows
copy db.sqlite3 db_backup.sqlite3

# Linux/Mac
cp db.sqlite3 db_backup.sqlite3
```

### Restaurar Backup:
```bash
# Windows
copy db_backup.sqlite3 db.sqlite3

# Linux/Mac
cp db_backup.sqlite3 db.sqlite3
```

## 📝 Notas Importantes

1. **Integridade Referencial**: Todas as chaves estrangeiras possuem `ON DELETE CASCADE`
2. **Encoding**: UTF-8 para suporte completo a caracteres especiais
3. **Timestamps**: Todos os timestamps são armazenados em UTC
4. **Preços**: Armazenados como DECIMAL(10,2) para precisão monetária
5. **Senhas**: Sempre armazenadas como hash (nunca em texto plano)

## 🛠️ Manutenção

### Verificar Integridade:
```sql
PRAGMA integrity_check;
```

### Otimizar Banco:
```sql
VACUUM;
ANALYZE;
```

### Ver Tamanho do Banco:
```sql
SELECT page_count * page_size as size 
FROM pragma_page_count(), pragma_page_size();
```

## 📞 Suporte

Para dúvidas ou problemas com o banco de dados, consulte a documentação do Django ou SQLite.

---

**Última Atualização:** 2025-12-03  
**Versão do Schema:** 2.0  
**Sistema:** BOSS SHOPP E-commerce
