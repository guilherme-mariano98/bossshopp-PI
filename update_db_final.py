#!/usr/bin/env python3
import sqlite3

db_path = '../bossshopp_complete.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("Atualizando banco de dados...")

# Criar tabelas
tables = [
    """CREATE TABLE IF NOT EXISTS job_applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        phone VARCHAR(20) NOT NULL,
        cpf VARCHAR(14),
        birthdate DATE,
        position VARCHAR(100) NOT NULL,
        specialty VARCHAR(100),
        experience VARCHAR(50),
        linkedin VARCHAR(255),
        resume_filename VARCHAR(255),
        motivation TEXT,
        strengths TEXT,
        availability VARCHAR(50),
        status VARCHAR(50) DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""",
    
    """CREATE TABLE IF NOT EXISTS job_openings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(255) NOT NULL,
        department VARCHAR(100),
        location VARCHAR(255),
        type VARCHAR(50),
        level VARCHAR(50),
        vacancies INTEGER DEFAULT 1,
        description TEXT,
        is_active BOOLEAN DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""",
    
    """CREATE TABLE IF NOT EXISTS press_releases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(255) NOT NULL,
        slug VARCHAR(255) UNIQUE NOT NULL,
        excerpt TEXT,
        content TEXT NOT NULL,
        image_url VARCHAR(500),
        published_date DATE NOT NULL,
        is_published BOOLEAN DEFAULT 1,
        views INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""",
    
    """CREATE TABLE IF NOT EXISTS investor_reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(255) NOT NULL,
        report_type VARCHAR(50) NOT NULL,
        published_date DATE NOT NULL,
        fiscal_year INTEGER,
        fiscal_quarter INTEGER,
        downloads INTEGER DEFAULT 0,
        is_active BOOLEAN DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""",
    
    """CREATE TABLE IF NOT EXISTS corporate_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(255) NOT NULL,
        event_type VARCHAR(50) NOT NULL,
        event_date DATE NOT NULL,
        event_time TIME,
        description TEXT,
        is_online BOOLEAN DEFAULT 0,
        status VARCHAR(50) DEFAULT 'scheduled',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""",
    
    """CREATE TABLE IF NOT EXISTS financial_indicators (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        indicator_name VARCHAR(100) NOT NULL,
        indicator_value DECIMAL(15,2) NOT NULL,
        indicator_unit VARCHAR(20),
        comparison_value DECIMAL(15,2),
        comparison_period VARCHAR(50),
        fiscal_year INTEGER NOT NULL,
        fiscal_quarter INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )"""
]

for table_sql in tables:
    try:
        cursor.execute(table_sql)
        print(f"✓ Tabela criada")
    except Exception as e:
        print(f"✗ Erro: {e}")

# Inserir dados
print("\nInserindo dados...")

# Vagas
cursor.execute("SELECT COUNT(*) FROM job_openings")
if cursor.fetchone()[0] == 0:
    vagas = [
        ('Desenvolvedor Full Stack', 'Tecnologia', 'São Paulo, SP', 'Tempo Integral', 'Pleno/Sênior', 3, 'Desenvolvedor experiente em Node.js, React e bancos de dados', 1),
        ('Analista de Marketing Digital', 'Marketing', 'São Paulo, SP (Híbrido)', 'Tempo Integral', 'Pleno', 2, 'Profissional criativo para gerenciar campanhas digitais', 1),
        ('Entregador/Motorista', 'Logística', 'Várias Cidades', 'Tempo Integral', 'Operacional', 10, 'Responsável por entregas', 1),
        ('Estoquista', 'Logística', 'São Paulo, SP', 'Tempo Integral', 'Operacional', 4, 'Organização e controle de estoque', 1),
    ]
    cursor.executemany("""INSERT INTO job_openings (title, department, location, type, level, vacancies, description, is_active) 
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", vagas)
    print(f"✓ {len(vagas)} vagas inseridas")

# Notícias
cursor.execute("SELECT COUNT(*) FROM press_releases")
if cursor.fetchone()[0] == 0:
    noticias = [
        ('BOSS SHOPP Anuncia Expansão', 'expansao-novas-regioes', 'Abertura de novos centros', 'Conteúdo completo...', None, '2025-01-15', 1, 0),
        ('Marketplace Alcança 1.000 Vendedores', 'marketplace-1000', 'Crescimento do marketplace', 'Conteúdo completo...', None, '2025-01-10', 1, 0),
    ]
    cursor.executemany("""INSERT INTO press_releases (title, slug, excerpt, content, image_url, published_date, is_published, views) 
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", noticias)
    print(f"✓ {len(noticias)} notícias inseridas")

# Relatórios
cursor.execute("SELECT COUNT(*) FROM investor_reports")
if cursor.fetchone()[0] == 0:
    relatorios = [
        ('Relatório Anual 2024', 'annual', '2025-01-15', 2024, None, 0, 1),
        ('Resultados 4T24', 'quarterly', '2025-01-10', 2024, 4, 0, 1),
        ('Apresentação Institucional', 'presentation', '2025-01-05', 2025, None, 0, 1),
    ]
    cursor.executemany("""INSERT INTO investor_reports (title, report_type, published_date, fiscal_year, fiscal_quarter, downloads, is_active) 
                         VALUES (?, ?, ?, ?, ?, ?, ?)""", relatorios)
    print(f"✓ {len(relatorios)} relatórios inseridos")

# Indicadores financeiros
cursor.execute("SELECT COUNT(*) FROM financial_indicators")
if cursor.fetchone()[0] == 0:
    indicadores = [
        ('Receita Bruta', 250000000, 'BRL', 185000000, 'vs ano anterior', 2024, 4),
        ('EBITDA', 45000000, 'BRL', 31690000, 'vs ano anterior', 2024, 4),
        ('Margem EBITDA', 18, 'PERCENT', 15.5, 'vs ano anterior', 2024, 4),
        ('Novos Clientes', 150000, 'COUNT', 117000, 'vs trimestre anterior', 2024, 4),
    ]
    cursor.executemany("""INSERT INTO financial_indicators (indicator_name, indicator_value, indicator_unit, comparison_value, comparison_period, fiscal_year, fiscal_quarter) 
                         VALUES (?, ?, ?, ?, ?, ?, ?)""", indicadores)
    print(f"✓ {len(indicadores)} indicadores inseridos")

conn.commit()
conn.close()

print("\n✅ Banco de dados atualizado com sucesso!")
print("\nNovas tabelas criadas:")
print("  • job_applications - Candidaturas de emprego")
print("  • job_openings - Vagas abertas")
print("  • press_releases - Notícias de imprensa")
print("  • investor_reports - Relatórios para investidores")
print("  • corporate_events - Eventos corporativos")
print("  • financial_indicators - Indicadores financeiros")
