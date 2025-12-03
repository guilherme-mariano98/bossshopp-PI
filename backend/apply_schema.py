#!/usr/bin/env python
"""
Script para aplicar o schema SQLite no banco de dados
BOSS SHOPP E-commerce System
"""

import sqlite3
import os
from pathlib import Path

def apply_schema():
    """Aplica o schema SQL no banco de dados SQLite"""
    
    # Caminho do banco de dados
    db_path = Path(__file__).parent / 'db.sqlite3'
    schema_path = Path(__file__).parent / 'database_schema_sqlite.sql'
    
    print("=" * 60)
    print("BOSS SHOPP - Aplicação do Schema SQLite")
    print("=" * 60)
    print()
    
    # Verificar se o arquivo de schema existe
    if not schema_path.exists():
        print(f"❌ Erro: Arquivo de schema não encontrado: {schema_path}")
        return False
    
    print(f"📁 Banco de dados: {db_path}")
    print(f"📄 Schema: {schema_path}")
    print()
    
    try:
        # Conectar ao banco de dados
        print("🔌 Conectando ao banco de dados...")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Ler o arquivo SQL
        print("📖 Lendo arquivo de schema...")
        with open(schema_path, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        # Executar o script SQL
        print("⚙️  Executando script SQL...")
        cursor.executescript(sql_script)
        
        # Commit das mudanças
        conn.commit()
        print("✅ Schema aplicado com sucesso!")
        print()
        
        # Verificar tabelas criadas
        print("📊 Verificando tabelas criadas:")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = cursor.fetchall()
        
        for i, (table,) in enumerate(tables, 1):
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"   {i:2d}. {table:30s} - {count:4d} registros")
        
        print()
        print("=" * 60)
        print("✨ Processo concluído com sucesso!")
        print("=" * 60)
        
        # Fechar conexão
        conn.close()
        return True
        
    except sqlite3.Error as e:
        print(f"❌ Erro ao aplicar schema: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def backup_database():
    """Cria um backup do banco de dados antes de aplicar o schema"""
    
    db_path = Path(__file__).parent / 'db.sqlite3'
    
    if not db_path.exists():
        print("ℹ️  Banco de dados não existe ainda. Nenhum backup necessário.")
        return True
    
    from datetime import datetime
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = Path(__file__).parent / f'db_backup_{timestamp}.sqlite3'
    
    try:
        import shutil
        print(f"💾 Criando backup: {backup_path.name}")
        shutil.copy2(db_path, backup_path)
        print("✅ Backup criado com sucesso!")
        print()
        return True
    except Exception as e:
        print(f"⚠️  Aviso: Não foi possível criar backup: {e}")
        print()
        return False

def show_statistics():
    """Mostra estatísticas do banco de dados"""
    
    db_path = Path(__file__).parent / 'db.sqlite3'
    
    if not db_path.exists():
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print()
        print("=" * 60)
        print("📈 ESTATÍSTICAS DO BANCO DE DADOS")
        print("=" * 60)
        print()
        
        # Categorias
        cursor.execute("SELECT COUNT(*) FROM api_category")
        cat_count = cursor.fetchone()[0]
        print(f"📦 Categorias: {cat_count}")
        
        # Produtos
        cursor.execute("SELECT COUNT(*) FROM api_product")
        prod_count = cursor.fetchone()[0]
        print(f"🛍️  Produtos: {prod_count}")
        
        # Usuários
        cursor.execute("SELECT COUNT(*) FROM api_user")
        user_count = cursor.fetchone()[0]
        print(f"👥 Usuários: {user_count}")
        
        # Pedidos
        cursor.execute("SELECT COUNT(*) FROM api_order")
        order_count = cursor.fetchone()[0]
        print(f"📋 Pedidos: {order_count}")
        
        print()
        
        # Top 5 categorias com mais produtos
        print("🏆 Top 5 Categorias com Mais Produtos:")
        cursor.execute("""
            SELECT c.name, COUNT(p.id) as total
            FROM api_category c
            LEFT JOIN api_product p ON c.id = p.category_id
            GROUP BY c.id, c.name
            ORDER BY total DESC
            LIMIT 5
        """)
        
        for i, (name, total) in enumerate(cursor.fetchall(), 1):
            print(f"   {i}. {name:20s} - {total:3d} produtos")
        
        print()
        print("=" * 60)
        
        conn.close()
        
    except Exception as e:
        print(f"⚠️  Erro ao obter estatísticas: {e}")

if __name__ == '__main__':
    print()
    
    # Criar backup
    backup_database()
    
    # Aplicar schema
    success = apply_schema()
    
    if success:
        # Mostrar estatísticas
        show_statistics()
    
    print()
    input("Pressione ENTER para sair...")
