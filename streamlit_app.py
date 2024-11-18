import streamlit as st
import json
import os
import plotly.graph_objects as go
import pandas as pd
import glob

# Configuração da página
st.set_page_config(page_title="Relatórios de Compressão LZW", layout="wide")

# Título da Aplicação
st.title("Relatórios de Compressão e Descompressão LZW")

# Função para carregar estatísticas de múltiplos arquivos na pasta 'stats'
def load_all_stats(directory):
    stats_list = []
    if not os.path.exists(directory):
        st.warning(f"O diretório {directory} não foi encontrado.")
        return stats_list
    files = glob.glob(os.path.join(directory, '*.json'))
    for file_path in files:
        try:
            with open(file_path, 'r') as f:
                stats = json.load(f)
                stats['file_name'] = os.path.basename(file_path)
                stats_list.append(stats)
        except json.JSONDecodeError:
            st.error(f"Erro ao decodificar o arquivo {file_path}.")
    return stats_list

# Carregar todas as estatísticas de compressão e descompressão da pasta 'stats'
all_stats = load_all_stats('stats')

# Sidebar para seleção de visualizações
st.sidebar.header("Opções de Visualização")
visualization = st.sidebar.selectbox(
    "Selecione a visualização:",
    ("Crescimento do Dicionário - Compressão",
     "Razão de Compressão",
     "Tempo de Execução",
     "Tamanho do Dicionário ao Longo do Tempo")
)

# Funções de plotagem
def plot_compression_dictionary_growth(all_stats):
    fig = go.Figure()
    for stats in all_stats:
        if 'dictionary_size_over_time' in stats and stats['dictionary_size_over_time']:
            df = pd.DataFrame({
                'Número de Códigos': range(1, len(stats['dictionary_size_over_time']) + 1),
                'Tamanho do Dicionário': stats['dictionary_size_over_time']
            })
            fig.add_trace(go.Scatter(
                x=df['Número de Códigos'],
                y=df['Tamanho do Dicionário'],
                mode='lines+markers',
                name=f"Dicionário {stats.get('file_name', 'Desconhecido')}"
            ))

    fig.update_layout(
        title='Crescimento do Dicionário ao Longo do Tempo (Compressão)',
        xaxis_title='Número de Códigos',
        yaxis_title='Tamanho do Dicionário',
        template='plotly_dark'
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_compression_ratio(all_stats):
    fig = go.Figure()
    for stats in all_stats:
        if ('compression_ratio' in stats and 'original_size_bytes' in stats and 'compressed_size_bytes' in stats):
            categories = ['Original', 'Comprimido']
            values = [stats['original_size_bytes'], stats['compressed_size_bytes']]
            fig.add_trace(go.Bar(
                x=categories,
                y=values,
                name=f"Razão de Compressão {stats.get('file_name', 'Desconhecido')}",
                marker_color=['#1f77b4', '#ff7f0e']
            ))

    fig.update_layout(
        title="Razão de Compressão para Diferentes Arquivos",
        yaxis_title='Tamanho (bytes)',
        template='plotly_dark'
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_execution_time(all_stats):
    fig = go.Figure()
    for stats in all_stats:
        if 'execution_time_seconds' in stats:
            categories = ['Tempo de Execução']
            values = [stats['execution_time_seconds']]
            fig.add_trace(go.Bar(
                x=categories,
                y=values,
                name=f"Tempo de Execução {stats.get('file_name', 'Desconhecido')}",
                marker_color=['#9467bd']
            ))

    fig.update_layout(
        title='Tempo de Execução para Diferentes Arquivos',
        yaxis_title='Tempo (segundos)',
        template='plotly_dark'
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_dictionary_size_over_time(all_stats):
    fig = go.Figure()
    for stats in all_stats:
        if 'dictionary_size_over_time' in stats and stats['dictionary_size_over_time']:
            df = pd.DataFrame({
                'Número de Códigos': range(1, len(stats['dictionary_size_over_time']) + 1),
                'Tamanho do Dicionário': stats['dictionary_size_over_time']
            })
            fig.add_trace(go.Scatter(
                x=df['Número de Códigos'],
                y=df['Tamanho do Dicionário'],
                mode='lines+markers',
                name=f"Dicionário {stats.get('file_name', 'Desconhecido')}"
            ))

    fig.update_layout(
        title='Tamanho do Dicionário ao Longo do Tempo',
        xaxis_title='Número de Códigos',
        yaxis_title='Tamanho do Dicionário',
        template='plotly_dark'
    )
    st.plotly_chart(fig, use_container_width=True)

# Renderizar a visualização selecionada
if visualization == "Crescimento do Dicionário - Compressão":
    plot_compression_dictionary_growth(all_stats)
elif visualization == "Razão de Compressão":
    plot_compression_ratio(all_stats)
elif visualization == "Tempo de Execução":
    plot_execution_time(all_stats)
elif visualization == "Tamanho do Dicionário ao Longo do Tempo":
    plot_dictionary_size_over_time(all_stats)

# Exibir dados brutos (opcional)
if st.sidebar.checkbox("Mostrar Dados Brutos"):
    for stats in all_stats:
        st.subheader(f"Dados Brutos para Arquivo {stats.get('file_name', 'Desconhecido')}")
        st.json(stats)
