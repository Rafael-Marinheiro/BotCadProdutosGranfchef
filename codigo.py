# bot de cadastro de produtos no sistema Grandchef
# Autor: Rafael Marinheiro
# Data: 15/01/2025
# Versão: 1.0

import pyautogui
import time
import pandas as pd
import numpy as np
import os

# 0 - Conectar-se ao arquivo .csv com os dados dos produtos a serem cadastrados no sistema Grandchef.
produtos_df = pd.read_csv('Tabela produtos.csv', encoding='latin1', sep=';')


# Filtrar as pizzas
pizzas_df = produtos_df[produtos_df['DESCRICAO'].str.contains('PIZZA', na=True)]
# Salvar as pizzas em um arquivo
pizzas_df.to_csv('pizzas_output.csv', index=False, encoding='latin1', sep=';')

# Filtrar os outros produtos
#outros_produtos_df = produtos_df[~produtos_df['GRUPO'].str.contains('PIZZA', na=False)]
outros_produtos_df = produtos_df[~(produtos_df['DESCRICAO'].str.contains('PIZZA', na=False) | 
                                   produtos_df['DESCRICAO'].str.contains('BORDA', na=False))]

# Salvar os outros produtos em um arquivo
outros_produtos_df.to_csv('outros_produtos_output.csv', index=False, encoding='latin1', sep=';')


#Salvar os produtos borda em um arquivo
borda_df = produtos_df[produtos_df['DESCRICAO'].str.contains('BORDA', na=True)]
borda_df.to_csv('borda_output.csv', index=False, encoding='latin1', sep=';')

print("Dados das pizzas e outros produtos foram salvos com sucesso.")

# 1 - Abrir o programa Grandchef
os.startfile(r"C:\Program Files (x86)\GrandChef\GrandChef.exe")
time.sleep(3)  # Aguardar o programa abrir

# 2 - Digitar a senha e pressionar Enter
pyautogui.typewrite("123456")
pyautogui.press("enter")
time.sleep(4)  # Aguardar o programa carregar

# 3 - Clicar para fechar janela de propaganda 1
pyautogui.click(x=1150, y=252)
time.sleep(6)  # Aguardar o programa carregar

# 4 - Clicar para fechar janela de propaganda 2
pyautogui.click(x=1180, y=375)

# 5 - Clicar no módulo de produtos (x=466, y=66)
pyautogui.click(x=466, y=66)
time.sleep(0.5)
pyautogui.click(x=134, y=125)
time.sleep(0.5)


#################################### CADASTRO DA TABELA DE PRODUTOS NÃO PIZZAS ####################################

tabela_op = pd.read_csv('outros_produtos_output.csv', encoding='latin1', sep=';')

# Conjunto para rastrear os grupos já cadastrados
grupos_cadastrados = set()

#  Abrir o campo de cadastro de "Grupos de Produtos"
pyautogui.PAUSE = 1.5

for linha in tabela_op.index:
    pyautogui.press("insert")
    pyautogui.write(str(tabela_op.loc[linha, "DESCRICAO"]))  # Nome do grupo de produtos
    

# Verificar se o grupo já foi cadastrado
    grupo = str(tabela_op.loc[linha, "GRUPO"])
    if grupo not in grupos_cadastrados:
        pyautogui.press("enter")
        pyautogui.press("+")
        pyautogui.typewrite(grupo)  # Nome do grupo de produtos
        pyautogui.click(x=1019, y=454)
        pyautogui.press("esc")
        grupos_cadastrados.add(grupo)  # Adicionar grupo ao conjunto

    pyautogui.doubleClick(x=1758, y=289)
    pyautogui.typewrite(str(tabela_op.loc[linha, "PRECO_VENDA"]))  # Preço do produto
    pyautogui.hotkey("ctrl", "enter")


#################################### CADASTRO DA TABELA DE PRODUTOS PIZZAs ####################################


# Verificar se o arquivo existe
if not os.path.exists('pizzas_output.csv'):
    raise FileNotFoundError("O arquivo 'pizzas_output.csv' não foi encontrado.")

tabela_pizzas = pd.read_csv('pizzas_output.csv', encoding='latin1', sep=';')

# Imprimir as colunas do DataFrame
print("Colunas disponíveis:", tabela_pizzas.columns.tolist())

# 2. Agrupamento e criação da nova tabela
df_nova = pd.DataFrame(columns=['DESCRICAO', 'GRUPO', 'VALOR TAMANHO PEQUENA', 'VALOR TAMANHO MEDIA', 'VALOR TAMANHO GRANDE', 'VALOR TAMANHO GIGANTE'])

# Iterar sobre as linhas da tabela de pizzas
for index, row in tabela_pizzas.iterrows():
    descricao = row['DESCRICAO']
    grupo = row['GRUPO']
    tamanho = row['TAMANHO']
    
    # Verificar se o tamanho é uma string antes de chamar strip()
    if isinstance(tamanho, str):
        tamanho = tamanho.strip()  # Remover espaços em branco
    else:
        print(f"Aviso: O tamanho na linha {index} não é uma string. Valor: {tamanho}")
        continue  # Ignorar esta linha se o tamanho não for uma string

    preco_venda = row['PRECO_VENDA']
    
    print(f"Processando: {descricao}, {grupo}, {tamanho}, {preco_venda}")  # Instrução de depuração
    
    # Formatar o preço com 2 casas decimais e vírgula como separador
    preco_formatado = f"{float(preco_venda):.2f}".replace(".", ",")

    
    # Verificar se a descrição e o grupo já existem no DataFrame df_nova
    if ((df_nova['DESCRICAO'] == descricao) & (df_nova['GRUPO'] == grupo)).any():
        # Se existir, atualizar o preço na coluna correspondente ao tamanho
        df_nova.loc[(df_nova['DESCRICAO'] == descricao) & (df_nova['GRUPO'] == grupo), f'VALOR TAMANHO {tamanho}'] = preco_formatado
    else:
        # Se não existir, adicionar uma nova linha
        nova_linha = pd.DataFrame({'DESCRICAO': [descricao], 'GRUPO': [grupo], f'VALOR TAMANHO {tamanho}': [preco_formatado]})
        df_nova = pd.concat([df_nova, nova_linha], ignore_index=True)

# Remover colunas duplicadas, se existirem
df_nova = df_nova.loc[:, ~df_nova.columns.duplicated()]

# 4. Exportação da nova tabela
df_nova.to_csv('pizzas_nova_tabela.csv', index=False, encoding='latin1', sep=';')

tabela_pizzas = pd.read_csv('pizzas_nova_tabela.csv', encoding='latin1', sep=';')

pyautogui.PAUSE = 1.5
pyautogui.press("insert") #Abrir menu de cadastro  
pyautogui.press("enter")
pyautogui.press("+")
pyautogui.typewrite(grupo)  # Nome do grupo de produtos
pyautogui.sleep(2)
pyautogui.click(x=1019, y=454)
pyautogui.press("esc")


for linha in tabela_pizzas.index:
    pyautogui.press("insert")
    pyautogui.click(x=406, y=213)
    pyautogui.write(str(tabela_pizzas.loc[linha, "DESCRICAO"]))  # Nome do grupo de produtos
    pyautogui.hotkey("ctrl", "enter")

pyautogui.press("insert")
pyautogui.write("Pacote Pizzas")
pyautogui.click(x=556, y=137)
pyautogui.click(x=37, y=192)
pyautogui.hotkey("ctrl", "enter")
pyautogui.write("Pacote Pizzas")
pyautogui.press("enter")
pyautogui.click(x=556, y=137)
pyautogui.click(x=129, y=231)


pyautogui.write("TAMANHO")
pyautogui.click(x=1283, y=275)
pyautogui.click(x=1281, y=309)
pyautogui.press("tab")
pyautogui.write("1")
pyautogui.press("tab")
pyautogui.write("1")
pyautogui.click(x=1136, y=320)
pyautogui.click(x=676, y=376)


pyautogui.click(x=662, y=562)   #Abrir aba tipo de item
pyautogui.click(x=632, y=594)   #Escolher tipo de item = Propriedade
pyautogui.click(x=970, y=564)  #Pop-up para Escolher nome de propriedade


pyautogui.write("TAMANHO PEQUENO")
pyautogui.press("tab") #Mudar para campo de abreviação da propriedade
pyautogui.write("P")
pyautogui.click(x=997, y=402)  #Click no botão cadastrar do pop-up de propriedades

pyautogui.write("TAMANHO MEDIO")
pyautogui.press("tab") #Mudar para campo de abreviação da propriedade
pyautogui.write("M")
pyautogui.click(x=997, y=402)  #Click no botão cadastrar do pop-up de propriedades

pyautogui.write("TAMANHO GRANDE")
pyautogui.press("tab") #Mudar para campo de abreviação da propriedade
pyautogui.write("G")
pyautogui.click(x=997, y=402)  #Click no botão cadastrar do pop-up de propriedades

pyautogui.write("TAMANHO GIGANTE")
pyautogui.press("tab") #Mudar para campo de abreviação da propriedade
pyautogui.write("GG")
pyautogui.click(x=997, y=402)  #Click no botão cadastrar do pop-up de propriedades

pyautogui.press("esc") #Fechar pop-up de propriedades

pyautogui.click(x=941, y=562) #Abrir aba de propriedades cadastradas
pyautogui.click(x=936, y=578) #Selecionar tamanho pequeno
pyautogui.click(x=1155, y=602) #Selecionar Cadastrar Valor

pyautogui.click(x=941, y=562) #Abrir aba de propriedades cadastradas
pyautogui.click(x=820, y=602) #Selecionar tamanho medio
pyautogui.click(x=1155, y=602) #Selecionar Cadastrar Valor

pyautogui.click(x=941, y=562) #Abrir aba de propriedades cadastradas
pyautogui.click(x=785, y=617) #Selecionar tamanho grande
pyautogui.click(x=1155, y=602) #Selecionar Cadastrar Valor

pyautogui.click(x=941, y=562) #Abrir aba de propriedades cadastradas
pyautogui.click(x=786, y=632) #Selecionar tamanho gigante
pyautogui.click(x=1155, y=602) #Selecionar Cadastrar Valor

pyautogui.click(x=652, y=278) #Campo de descrição do pacote
pyautogui.write("ESCOLHA OS SABORES")
pyautogui.click(x=1283, y=275)
pyautogui.click(x=1281, y=309)
pyautogui.press("tab")
pyautogui.write("1")
pyautogui.press("tab")
pyautogui.write("2")
pyautogui.click(x=1136, y=320)
pyautogui.click(x=659, y=392)  #Selecionar pacote de sabores

pyautogui.click(x=798, y=611)   #Abrir aba tipo de associação
pyautogui.click(x=717, y=645)  #Escolher associação ao tamanho pequeno

pyautogui.click(x=663, y=566)   #Abrir aba tipo de item
pyautogui.click(x=609, y=580)   #Selecionar opção produtos

################# Pacote pequeno ##########################

for linha in tabela_pizzas.index:
    pyautogui.click(x=750, y=560) #clicar
    pyautogui.hotkey("ctrl", "a")
    pyautogui.write(str(tabela_pizzas.loc[linha, "DESCRICAO"]))
    pyautogui.press("enter")
    pyautogui.write(str(tabela_pizzas.loc[linha, "VALOR TAMANHO PEQUENA"]))
    pyautogui.click(x=1139, y=604) #Cadastrar valor

################# Pacote medio ##########################

pyautogui.click(x=798, y=611)   #Abrir aba tipo de associação
pyautogui.click(x=713, y=663)  #Escolher associação ao tamanho medio

for linha in tabela_pizzas.index:
    pyautogui.click(x=750, y=560) #clicar
    pyautogui.hotkey("ctrl", "a")
    pyautogui.write(str(tabela_pizzas.loc[linha, "DESCRICAO"]))
    pyautogui.press("enter")
    pyautogui.write(str(tabela_pizzas.loc[linha, "VALOR TAMANHO MEDIA"]))
    pyautogui.click(x=1139, y=604) #Cadastrar valor

################# Pacote grande ##########################

pyautogui.click(x=798, y=611)   #Abrir aba tipo de associação
pyautogui.click(x=677, y=679)  #Escolher associação ao tamanho medio

for linha in tabela_pizzas.index:
    pyautogui.click(x=750, y=560) #clicar
    pyautogui.hotkey("ctrl", "a")
    pyautogui.write(str(tabela_pizzas.loc[linha, "DESCRICAO"]))
    pyautogui.press("enter")
    pyautogui.write(str(tabela_pizzas.loc[linha, "VALOR TAMANHO GRANDE"]))
    pyautogui.click(x=1139, y=604) #Cadastrar valor

################# Pacote gigante ##########################

pyautogui.click(x=798, y=611)   #Abrir aba tipo de associação
pyautogui.click(x=676, y=692)  #Escolher associação ao tamanho medio

for linha in tabela_pizzas.index:
    pyautogui.click(x=750, y=560) #clicar
    pyautogui.hotkey("ctrl", "a")
    pyautogui.write(str(tabela_pizzas.loc[linha, "DESCRICAO"]))
    pyautogui.press("enter")
    pyautogui.write(str(tabela_pizzas.loc[linha, "VALOR TAMANHO GIGANTE"]))
    pyautogui.click(x=1139, y=604) #Cadastrar valor