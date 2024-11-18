import streamlit as st
import json
import os
import plotly.graph_objects as go
import pandas as pd
import glob
import plotly.express as px
import numpy as np

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

# Mapeamento de nomes de arquivos para tipos de texto
file_type_mapping = {
    'input.txt': 'Enunciado TP',
    'input2.txt': 'História Aleatória',
    'input3.txt': 'Bits Aleatórios',
    'input.pdf' : 'PDF'
}

# Mapeamento de arquivos de estatísticas para inputs
stats_file_mapping = {
    'compression_stats.json': 'input.txt',
    'compression_stats2.json': 'input2.txt',
    'compression_stats3.json': 'input3.txt',
    'compression_stats4.json' : 'input.pdf',
    'decompression_stats.json': 'input.txt',
    'decompression_stats2.json': 'input2.txt',
    'decompression_stats3.json': 'input3.txt',
    'decompression_stats4.json' : 'input.pdf'
}

# Carregar todas as estatísticas de compressão e descompressão da pasta 'stats'
all_stats = load_all_stats('stats')

# Atualizar os nomes dos arquivos com base nos mapeamentos
for stats in all_stats:
    stats_file_name = stats.get('file_name', '')
    associated_input = stats_file_mapping.get(stats_file_name)
    if associated_input:
        stats['input_file'] = associated_input
        stats['file_type'] = file_type_mapping.get(associated_input)
    else:
        stats['input_file'] = None
        stats['file_type'] = None

# Filtrar para incluir apenas os tipos desejados
desired_types = ['Enunciado TP', 'História Aleatória', 'Bits Aleatórios']
all_stats = [stats for stats in all_stats if stats.get('file_type') in desired_types]

# Sidebar para seleção de visualizações
st.sidebar.header("Opções de Visualização")
visualization = st.sidebar.selectbox(
    "Selecione a visualização:",
    (
        "Razão de Compressão",
        "Crescimento do Dicionário - Compressão",
        "Tempo de Execução",
        "Tamanho do Dicionário ao Longo do Tempo",
        "Heatmap de Tamanho Comprimido"
    )
)

# Funções de plotagem
def plot_compression_ratio(all_stats):
    data = []
    for stats in all_stats:
        if ('compression_ratio' in stats and 'original_size_bytes' in stats and 'compressed_size_bytes' in stats):
            data.append({
                'Tipo do Texto': stats.get('file_type'),
                'Original (bytes)': stats['original_size_bytes'],
                'Comprimido (bytes)': stats['compressed_size_bytes'],
                'Razão de Compressão': stats['compression_ratio']
            })
    if data:
        df = pd.DataFrame(data)
        fig = go.Figure(data=[
            go.Bar(name='Original', x=df['Tipo do Texto'], y=df['Original (bytes)']),
            go.Bar(name='Comprimido', x=df['Tipo do Texto'], y=df['Comprimido (bytes)'])
        ])
        fig.update_layout(
            barmode='group',
            title='Razão de Compressão para Diferentes Arquivos',
            yaxis_title='Tamanho (bytes)',
            template='plotly_dark'
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível para gerar o gráfico.")

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
                name=f"{stats.get('file_type')}"
            ))

    fig.update_layout(
        title='Crescimento do Dicionário ao Longo do Tempo (Compressão)',
        xaxis_title='Número de Códigos',
        yaxis_title='Tamanho do Dicionário',
        template='plotly_dark'
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_execution_time(all_stats):
    data = []
    for stats in all_stats:
        if 'execution_time_seconds' in stats:
            data.append({
                'Tipo do Texto': stats.get('file_type'),
                'Tempo de Execução (s)': stats['execution_time_seconds']
            })
    if data:
        df = pd.DataFrame(data)
        fig = go.Figure(data=[
            go.Bar(x=df['Tipo do Texto'], y=df['Tempo de Execução (s)'])
        ])
        fig.update_layout(
            title='Tempo de Execução para Diferentes Arquivos',
            yaxis_title='Tempo (segundos)',
            template='plotly_dark'
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível para gerar o gráfico.")

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
                name=f"{stats.get('file_type')}"
            ))

    fig.update_layout(
        title='Tamanho do Dicionário ao Longo do Tempo',
        xaxis_title='Número de Códigos',
        yaxis_title='Tamanho do Dicionário',
        template='plotly_dark'
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_compression_heatmap(all_stats):
    data = []
    for stats in all_stats:
        if 'compression_ratio' in stats and 'compressed_size_bytes' in stats:
            data.append({
                'Tipo do Texto': stats.get('file_type'),
                'Tamanho Comprimido (bytes)': stats['compressed_size_bytes'],
                'Razão de Compressão': stats['compression_ratio']
            })
    if data:
        df = pd.DataFrame(data)
        pivot_table = df.pivot_table(
            index='Tipo do Texto',
            values='Tamanho Comprimido (bytes)',
            aggfunc='mean'
        ).reset_index()

        fig = px.imshow(
            [pivot_table['Tamanho Comprimido (bytes)']],
            labels=dict(x="Tipo do Texto", y="", color="Tamanho Comprimido (bytes)"),
            x=pivot_table['Tipo do Texto'],
            y=[''],
            color_continuous_scale='Viridis',
            aspect="auto",
            text_auto=True
        )
        fig.update_layout(
            title='Heatmap do Tamanho Comprimido dos Arquivos',
            template='plotly_dark'
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível para gerar o heatmap.")

# Renderizar a visualização selecionada
if visualization == "Razão de Compressão":
    plot_compression_ratio(all_stats)
elif visualization == "Crescimento do Dicionário - Compressão":
    plot_compression_dictionary_growth(all_stats)
elif visualization == "Tempo de Execução":
    plot_execution_time(all_stats)
elif visualization == "Tamanho do Dicionário ao Longo do Tempo":
    plot_dictionary_size_over_time(all_stats)
elif visualization == "Heatmap de Tamanho Comprimido":
    plot_compression_heatmap(all_stats)

# Exibir dados brutos (opcional)
if st.sidebar.checkbox("Mostrar Dados Brutos"):
    for stats in all_stats:
        st.subheader(f"Dados Brutos para {stats.get('file_type')}")
        st.json(stats)