# Bot de Cadastro de Produtos no Sistema Grandchef

## Descrição
Este projeto é um bot desenvolvido para cadastrar produtos no sistema Grandchef, filtrando e organizando dados de um arquivo CSV, 
pois o cadastro de produtos PIZZAS e NÃO-PIZZAS é feito de forma diferente. 

## Instalação
Para instalar as dependências necessárias, execute o seguinte comando:
```
pip install pyautogui pandas numpy
```

## Como Usar
1. Certifique-se de que o arquivo `Tabela produtos.csv` está no mesmo diretório que o script.
2. Execute o script `codigo.py` para iniciar o bot.

## Arquivos Principais
- `codigo.py`: Lógica principal do bot.
- `beta_pizza.py`: Versão beta do código de cadastro de pizzas
- `Auxiliar.py`: Funções auxiliares para manipulação de dados.
- `pizzas_nova_tabela.csv`: Arquivo gerado com a nova tabela de pizzas.
