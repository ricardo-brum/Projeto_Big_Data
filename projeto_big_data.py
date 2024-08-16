import pandas as pd

# 1. Carregar os dados de vendas e estoque
# Suponha que os dados de vendas estejam em 'vendas_padaria.csv'
# e os dados de estoque estejam em 'estoque_padaria.csv'

# Dados de vendas: colunas ['Data', 'Produto', 'Quantidade', 'Preço']
df_vendas = pd.read_csv('vendas_padaria.csv')

# Dados de estoque: colunas ['Produto', 'Estoque_Inicial', 'Estoque_Atual', 'Custo_Unitario']
df_estoque = pd.read_csv('estoque_padaria.csv')

# 2. Calcular a receita total por venda
df_vendas['Receita'] = df_vendas['Quantidade'] * df_vendas['Preço']

# 3. Agrupar os dados de vendas por produto para calcular a quantidade total vendida e a receita
resumo_vendas = df_vendas.groupby('Produto').agg(
    Quantidade_Vendida=('Quantidade', 'sum'),
    Receita_Total=('Receita', 'sum')
).reset_index()

# 4. Combinar os dados de vendas com os dados de estoque
df_resumo = pd.merge(resumo_vendas, df_estoque, on='Produto')

# 5. Calcular o estoque restante e a necessidade de reabastecimento
df_resumo['Estoque_Final'] = df_resumo['Estoque_Inicial'] - df_resumo['Quantidade_Vendida']
df_resumo['Reabastecer'] = df_resumo['Estoque_Final'] < 10  # Supondo que 10 seja o limite mínimo para reabastecimento

# 6. Calcular o custo total do estoque restante
df_resumo['Custo_Estoque_Final'] = df_resumo['Estoque_Final'] * df_resumo['Custo_Unitario']

# 7. Exibir o resumo final
print("Resumo das Vendas e Estoque:")
print(df_resumo[['Produto', 'Quantidade_Vendida', 'Receita_Total', 'Estoque_Final', 'Reabastecer', 'Custo_Estoque_Final']])

# 8. Análise básica: Produto que mais precisa de reabastecimento
produtos_a_reabastecer = df_resumo[df_resumo['Reabastecer'] == True]
print("\nProdutos que precisam de reabastecimento:")
print(produtos_a_reabastecer[['Produto', 'Estoque_Final']])

# 9. Receita total e custo total do estoque final
receita_total = df_resumo['Receita_Total'].sum()
custo_estoque_total = df_resumo['Custo_Estoque_Final'].sum()

print(f"\nReceita total de todos os produtos: R$ {receita_total:.2f}")
print(f"Custo total do estoque final: R$ {custo_estoque_total:.2f}")

# 10. Exportar o resumo para um arquivo CSV
df_resumo.to_csv('resumo_vendas_estoque_padaria.csv', index=False)
