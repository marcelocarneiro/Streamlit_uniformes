import pandas as pd
import pyodbc

# Configurações de conexão ao SQL Server
server = '192.168.252.25'  # Endereço do servidor SQL
database = 'CorporeRM'   # Nome do banco de dados
username = 'u_sci'     # Usuário do banco de dados
password = '@n0ss@drg'       # Senha do banco de dados

# String de conexão
conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

try:
    # Conectar ao banco de dados
    print("Tentando conectar ao banco de dados...")
    conn = pyodbc.connect(conn_str)
    print("Conexão bem-sucedida!")

    # Query SQL que você deseja executar
    query = "SELECT * FROM sua_tabela"  # Substitua pela sua consulta

    # Executar a query e carregar os dados em um DataFrame do Pandas
    print("Executando a query...")
    df = pd.read_sql(query, conn)

    # Salvar os dados em um arquivo CSV
    csv_file = 'dados_exportados.csv'
    df.to_csv(csv_file, index=False)
    print(f"Dados exportados com sucesso para {csv_file}!")

except pyodbc.Error as e:
    print(f"Erro ao conectar ou executar a query: {e}")
    print("Verifique a VPN, o nome do servidor, as credenciais e as permissões.")

finally:
    # Fechar a conexão
    if 'conn' in locals():
        conn.close()
        print("Conexão fechada.")
