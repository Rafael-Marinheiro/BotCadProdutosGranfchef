import pandas as pd
import os


# Verificar se o arquivo existe
if not os.path.exists('Tabela produtos.csv'):
    raise FileNotFoundError("O arquivo 'Tabela produtos.csv' não foi encontrado.")

# Ler o arquivo CSV
tabela_produtos = pd.read_csv('Tabela produtos.csv', sep=';')

# Agrupar os dados pela coluna "GRUPO" e pegar a primeira ocorrência de cada grupo
tabela_organizada = tabela_produtos.groupby('GRUPO').first().reset_index()

# Salvar os dados organizados no próprio arquivo CSV
tabela_organizada.to_csv('Tabela produtos.csv', sep=';', index=False)

print("Os produtos foram organizados e salvos em 'Tabela produtos.csv'.")

# Verificar se o arquivo existe
if not os.path.exists('borda_output.csv'):
    raise FileNotFoundError("O arquivo 'borda_output.csv' não foi encontrado.")

# Ler o arquivo CSV
tabela_produtos = pd.read_csv('borda_output.csv', sep=';')

# Agrupar os dados pela coluna "TAMANHO" e pegar a primeira ocorrência de cada grupo
tabela_organizada = tabela_produtos.groupby('TAMANHO').first().reset_index()

# Salvar os dados organizados no próprio arquivo CSV
tabela_organizada.to_csv('borda_output.csv', sep=';', index=False)

print("Os produtos foram organizados e salvos em 'borda_output.csv'.")
