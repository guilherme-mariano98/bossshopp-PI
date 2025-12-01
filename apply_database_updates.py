#!/usr/bin/env python3
"""
Script para aplicar atualizações no banco de dados SQLite do BOSS SHOPP
"""

import sqlite3
import os
import sys
from datetime import datetime

def apply_updates(db_path='../bossshopp_complete.db', sql_file='update_database_schema.sql'):
    """Aplicar atualizações do schema no banco de dados"""
    
    # Verificar se o arquivo SQL existe
    if not os.path.exists(sql_file):
        print(f"❌ Arquivo SQL não encontrado: {sql_file}")
        return False
    
    # Verificar se o banco de dados existe
    if not os.path.exists(db_path):
        print(f"⚠️  Banco de dados não encontrado em {db_path}")
        print(f"   Criando novo banco de dados...")
    
    try:
        # Conectar ao banco de dados
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print(f"✅ Conectado ao banco de dados: {db_path}")
        
        # Ler o arquivo SQL
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        # Dividir em comandos individuais
        commands = sql_script.split(';')
        
        success_count = 0
        error_count = 0
        
        print(f"\n📝 Executando {len(commands)} comandos SQL...")
        print("=" * 60)
        
        for i, command in enumerate(commands, 1):
            command = command.strip()
            if not command or command.startswith('--'):
                continue
            
            try:
                cursor.execute(command)
                success_count += 1
                
                # Mostrar progresso para comandos importantes
                if 'CREATE TABLE' in command.upper():
                    table_name = command.split('CREATE TABLE')[1].split('(')[0].strip()
                    if 'IF NOT EXISTS' in command.upper():
                        table_name = table_name.replace('IF NOT EXISTS', '').strip()
                    print(f"  ✓ Tabela criada/verificada: {table_name}")
                elif 'INSERT INTO' in command.upper():
                    table_name = command.split('INSERT INTO')[1].split('(')[0].strip()
                    print(f"  ✓ Dados inseridos em: {table_name}")
                elif 'CREATE INDEX' in command.upper():
                    index_name = command.split('CREATE INDEX')[1].split('ON')[0].strip()
                    if 'IF NOT EXISTS' in command.upper():
                        index_name = index_name.replace('IF NOT EXISTS', '').strip()
                    print(f"  ✓ Índice criado: {index_name}")
                elif 'CREATE VIEW' in command.upper():
                    view_name = command.split('CREATE VIEW')[1].split('AS')[0].strip()
                    if 'IF NOT EXISTS' in command.upper():
                        view_name = view_name.replace('IF NOT EXISTS', '').strip()
                    print(f"  ✓ View criada: {view_name}")
                elif 'CREATE TRIGGER' in command.upper():
                    trigger_name = command.split('CREATE TRIGGER')[1].split('AFTER')[0].strip()
                    if 'IF NOT EXISTS' in command.upper():
                        trigger_name = trigger_name.replace('IF NOT EXISTS', '').strip()
                    print(f"  ✓ Trigger criado: {trigger_name}")
                    
            except sqlite3.Error as e:
                error_count += 1
                # Ignorar erros de "já existe" pois usamos IF NOT EXISTS
                if 'already exists' not in str(e).lower():
                    print(f"  ⚠️  Erro no comando {i}: {str(e)[:100]}")
        
        # Commit das mudanças
        conn.commit()
        
        print("=" * 60)
        print(f"\n✅ Atualização concluída!")
        print(f"   Comandos executados com sucesso: {success_count}")
        if error_count > 0:
            print(f"   Avisos/Erros: {error_count}")
        
        # Verificar tabelas criadas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = cursor.fetchall()
        
        print(f"\n📊 Tabelas no banco de dados ({len(tables)}):")
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
            count = cursor.fetchone()[0]
            print(f"   • {table[0]}: {count} registros")
        
        # Fechar conexão
        cursor.close()
        conn.close()
        
        print(f"\n🎉 Banco de dados atualizado com sucesso!")
        print(f"   Localização: {os.path.abspath(db_path)}")
        
        return True
        
    except sqlite3.Error as e:
        print(f"\n❌ Erro ao atualizar banco de dados: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        return False

def backup_database(db_path):
    """Criar backup do banco de dados antes de atualizar"""
    if not os.path.exists(db_path):
        return None
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = f"{db_path}.backup_{timestamp}"
    
    try:
        import shutil
        shutil.copy2(db_path, backup_path)
        print(f"💾 Backup criado: {backup_path}")
        return backup_path
    except Exception as e:
        print(f"⚠️  Não foi possível criar backup: {e}")
        return None

if __name__ == "__main__":
    print("=" * 60)
    print("  BOSS SHOPP - Atualização do Banco de Dados")
    print("=" * 60)
    print()
    
    # Caminhos padrão
    db_path = '../bossshopp_complete.db'
    sql_file = 'update_database_schema.sql'
    
    # Verificar argumentos da linha de comando
    if len(sys.argv) > 1:
        db_path = sys.argv[1]
    if len(sys.argv) > 2:
        sql_file = sys.argv[2]
    
    # Criar backup antes de atualizar
    if os.path.exists(db_path):
        response = input("Deseja criar um backup antes de atualizar? (S/n): ")
        if response.lower() != 'n':
            backup_database(db_path)
            print()
    
    # Aplicar atualizações
    success = apply_updates(db_path, sql_file)
    
    if success:
        print("\n✨ Todas as atualizações foram aplicadas com sucesso!")
        print("\n📝 Novas funcionalidades disponíveis:")
        print("   • Sistema de candidaturas de emprego")
        print("   • Gerenciamento de vagas")
        print("   • Notícias de imprensa")
        print("   • Relatórios para investidores")
        print("   • Eventos corporativos")
        print("   • Indicadores financeiros")
        print("   • Newsletter/Mailing list")
        sys.exit(0)
    else:
        print("\n❌ Falha ao aplicar atualizações.")
        sys.exit(1)
