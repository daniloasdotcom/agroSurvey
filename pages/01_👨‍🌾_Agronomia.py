import streamlit as st  # Importa a biblioteca Streamlit para construir a interface do aplicativo
import pandas as pd  # Importa a biblioteca Pandas para manipulação de dados
import pygsheets  # Importa a biblioteca Pygsheets para acessar planilhas do Google Sheets
import os  # Importa o módulo os para manipulação de caminhos de arquivo
import matplotlib.pyplot as plt  # Importa a biblioteca Matplotlib para visualização de dados
from matplotlib import rcParams  # Importa rcParams para configurar as propriedades da fonte

# Configurar a fonte padrão do matplotlib para Times New Roman
rcParams['font.family'] = 'serif'
rcParams['font.serif'] = ['Times New Roman'] + rcParams['font.serif']

# Definir constantes para o arquivo de credenciais do serviço do Google Sheets, URL da planilha e título da aba
SERVICE_FILE = os.path.join(os.getcwd(), "cred.json")
SHEET_URL = "https://docs.google.com/spreadsheets/d/1AhsnUZFQ7yF9FypzeixHfiMAUtFgmGxj_Xebbuk8ESE/"
SHEET_TITLE = "plan01"

def get_google_sheet_data(service_file, sheet_url, sheet_title):
    """
    Autoriza o acesso ao Google Sheets e obtém os dados da planilha especificada.

    Args:
        service_file (str): Caminho para o arquivo de credenciais do serviço.
        sheet_url (str): URL da planilha do Google Sheets.
        sheet_title (str): Título da aba a ser acessada.

    Returns:
        list: Dados da planilha como uma lista de listas.
    """
    credenciais = pygsheets.authorize(service_file=service_file)  # Autoriza o acesso usando o arquivo de credenciais
    arquivo = credenciais.open_by_url(sheet_url)  # Abre a planilha pelo URL fornecido
    aba = arquivo.worksheet_by_title(sheet_title)  # Seleciona a aba especificada
    return aba.get_all_values()  # Retorna os dados da planilha como uma lista de listas

def clean_data(data):
    """
    Limpa os dados da planilha removendo colunas duplicadas e vazias.

    Args:
        data (list): Dados brutos da planilha.

    Returns:
        pd.DataFrame: Dados limpos em um DataFrame.
    """
    header = [col for col in data[0] if col != '']  # Extrai os nomes das colunas do cabeçalho (primeira linha)
    data_cleaned = [[value for value in row if value != ''] for row in data[1:]]  # Remove valores vazios de cada linha
    return pd.DataFrame(data_cleaned, columns=header)  # Retorna os dados limpos como um DataFrame do Pandas

def plot_salary_distribution(df, x_label, bar_color='blue'):
    """
    Plota a distribuição percentual dos salários.

    Args:
        df (pd.DataFrame): DataFrame contendo os dados dos salários.
        x_label (str): Rótulo para o eixo x.
        bar_color (str): Cor das barras do gráfico.

    Returns:
        plt.Figure: Figura do Matplotlib contendo o gráfico de barras.
    """
    # Calcula a contagem de salários e a distribuição percentual
    salary_counts = df['Qual salário você ganha hoje'].value_counts().reindex(['R$1.000 - R$2.000', 'R$2.000 - R$3.000',
                                                                               'R$3.000 - R$4.000',
                                                                               'R$4.000 - R$5.000'])
    total_count = salary_counts.sum()
    percentages = (salary_counts / total_count) * 100

    # Cria um gráfico de barras
    fig, ax = plt.subplots(figsize=(8, 6))
    bars = salary_counts.plot(kind='bar', ax=ax, color=bar_color)

    # Adiciona o texto de contagem e percentagem em cada barra
    for i, v in enumerate(salary_counts):
        percentage_str = f"{percentages[i]:.1f}".replace('.', ',')
        ax.text(i, v / 2, f"{v:.0f}", ha='center', va='center', fontsize=12, fontweight='bold', color='white')
        ax.text(i, v + 0.1, f"{percentage_str}%", ha='center', fontsize=12, fontweight='bold')

    # Configurações do eixo x
    plt.xticks(rotation=0, fontsize=12, fontweight='bold')
    tick_labels = [label.replace('$', '').replace('R', '') for label in salary_counts.index]
    ax.set_xticklabels(tick_labels, fontsize=12, fontweight='bold')

    # Configurações dos eixos e do título
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.yaxis.set_visible(False)
    ax.set_title('Distribuição Percentual dos Salários', fontsize=15, fontweight='bold')
    ax.set_xlabel(x_label, fontsize=12, fontweight='bold', labelpad=15)

    # Define o valor máximo do eixo y para o maior valor de frequência mais 2 unidades
    max_freq = max(salary_counts) + 2
    ax.set_ylim(0, max_freq)

    return fig

def main():
    # Obtém e limpa os dados da planilha
    data = get_google_sheet_data(SERVICE_FILE, SHEET_URL, SHEET_TITLE)
    df = clean_data(data)

    # Cria o layout do aplicativo no Streamlit
    st.title("Agrônomos 2024")
    st.write("Estatística do Mercado de Trabalho Agrônomico")

    # Cria três colunas no Streamlit com larguras específicas
    col1, col2, col3 = st.columns([0.1, 0.8, 0.1])

    # Plota e exibe o gráfico na segunda coluna (mais larga)
    with col2:
        fig = plot_salary_distribution(df, "Faixa Salarial (R$)", bar_color='black')
        st.pyplot(fig)

# Executa o aplicativo principal
if __name__ == "__main__":
    main()

