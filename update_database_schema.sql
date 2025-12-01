-- =====================================================
-- BOSS SHOPP - Atualização do Schema do Banco de Dados
-- Data: 2025-01-01
-- Descrição: Adiciona tabelas para novas funcionalidades
-- =====================================================

-- Tabela para candidaturas de emprego
CREATE TABLE IF NOT EXISTS job_applications (
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
    resume_path VARCHAR(500),
    cnh_filename VARCHAR(255),
    cnh_path VARCHAR(500),
    cnh_category VARCHAR(5),
    has_vehicle BOOLEAN DEFAULT 0,
    motivation TEXT,
    strengths TEXT,
    availability VARCHAR(50),
    salary_expectation VARCHAR(50),
    flexible_hours BOOLEAN,
    additional_info TEXT,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para job_applications
CREATE INDEX IF NOT EXISTS idx_job_applications_email ON job_applications(email);
CREATE INDEX IF NOT EXISTS idx_job_applications_position ON job_applications(position);
CREATE INDEX IF NOT EXISTS idx_job_applications_status ON job_applications(status);
CREATE INDEX IF NOT EXISTS idx_job_applications_created ON job_applications(created_at);

-- Tabela para vagas de emprego
CREATE TABLE IF NOT EXISTS job_openings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    department VARCHAR(100),
    location VARCHAR(255),
    type VARCHAR(50),
    level VARCHAR(50),
    vacancies INTEGER DEFAULT 1,
    description TEXT,
    requirements TEXT,
    benefits TEXT,
    salary_range VARCHAR(100),
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Inserir vagas atuais
INSERT INTO job_openings (title, department, location, type, level, vacancies, description, is_active) VALUES
('Desenvolvedor Full Stack', 'Tecnologia', 'São Paulo, SP', 'Tempo Integral', 'Pleno/Sênior', 3, 'Desenvolvedor experiente em Node.js, React e bancos de dados', 1),
('Analista de Marketing Digital', 'Marketing', 'São Paulo, SP (Híbrido)', 'Tempo Integral', 'Pleno', 2, 'Profissional criativo para gerenciar campanhas digitais', 1),
('Coordenador de Logística', 'Logística', 'Rio de Janeiro, RJ', 'Tempo Integral', 'Sênior', 1, 'Coordenação de operações de distribuição', 1),
('Atendente de Customer Success', 'Atendimento', 'Remoto', 'Tempo Integral', 'Júnior/Pleno', 5, 'Profissional dedicado ao sucesso do cliente', 1),
('Entregador/Motorista', 'Logística', 'Várias Cidades', 'Tempo Integral', 'Operacional', 10, 'Responsável por entregas. CNH categoria B necessária', 1),
('Estoquista', 'Logística', 'São Paulo, SP', 'Tempo Integral', 'Operacional', 4, 'Organização e controle de estoque', 1),
('Designer Gráfico', 'Marketing', 'São Paulo, SP (Híbrido)', 'Tempo Integral', 'Pleno', 2, 'Criação de peças gráficas e materiais promocionais', 1),
('Analista Financeiro', 'Financeiro', 'São Paulo, SP', 'Tempo Integral', 'Pleno/Sênior', 1, 'Análise de demonstrativos financeiros', 1),
('Analista de Recursos Humanos', 'RH', 'São Paulo, SP', 'Tempo Integral', 'Pleno', 1, 'Recrutamento, seleção e gestão de benefícios', 1),
('Comprador', 'Compras', 'São Paulo, SP', 'Tempo Integral', 'Pleno', 2, 'Negociação com fornecedores', 1),
('Assistente Administrativo', 'Administrativo', 'São Paulo, SP', 'Tempo Integral', 'Júnior', 3, 'Suporte administrativo geral', 1);

-- Tabela para notícias de imprensa
CREATE TABLE IF NOT EXISTS press_releases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    excerpt TEXT,
    content TEXT NOT NULL,
    image_url VARCHAR(500),
    author VARCHAR(100),
    published_date DATE NOT NULL,
    is_published BOOLEAN DEFAULT 1,
    views INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Inserir notícias de exemplo
INSERT INTO press_releases (title, slug, excerpt, content, published_date, is_published) VALUES
('BOSS SHOPP Anuncia Expansão para Novas Regiões do Brasil', 
 'expansao-novas-regioes', 
 'A BOSS SHOPP anuncia a abertura de três novos centros de distribuição nas regiões Norte e Nordeste',
 'A BOSS SHOPP anuncia a abertura de três novos centros de distribuição nas regiões Norte e Nordeste, visando reduzir o tempo de entrega e melhorar o atendimento aos clientes dessas regiões. Com investimento de R$ 50 milhões, os novos centros estarão operacionais até março de 2025.',
 '2025-01-15', 1),
('Marketplace BOSS SHOPP Alcança 1.000 Vendedores Parceiros',
 'marketplace-1000-vendedores',
 'Em apenas 6 meses desde o lançamento, o marketplace já conta com mais de 1.000 vendedores parceiros',
 'Em apenas 6 meses desde o lançamento, o marketplace da BOSS SHOPP já conta com mais de 1.000 vendedores parceiros, oferecendo uma variedade ainda maior de produtos aos clientes. A plataforma processou mais de R$ 20 milhões em transações no último trimestre.',
 '2025-01-10', 1),
('BOSS SHOPP Recebe Certificação de Sustentabilidade',
 'certificacao-sustentabilidade',
 'A empresa recebe certificação internacional por suas práticas sustentáveis',
 'A empresa recebe certificação internacional por suas práticas sustentáveis, incluindo uso de embalagens 100% recicláveis e programa de logística reversa. A BOSS SHOPP se compromete a reduzir em 50% suas emissões de carbono até 2027.',
 '2024-12-28', 1);

-- Índices para press_releases
CREATE INDEX IF NOT EXISTS idx_press_releases_slug ON press_releases(slug);
CREATE INDEX IF NOT EXISTS idx_press_releases_published ON press_releases(published_date);

-- Tabela para relatórios de investidores
CREATE TABLE IF NOT EXISTS investor_reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    report_type VARCHAR(50) NOT NULL,
    file_path VARCHAR(500),
    file_size INTEGER,
    published_date DATE NOT NULL,
    fiscal_year INTEGER,
    fiscal_quarter INTEGER,
    downloads INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Inserir relatórios de exemplo
INSERT INTO investor_reports (title, report_type, published_date, fiscal_year, fiscal_quarter, is_active) VALUES
('Relatório Anual 2024', 'annual', '2025-01-15', 2024, NULL, 1),
('Resultados 4T24', 'quarterly', '2025-01-10', 2024, 4, 1),
('Apresentação Institucional', 'presentation', '2025-01-05', 2025, NULL, 1),
('Demonstrações Financeiras 2024', 'financial', '2024-12-20', 2024, NULL, 1),
('Calendário de Eventos 2025', 'calendar', '2025-01-01', 2025, NULL, 1),
('Estatuto Social', 'statute', '2024-12-15', NULL, NULL, 1);

-- Índices para investor_reports
CREATE INDEX IF NOT EXISTS idx_investor_reports_type ON investor_reports(report_type);
CREATE INDEX IF NOT EXISTS idx_investor_reports_year ON investor_reports(fiscal_year);

-- Tabela para contatos de imprensa
CREATE TABLE IF NOT EXISTS press_contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    company VARCHAR(255),
    subject VARCHAR(255),
    message TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para press_contacts
CREATE INDEX IF NOT EXISTS idx_press_contacts_status ON press_contacts(status);
CREATE INDEX IF NOT EXISTS idx_press_contacts_created ON press_contacts(created_at);

-- Tabela para downloads de mídia kit
CREATE TABLE IF NOT EXISTS media_kit_downloads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_type VARCHAR(50) NOT NULL,
    item_name VARCHAR(255) NOT NULL,
    downloaded_by_email VARCHAR(255),
    downloaded_by_name VARCHAR(255),
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para media_kit_downloads
CREATE INDEX IF NOT EXISTS idx_media_kit_type ON media_kit_downloads(item_type);
CREATE INDEX IF NOT EXISTS idx_media_kit_created ON media_kit_downloads(created_at);

-- Tabela para eventos corporativos
CREATE TABLE IF NOT EXISTS corporate_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    event_date DATE NOT NULL,
    event_time TIME,
    location VARCHAR(255),
    description TEXT,
    is_online BOOLEAN DEFAULT 0,
    meeting_link VARCHAR(500),
    is_public BOOLEAN DEFAULT 1,
    max_participants INTEGER,
    registered_count INTEGER DEFAULT 0,
    status VARCHAR(50) DEFAULT 'scheduled',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Inserir eventos de exemplo
INSERT INTO corporate_events (title, event_type, event_date, event_time, description, is_online, is_public, status) VALUES
('Divulgação Relatório Anual 2024', 'release', '2025-01-15', '18:00:00', 'Divulgação dos resultados anuais de 2024', 1, 1, 'completed'),
('Conference Call - Resultados 4T24', 'conference', '2025-02-10', '10:00:00', 'Apresentação e discussão dos resultados do 4º trimestre', 1, 1, 'scheduled'),
('Assembleia Geral Ordinária', 'assembly', '2025-03-15', '14:00:00', 'Assembleia Geral Ordinária de Acionistas', 0, 1, 'scheduled'),
('Investor Day', 'investor_day', '2025-08-15', '09:00:00', 'Dia do Investidor com apresentações e networking', 0, 1, 'scheduled');

-- Índices para corporate_events
CREATE INDEX IF NOT EXISTS idx_corporate_events_date ON corporate_events(event_date);
CREATE INDEX IF NOT EXISTS idx_corporate_events_type ON corporate_events(event_type);
CREATE INDEX IF NOT EXISTS idx_corporate_events_status ON corporate_events(status);

-- Tabela para indicadores financeiros
CREATE TABLE IF NOT EXISTS financial_indicators (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    indicator_name VARCHAR(100) NOT NULL,
    indicator_value DECIMAL(15,2) NOT NULL,
    indicator_unit VARCHAR(20),
    comparison_value DECIMAL(15,2),
    comparison_period VARCHAR(50),
    fiscal_year INTEGER NOT NULL,
    fiscal_quarter INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Inserir indicadores atuais
INSERT INTO financial_indicators (indicator_name, indicator_value, indicator_unit, comparison_value, comparison_period, fiscal_year, fiscal_quarter) VALUES
('Receita Bruta', 250000000, 'BRL', 185000000, 'vs ano anterior', 2024, 4),
('EBITDA', 45000000, 'BRL', 31690000, 'vs ano anterior', 2024, 4),
('Margem EBITDA', 18, 'PERCENT', 15.5, 'vs ano anterior', 2024, 4),
('Novos Clientes', 150000, 'COUNT', 117000, 'vs trimestre anterior', 2024, 4),
('GMV', 95000000, 'BRL', 68000000, 'vs ano anterior', 2024, 4),
('Ticket Médio', 339, 'BRL', 295, 'vs ano anterior', 2024, 4),
('Taxa de Conversão', 3.8, 'PERCENT', 3.2, 'vs ano anterior', 2024, 4),
('NPS', 72, 'SCORE', 68, 'vs trimestre anterior', 2024, 4);

-- Índices para financial_indicators
CREATE INDEX IF NOT EXISTS idx_financial_indicators_year ON financial_indicators(fiscal_year);
CREATE INDEX IF NOT EXISTS idx_financial_indicators_quarter ON financial_indicators(fiscal_quarter);

-- Tabela para newsletter/mailing list
CREATE TABLE IF NOT EXISTS newsletter_subscribers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    subscription_type VARCHAR(50) DEFAULT 'general',
    is_active BOOLEAN DEFAULT 1,
    confirmed_at TIMESTAMP,
    unsubscribed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para newsletter_subscribers
CREATE INDEX IF NOT EXISTS idx_newsletter_email ON newsletter_subscribers(email);
CREATE INDEX IF NOT EXISTS idx_newsletter_active ON newsletter_subscribers(is_active);

-- Atualizar tabela de usuários com novos campos
-- Nota: SQLite não suporta IF NOT EXISTS em ALTER TABLE, então ignoramos erros se já existir

-- Criar view para estatísticas de candidaturas
CREATE VIEW IF NOT EXISTS job_applications_stats AS
SELECT 
    position,
    COUNT(*) as total_applications,
    SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending,
    SUM(CASE WHEN status = 'reviewing' THEN 1 ELSE 0 END) as reviewing,
    SUM(CASE WHEN status = 'approved' THEN 1 ELSE 0 END) as approved,
    SUM(CASE WHEN status = 'rejected' THEN 1 ELSE 0 END) as rejected,
    DATE(created_at) as application_date
FROM job_applications
GROUP BY position, DATE(created_at);

-- Criar view para estatísticas de downloads de relatórios
CREATE VIEW IF NOT EXISTS report_downloads_stats AS
SELECT 
    report_type,
    COUNT(*) as total_downloads,
    fiscal_year,
    fiscal_quarter
FROM investor_reports
GROUP BY report_type, fiscal_year, fiscal_quarter;

-- Criar trigger para atualizar updated_at automaticamente
CREATE TRIGGER IF NOT EXISTS update_job_applications_timestamp 
AFTER UPDATE ON job_applications
BEGIN
    UPDATE job_applications SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS update_job_openings_timestamp 
AFTER UPDATE ON job_openings
BEGIN
    UPDATE job_openings SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS update_press_releases_timestamp 
AFTER UPDATE ON press_releases
BEGIN
    UPDATE press_releases SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS update_investor_reports_timestamp 
AFTER UPDATE ON investor_reports
BEGIN
    UPDATE investor_reports SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- Mensagem de conclusão
SELECT 'Schema atualizado com sucesso!' as message;
