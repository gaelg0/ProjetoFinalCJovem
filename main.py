import pandas as pd

# Ler arquivo
arquivoCsv = 'baseDados.csv'
tabela = pd.read_csv(arquivoCsv, encoding='latin1')

# Preencher valores ausentes
for coluna in tabela.select_dtypes(include=['object']).columns:
    tabela[coluna].fillna(tabela[coluna].mode()[0], inplace=True)

# Tentar converter todas as colunas numéricas para tipo numérico
for coluna in tabela.select_dtypes(include=['object']).columns:
    tabela[coluna] = pd.to_numeric(tabela[coluna], errors='coerce')

# Preencher valores ausentes nas colunas numéricas com a média
tabela.fillna(tabela.mean(), inplace=True)

#criar coluna de riscos de calote
tabela['RiscoCalote'] = 0

# verificar se a taxa de utilizacao é maior que 75%
tabela.loc[tabela['Taxa de Utilização Cartão'] > 0.75, 'RiscoCalote'] += 2

# verificar se o limite disponivel é menor que 1000
tabela.loc[tabela['Limite Disponível'] < 1000, 'RiscoCalote'] += 1

# verificar se o limite consumido é maior que 
tabela.loc[tabela['Limite Consumido'] > tabela['Limite Disponível'] * 0.75, 'RiscoCalote'] += 2

# verificar se a mudança de transações é maior que 1
tabela.loc[tabela['Mudanças Transacoes_Q4_Q1'] > 1, 'RiscoCalote'] += 1

# verificar se esteve ausente por mais de 3 meses
tabela.loc[tabela['Inatividade 12m'] > 3, 'RiscoCalote'] += 1

# vefificar se o salario anual é menor que 40k
tabela.loc[tabela['Faixa Salarial Anual'] == 'Less than $40K', 'RiscoCalote'] += 2


clientesCaloteiros = tabela[tabela['RiscoCalote'] >= 5]
clientesCaloteiros = clientesCaloteiros[['CLIENTNUM', 'RiscoCalote']]
print(clientesCaloteiros)