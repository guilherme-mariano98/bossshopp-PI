-- ============================================
-- BOSS SHOPP - SQLite Database Schema
-- Sistema de E-commerce Completo
-- Versão: 2.0
-- Data: 2025-12-03
-- ============================================

-- Este schema reflete exatamente os modelos Django do sistema
-- Compatível com SQLite 3.x

-- ============================================
-- 1. TABELAS PRINCIPAIS DO SISTEMA
-- ============================================

-- Tabela de Usuários (Custom User Model)
CREATE TABLE IF NOT EXISTS api_user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    password VARCHAR(128) NOT NULL,
    last_login DATETIME NULL,
    is_superuser BOOLEAN NOT NULL DEFAULT 0,
    username VARCHAR(150) NOT NULL UNIQUE,
    first_name VARCHAR(150) NOT NULL DEFAULT '',
    last_name VARCHAR(150) NOT NULL DEFAULT '',
    email VARCHAR(254) NOT NULL UNIQUE,
    is_staff BOOLEAN NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    date_joined DATETIME NOT NULL,
    created_at DATETIME NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_user_email ON api_user(email);
CREATE INDEX IF NOT EXISTS idx_user_username ON api_user(username);
CREATE INDEX IF NOT EXISTS idx_user_is_active ON api_user(is_active);
CREATE INDEX IF NOT EXISTS idx_user_date_joined ON api_user(date_joined);

-- Tabela de Categorias
CREATE TABLE IF NOT EXISTS api_category (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    created_at DATETIME NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_category_slug ON api_category(slug);
CREATE INDEX IF NOT EXISTS idx_category_name ON api_category(name);
CREATE INDEX IF NOT EXISTS idx_category_created_at ON api_category(created_at);

-- Tabela de Produtos
CREATE TABLE IF NOT EXISTS api_product (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    category_id INTEGER NOT NULL,
    image VARCHAR(100) NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    FOREIGN KEY (category_id) REFERENCES api_category(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_product_category ON api_product(category_id);
CREATE INDEX IF NOT EXISTS idx_product_name ON api_product(name);
CREATE INDEX IF NOT EXISTS idx_product_price ON api_product(price);
CREATE INDEX IF NOT EXISTS idx_product_created_at ON api_product(created_at);
CREATE INDEX IF NOT EXISTS idx_product_category_price ON api_product(category_id, price);

-- Tabela de Pedidos
CREATE TABLE IF NOT EXISTS api_order (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    shipping_address TEXT NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES api_user(id) ON DELETE CASCADE,
    CHECK (status IN ('pending', 'processing', 'shipped', 'delivered', 'cancelled'))
);

CREATE INDEX IF NOT EXISTS idx_order_user ON api_order(user_id);
CREATE INDEX IF NOT EXISTS idx_order_status ON api_order(status);
CREATE INDEX IF NOT EXISTS idx_order_created_at ON api_order(created_at);
CREATE INDEX IF NOT EXISTS idx_order_user_status ON api_order(user_id, status);

-- Tabela de Itens do Pedido
CREATE TABLE IF NOT EXISTS api_orderitem (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES api_order(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES api_product(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_orderitem_order ON api_orderitem(order_id);
CREATE INDEX IF NOT EXISTS idx_orderitem_product ON api_orderitem(product_id);

-- ============================================
-- 2. TABELAS DE AUTENTICAÇÃO E PERMISSÕES
-- ============================================

-- Tabela de Tokens de Autenticação
CREATE TABLE IF NOT EXISTS authtoken_token (
    key VARCHAR(40) NOT NULL PRIMARY KEY,
    created DATETIME NOT NULL,
    user_id INTEGER NOT NULL UNIQUE,
    FOREIGN KEY (user_id) REFERENCES api_user(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_token_created ON authtoken_token(created);

-- Tabela de Grupos
CREATE TABLE IF NOT EXISTS auth_group (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(150) NOT NULL UNIQUE
);

-- Tabela de Permissões
CREATE TABLE IF NOT EXISTS auth_permission (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    content_type_id INTEGER NOT NULL,
    codename VARCHAR(100) NOT NULL,
    UNIQUE(content_type_id, codename)
);

-- Tabela de Relacionamento Usuário-Grupo
CREATE TABLE IF NOT EXISTS api_user_groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    group_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES api_user(id) ON DELETE CASCADE,
    FOREIGN KEY (group_id) REFERENCES auth_group(id) ON DELETE CASCADE,
    UNIQUE(user_id, group_id)
);

-- Tabela de Relacionamento Usuário-Permissão
CREATE TABLE IF NOT EXISTS api_user_user_permissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    permission_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES api_user(id) ON DELETE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES auth_permission(id) ON DELETE CASCADE,
    UNIQUE(user_id, permission_id)
);

-- Tabela de Relacionamento Grupo-Permissão
CREATE TABLE IF NOT EXISTS auth_group_permissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_id INTEGER NOT NULL,
    permission_id INTEGER NOT NULL,
    FOREIGN KEY (group_id) REFERENCES auth_group(id) ON DELETE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES auth_permission(id) ON DELETE CASCADE,
    UNIQUE(group_id, permission_id)
);

-- ============================================
-- 3. TABELAS DO DJANGO
-- ============================================

-- Tabela de Content Types
CREATE TABLE IF NOT EXISTS django_content_type (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    app_label VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    UNIQUE(app_label, model)
);

-- Tabela de Migrações
CREATE TABLE IF NOT EXISTS django_migrations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    app VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    applied DATETIME NOT NULL
);

-- Tabela de Sessões
CREATE TABLE IF NOT EXISTS django_session (
    session_key VARCHAR(40) NOT NULL PRIMARY KEY,
    session_data TEXT NOT NULL,
    expire_date DATETIME NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_session_expire_date ON django_session(expire_date);

-- Tabela de Admin Log
CREATE TABLE IF NOT EXISTS django_admin_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    action_time DATETIME NOT NULL,
    object_id TEXT,
    object_repr VARCHAR(200) NOT NULL,
    action_flag INTEGER NOT NULL,
    change_message TEXT NOT NULL,
    content_type_id INTEGER,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES api_user(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_admin_log_user ON django_admin_log(user_id);
CREATE INDEX IF NOT EXISTS idx_admin_log_content_type ON django_admin_log(content_type_id);

-- ============================================
-- 4. DADOS INICIAIS - CATEGORIAS
-- ============================================

INSERT OR IGNORE INTO api_category (id, name, slug, description, created_at) VALUES
(1, 'Moda', 'moda', 'Roupas, calçados e acessórios de moda para todos os estilos', datetime('now')),
(2, 'Eletrônicos', 'eletronicos', 'Smartphones, notebooks, TVs e dispositivos eletrônicos', datetime('now')),
(3, 'Casa', 'casa', 'Móveis, decoração e utensílios para o lar', datetime('now')),
(4, 'Games', 'games', 'Consoles, jogos e acessórios para gamers', datetime('now')),
(5, 'Esportes', 'esportes', 'Equipamentos e acessórios esportivos', datetime('now')),
(6, 'Infantil', 'infantil', 'Produtos para bebês e crianças', datetime('now')),
(7, 'Beleza', 'beleza', 'Cosméticos, perfumes e produtos de beleza', datetime('now')),
(8, 'Livros', 'livros', 'Livros, e-books e materiais de leitura', datetime('now')),
(9, 'Automotivo', 'automotivo', 'Acessórios e peças para veículos', datetime('now')),
(10, 'Pet Shop', 'pet-shop', 'Produtos para animais de estimação', datetime('now')),
(11, 'Alimentos', 'alimentos', 'Alimentos, bebidas e produtos alimentícios', datetime('now')),
(12, 'Ferramentas', 'ferramentas', 'Ferramentas e equipamentos profissionais', datetime('now')),
(13, 'Música', 'musica', 'Instrumentos musicais e equipamentos de áudio', datetime('now')),
(14, 'Papelaria', 'papelaria', 'Material escolar e de escritório', datetime('now')),
(15, 'Saúde', 'saude', 'Produtos de saúde e bem-estar', datetime('now')),
(16, 'Brinquedos', 'brinquedos', 'Brinquedos e jogos educativos', datetime('now'));

-- ============================================
-- 5. DADOS INICIAIS - PRODUTOS
-- ============================================

INSERT OR IGNORE INTO api_product (name, description, price, category_id, created_at, updated_at) VALUES
-- Moda (category_id = 1)
('Camiseta Básica', 'Camiseta de algodão 100% com modelagem confortável. Disponível em várias cores.', 39.90, 1, datetime('now'), datetime('now')),
('Calça Jeans', 'Calça jeans masculina com corte moderno e tecido de alta qualidade.', 89.90, 1, datetime('now'), datetime('now')),
('Tênis Esportivo', 'Tênis para corrida com tecnologia de amortecimento e design ergonômico.', 169.90, 1, datetime('now'), datetime('now')),
('Boné Estiloso', 'Boné com proteção UV e ajuste regulável. Perfeito para o dia a dia.', 34.90, 1, datetime('now'), datetime('now')),
('Jaqueta Jeans', 'Jaqueta jeans clássica com bolsos e acabamento premium.', 129.90, 1, datetime('now'), datetime('now')),
('Vestido Floral', 'Vestido feminino com estampa floral e tecido leve para o verão.', 79.90, 1, datetime('now'), datetime('now')),

-- Eletrônicos (category_id = 2)
('Smartphone Premium', 'Smartphone com câmera de 108MP, 256GB de armazenamento e 5G.', 1760.00, 2, datetime('now'), datetime('now')),
('Notebook Ultrafino', 'Notebook com processador i7, 16GB RAM, SSD 512GB e tela Full HD.', 2975.00, 2, datetime('now'), datetime('now')),
('Fone Bluetooth Sem Fio', 'Fone com cancelamento de ruído ativo e bateria de 30 horas.', 224.90, 2, datetime('now'), datetime('now')),
('Smart TV 55"', 'TV 4K com HDR, sistema operacional Android e controle por voz.', 1750.00, 2, datetime('now'), datetime('now')),
('Tablet 10 polegadas', 'Tablet com tela Full HD, 128GB e caneta stylus incluída.', 899.00, 2, datetime('now'), datetime('now')),
('Smartwatch Fitness', 'Relógio inteligente com monitor cardíaco e GPS integrado.', 349.90, 2, datetime('now'), datetime('now')),

-- Casa (category_id = 3)
('Sofá Confortável', 'Sofá de 3 lugares com estrutura de madeira e estofado premium.', 1020.00, 3, datetime('now'), datetime('now')),
('Cama Queen Size', 'Cama com headboard estofado e estrutura reforçada.', 899.90, 3, datetime('now'), datetime('now')),
('Jogo de Talheres', 'Talheres em aço inoxidável com 24 peças e estojo elegante.', 159.90, 3, datetime('now'), datetime('now')),
('Kit de Lâmpadas LED', 'Lâmpadas LED econômicas 9W, luz branca, pacote com 10 unidades.', 97.40, 3, datetime('now'), datetime('now')),
('Mesa de Jantar', 'Mesa de jantar para 6 pessoas em madeira maciça.', 749.90, 3, datetime('now'), datetime('now')),
('Aspirador de Pó', 'Aspirador de pó potente com filtro HEPA e acessórios.', 299.90, 3, datetime('now'), datetime('now')),

-- Games (category_id = 4)
('Console de Videogame', 'Console de última geração com 1TB de armazenamento e controle sem fio.', 2250.00, 4, datetime('now'), datetime('now')),
('Jogo de Tabuleiro', 'Jogo estratégico para toda família com 2-6 jogadores.', 89.90, 4, datetime('now'), datetime('now')),
('Fone Gamer', 'Fone com som surround 7.1, microfone removível e iluminação RGB.', 299.90, 4, datetime('now'), datetime('now')),
('Teclado Mecânico', 'Teclado RGB com switches blue, anti-ghosting e repouso para pulso.', 319.90, 4, datetime('now'), datetime('now')),
('Mouse Gamer', 'Mouse com sensor óptico de 16000 DPI e 8 botões programáveis.', 149.90, 4, datetime('now'), datetime('now')),
('Cadeira Gamer', 'Cadeira ergonômica com apoio lombar e ajuste de altura.', 899.90, 4, datetime('now'), datetime('now')),

-- Esportes (category_id = 5)
('Conjunto de Halteres', 'Halteres ajustáveis de 5 a 25kg com suporte incluso.', 254.90, 5, datetime('now'), datetime('now')),
('Tênis para Corrida', 'Tênis com amortecimento especial e solado antiderrapante.', 199.90, 5, datetime('now'), datetime('now')),
('Bola de Futebol', 'Bola oficial com certificação FIFA e costura reforçada.', 74.90, 5, datetime('now'), datetime('now')),
('Bicicleta Mountain Bike', 'Bicicleta para trilhas com 21 marchas e suspensão dianteira.', 1299.90, 5, datetime('now'), datetime('now')),
('Esteira Elétrica', 'Esteira dobrável com velocidade até 12km/h e monitor LCD.', 1499.90, 5, datetime('now'), datetime('now')),
('Kit de Yoga', 'Kit completo com tapete, blocos e cinta de alongamento.', 89.90, 5, datetime('now'), datetime('now')),

-- Infantil (category_id = 6)
('Camiseta Infantil', 'Camiseta 100% algodão com estampas divertidas.', 33.90, 6, datetime('now'), datetime('now')),
('Meias Coloridas', 'Pacote com 5 pares de meias infantis coloridas.', 19.90, 6, datetime('now'), datetime('now')),
('Sapatilha Infantil', 'Sapatilha confortável para festas e ocasiões especiais.', 47.90, 6, datetime('now'), datetime('now')),
('Carrinho de Controle Remoto', 'Carrinho com controle remoto, luzes e sons.', 89.90, 6, datetime('now'), datetime('now')),
('Boneca Interativa', 'Boneca que fala e canta com acessórios inclusos.', 129.90, 6, datetime('now'), datetime('now')),
('Quebra-Cabeça Educativo', 'Quebra-cabeça de 100 peças com tema educativo.', 34.90, 6, datetime('now'), datetime('now')),

-- Beleza (category_id = 7)
('Kit de Maquiagem', 'Kit completo com sombras, batons e pincéis profissionais.', 149.90, 7, datetime('now'), datetime('now')),
('Perfume Importado', 'Perfume masculino com fragrância amadeirada e duradoura.', 189.90, 7, datetime('now'), datetime('now')),
('Secador de Cabelo', 'Secador profissional com 3 temperaturas e difusor.', 129.90, 7, datetime('now'), datetime('now')),

-- Livros (category_id = 8)
('Box Harry Potter', 'Coleção completa com 7 livros da saga Harry Potter.', 199.90, 8, datetime('now'), datetime('now')),
('Livro de Receitas', 'Livro com 500 receitas práticas e deliciosas.', 49.90, 8, datetime('now'), datetime('now')),
('Romance Bestseller', 'Romance contemporâneo mais vendido do ano.', 34.90, 8, datetime('now'), datetime('now')),

-- Automotivo (category_id = 9)
('Kit de Ferramentas Automotivas', 'Kit com 100 peças para manutenção veicular.', 249.90, 9, datetime('now'), datetime('now')),
('Capa para Carro', 'Capa impermeável com proteção UV para veículos.', 89.90, 9, datetime('now'), datetime('now')),
('Aspirador Automotivo', 'Aspirador portátil 12V para limpeza interna.', 79.90, 9, datetime('now'), datetime('now')),

-- Pet Shop (category_id = 10)
('Ração Premium para Cães', 'Ração super premium 15kg para cães adultos.', 159.90, 10, datetime('now'), datetime('now')),
('Arranhador para Gatos', 'Arranhador de sisal com plataformas e brinquedos.', 129.90, 10, datetime('now'), datetime('now')),
('Coleira com GPS', 'Coleira inteligente com rastreamento GPS em tempo real.', 199.90, 10, datetime('now'), datetime('now')),

-- Alimentos (category_id = 11)
('Cesta de Café da Manhã', 'Cesta gourmet com pães, geleias e cafés especiais.', 89.90, 11, datetime('now'), datetime('now')),
('Kit de Temperos', 'Kit com 20 temperos naturais em potes de vidro.', 69.90, 11, datetime('now'), datetime('now')),
('Chocolate Artesanal', 'Caixa com 12 bombons artesanais sortidos.', 39.90, 11, datetime('now'), datetime('now')),

-- Ferramentas (category_id = 12)
('Furadeira de Impacto', 'Furadeira profissional 800W com maleta e brocas.', 299.90, 12, datetime('now'), datetime('now')),
('Jogo de Chaves', 'Jogo com 40 chaves combinadas em aço cromo vanádio.', 149.90, 12, datetime('now'), datetime('now')),
('Serra Tico-Tico', 'Serra elétrica 500W com guia laser e 5 lâminas.', 189.90, 12, datetime('now'), datetime('now')),

-- Música (category_id = 13)
('Violão Acústico', 'Violão folk com cordas de aço e capa acolchoada.', 349.90, 13, datetime('now'), datetime('now')),
('Teclado Musical', 'Teclado com 61 teclas, 200 timbres e suporte.', 599.90, 13, datetime('now'), datetime('now')),
('Caixa de Som Bluetooth', 'Caixa portátil 50W com bateria de 12 horas.', 199.90, 13, datetime('now'), datetime('now')),

-- Papelaria (category_id = 14)
('Kit Escolar Completo', 'Kit com cadernos, canetas, lápis e estojo.', 79.90, 14, datetime('now'), datetime('now')),
('Agenda 2025', 'Agenda executiva com capa de couro sintético.', 49.90, 14, datetime('now'), datetime('now')),
('Calculadora Científica', 'Calculadora com 240 funções para estudantes.', 59.90, 14, datetime('now'), datetime('now')),

-- Saúde (category_id = 15)
('Termômetro Digital', 'Termômetro infravermelho sem contato.', 89.90, 15, datetime('now'), datetime('now')),
('Medidor de Pressão', 'Medidor digital de pressão arterial de pulso.', 119.90, 15, datetime('now'), datetime('now')),
('Kit de Primeiros Socorros', 'Kit completo com 100 itens para emergências.', 69.90, 15, datetime('now'), datetime('now')),

-- Brinquedos (category_id = 16)
('Lego Criativo', 'Set com 500 peças para construções criativas.', 149.90, 16, datetime('now'), datetime('now')),
('Boneco de Ação', 'Boneco articulado de super-herói com acessórios.', 79.90, 16, datetime('now'), datetime('now')),
('Jogo de Memória', 'Jogo educativo de memória com 40 cartas.', 29.90, 16, datetime('now'), datetime('now'));

-- ============================================
-- 6. VIEWS ÚTEIS PARA RELATÓRIOS
-- ============================================

-- View de Produtos com Categoria
CREATE VIEW IF NOT EXISTS vw_products_with_category AS
SELECT 
    p.id,
    p.name AS product_name,
    p.description,
    p.price,
    c.name AS category_name,
    c.slug AS category_slug,
    p.image,
    p.created_at,
    p.updated_at
FROM api_product p
INNER JOIN api_category c ON p.category_id = c.id;

-- View de Pedidos Completos
CREATE VIEW IF NOT EXISTS vw_orders_complete AS
SELECT 
    o.id AS order_id,
    u.username,
    u.email,
    o.total_amount,
    o.status,
    o.payment_method,
    o.created_at AS order_date,
    COUNT(oi.id) AS total_items
FROM api_order o
INNER JOIN api_user u ON o.user_id = u.id
LEFT JOIN api_orderitem oi ON o.id = oi.order_id
GROUP BY o.id, u.username, u.email, o.total_amount, o.status, o.payment_method, o.created_at;

-- View de Estatísticas de Vendas por Categoria
CREATE VIEW IF NOT EXISTS vw_sales_by_category AS
SELECT 
    c.name AS category_name,
    COUNT(DISTINCT oi.id) AS items_sold,
    SUM(oi.quantity) AS total_quantity,
    SUM(oi.price * oi.quantity) AS total_revenue
FROM api_category c
INNER JOIN api_product p ON c.id = p.category_id
INNER JOIN api_orderitem oi ON p.id = oi.product_id
GROUP BY c.id, c.name;

-- View de Produtos Mais Vendidos
CREATE VIEW IF NOT EXISTS vw_top_products AS
SELECT 
    p.id,
    p.name,
    p.price,
    c.name AS category_name,
    COUNT(oi.id) AS times_sold,
    SUM(oi.quantity) AS total_quantity_sold,
    SUM(oi.price * oi.quantity) AS total_revenue
FROM api_product p
INNER JOIN api_category c ON p.category_id = c.id
LEFT JOIN api_orderitem oi ON p.id = oi.product_id
GROUP BY p.id, p.name, p.price, c.name
ORDER BY total_quantity_sold DESC;

-- View de Usuários Ativos
CREATE VIEW IF NOT EXISTS vw_active_users AS
SELECT 
    u.id,
    u.username,
    u.email,
    u.first_name,
    u.last_name,
    u.date_joined,
    COUNT(o.id) AS total_orders,
    COALESCE(SUM(o.total_amount), 0) AS total_spent
FROM api_user u
LEFT JOIN api_order o ON u.id = o.user_id
WHERE u.is_active = 1
GROUP BY u.id, u.username, u.email, u.first_name, u.last_name, u.date_joined;

-- ============================================
-- 7. TRIGGERS
-- ============================================

-- Trigger para atualizar updated_at automaticamente em produtos
CREATE TRIGGER IF NOT EXISTS trg_product_update_timestamp
AFTER UPDATE ON api_product
FOR EACH ROW
BEGIN
    UPDATE api_product SET updated_at = datetime('now') WHERE id = NEW.id;
END;

-- Trigger para atualizar updated_at automaticamente em pedidos
CREATE TRIGGER IF NOT EXISTS trg_order_update_timestamp
AFTER UPDATE ON api_order
FOR EACH ROW
BEGIN
    UPDATE api_order SET updated_at = datetime('now') WHERE id = NEW.id;
END;

-- ============================================
-- 8. CONSULTAS ÚTEIS
-- ============================================

-- Verificar todas as tabelas criadas
SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;

-- Verificar todas as views criadas
SELECT name FROM sqlite_master WHERE type='view' ORDER BY name;

-- Verificar todos os índices criados
SELECT name FROM sqlite_master WHERE type='index' ORDER BY name;

-- Contar registros por tabela
SELECT 
    'api_user' as tabela, COUNT(*) as registros FROM api_user
UNION ALL SELECT 'api_category', COUNT(*) FROM api_category
UNION ALL SELECT 'api_product', COUNT(*) FROM api_product
UNION ALL SELECT 'api_order', COUNT(*) FROM api_order
UNION ALL SELECT 'api_orderitem', COUNT(*) FROM api_orderitem;

-- ============================================
-- FIM DO SCHEMA SQLite
-- ============================================

-- Mensagem de conclusão
SELECT 'Database schema SQLite criado com sucesso!' AS Status,
       (SELECT COUNT(*) FROM api_category) AS Total_Categorias,
       (SELECT COUNT(*) FROM api_product) AS Total_Produtos;
