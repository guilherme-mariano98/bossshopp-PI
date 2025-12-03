"""
Script para adicionar colunas faltantes no banco de dados
"""

import sqlite3
import os

DB_PATH = 'db.sqlite3'

def add_column_if_not_exists(cursor, table, column, definition):
    """Adiciona coluna se ela não existir"""
    cursor.execute(f"PRAGMA table_info({table})")
    columns = [row[1] for row in cursor.fetchall()]
    
    if column not in columns:
        try:
            cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")
            print(f"✓ Coluna {column} adicionada em {table}")
            return True
        except sqlite3.OperationalError as e:
            print(f"✗ Erro ao adicionar {column}: {e}")
            return False
    else:
        print(f"  Coluna {column} já existe em {table}")
        return False

def create_table_if_not_exists(cursor, table_name, create_sql):
    """Cria tabela se ela não existir"""
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    if not cursor.fetchone():
        try:
            cursor.execute(create_sql)
            print(f"✓ Tabela {table_name} criada")
            return True
        except sqlite3.OperationalError as e:
            print(f"✗ Erro ao criar {table_name}: {e}")
            return False
    else:
        print(f"  Tabela {table_name} já existe")
        return False

def main():
    if not os.path.exists(DB_PATH):
        print(f"❌ Banco de dados não encontrado: {DB_PATH}")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("🔧 Corrigindo estrutura do banco de dados...\n")
    
    # Adicionar colunas faltantes em api_product
    print("📦 Atualizando tabela api_product:")
    add_column_if_not_exists(cursor, 'api_product', 'brand', 'varchar(100) NULL')
    add_column_if_not_exists(cursor, 'api_product', 'is_active', 'INTEGER NOT NULL DEFAULT 1')
    add_column_if_not_exists(cursor, 'api_product', 'featured', 'INTEGER NOT NULL DEFAULT 0')
    add_column_if_not_exists(cursor, 'api_product', 'discount_percentage', 'DECIMAL NOT NULL DEFAULT 0')
    
    # Criar tabela ProductVariation
    print("\n🎨 Criando tabela api_productvariation:")
    create_table_if_not_exists(cursor, 'api_productvariation', '''
        CREATE TABLE api_productvariation (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            variation_type varchar(20) NOT NULL,
            variation_value varchar(100) NOT NULL,
            price_adjustment DECIMAL NOT NULL DEFAULT 0,
            stock_quantity INTEGER NOT NULL DEFAULT 0,
            sku varchar(100) NULL UNIQUE,
            product_id INTEGER NOT NULL,
            FOREIGN KEY (product_id) REFERENCES api_product(id),
            UNIQUE (product_id, variation_type, variation_value)
        )
    ''')
    
    # Criar tabela ProductImage
    print("\n🖼️ Criando tabela api_productimage:")
    create_table_if_not_exists(cursor, 'api_productimage', '''
        CREATE TABLE api_productimage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image varchar(100) NOT NULL,
            alt_text varchar(200) NOT NULL DEFAULT '',
            is_primary INTEGER NOT NULL DEFAULT 0,
            "order" INTEGER NOT NULL DEFAULT 0,
            product_id INTEGER NOT NULL,
            FOREIGN KEY (product_id) REFERENCES api_product(id)
        )
    ''')
    
    # Criar tabela ProductReview
    print("\n⭐ Criando tabela api_productreview:")
    create_table_if_not_exists(cursor, 'api_productreview', '''
        CREATE TABLE api_productreview (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rating INTEGER NOT NULL,
            title varchar(200) NOT NULL,
            comment TEXT NOT NULL,
            verified_purchase INTEGER NOT NULL DEFAULT 0,
            helpful_count INTEGER NOT NULL DEFAULT 0,
            created_at datetime NOT NULL,
            updated_at datetime NOT NULL,
            product_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (product_id) REFERENCES api_product(id),
            FOREIGN KEY (user_id) REFERENCES api_user(id),
            UNIQUE (product_id, user_id)
        )
    ''')
    
    conn.commit()
    conn.close()
    
    print("\n✅ Banco de dados atualizado com sucesso!")
    print("\nPróximos passos:")
    print("1. Reiniciar o servidor Django")
    print("2. Testar os endpoints da API")
    print("3. Popular dados de exemplo")

if __name__ == "__main__":
    main()
