import sqlite3

conn = sqlite3.connect('../bossshopp_complete.db')
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = cursor.fetchall()

print('\n📊 Tabelas no banco de dados:')
for table in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
    count = cursor.fetchone()[0]
    print(f'  • {table[0]}: {count} registros')

conn.close()
