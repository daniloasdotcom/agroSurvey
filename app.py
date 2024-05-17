import streamlit as st
import pandas as pd
import pygsheets
import os
import matplotlib.pyplot as plt

credenciais = pygsheets.authorize(service_file=os.getcwd() + "/cred.json")
planGoogleSheets = "https://docs.google.com/spreadsheets/d/1AhsnUZFQ7yF9FypzeixHfiMAUtFgmGxj_Xebbuk8ESE/"
arquivo = credenciais.open_by_url(planGoogleSheets)
aba = arquivo.worksheet_by_title("plan01")
data = aba.get_all_values()
# Remova as colunas duplicadas da primeira linha
header = [col for col in data[0] if col != '']

# Remova as colunas vazias dos dados
data_cleaned = [[value for value in row if value != ''] for row in data[1:]]

# Use a primeira linha sem as colunas duplicadas como cabeçalho
df = pd.DataFrame(data_cleaned, columns=header)

st.title("Agrônomos 2024")
st.write("Estatística do Mercado de Trabalho Agrônomico")
st.write(df)

# Ordenar as categorias de salário para garantir que 'R$1.000 - R$2.000' seja a primeira
salary_counts = df['Qual salário você ganha hoje'].value_counts().reindex(['R$1.000 - R$2.000', 'R$2.000 - R$3.000',
                                                                           'R$3.000 - R$4.000',
                                                                           'R$4.000 - R$5.000'])
# Calcular a contagem percentual
total_count = salary_counts.sum()
percentages = (salary_counts / total_count) * 100

# Criar o gráfico de colunas usando o Matplotlib
fig, ax = plt.subplots(figsize=(8, 6))  # Defina o tamanho da figura aqui (largura, altura)
bars = salary_counts.plot(kind='bar', ax=ax)

# Adicionar a contagem percentual no topo das barras
for i, v in enumerate(salary_counts):
    ax.text(i, v + 0.1, f"{percentages[i]:.1f}%", ha='center')

# Ajustar a rotação dos rótulos do eixo x
plt.xticks(rotation=0)

# Remover o símbolo "$" e "R" dos rótulos do eixo x
tick_labels = [label.replace('$', '').replace('R', '') for label in salary_counts.index]
ax.set_xticklabels(tick_labels)

# Remover a borda superior e a borda à direita
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Mostrar o gráfico no Streamlit
st.pyplot(fig)
