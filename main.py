import pandas as pd
tabelas_cliente = 'base_de_dados_clientes.csv'

dataset = pd.read_csv(tabelas_cliente, encoding='latin1')
print(dataset.describe())