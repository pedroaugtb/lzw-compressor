# print_stats.py

import json
import os
import glob

def load_all_stats(directory):
    """
    Carrega todos os arquivos JSON de estatísticas da pasta especificada.
    """
    stats_list = []
    if not os.path.exists(directory):
        print(f"O diretório '{directory}' não foi encontrado.")
        return stats_list
    files = glob.glob(os.path.join(directory, '*.json'))
    for file_path in files:
        try:
            with open(file_path, 'r') as f:
                stats = json.load(f)
                stats['file_name'] = os.path.basename(file_path)
                stats_list.append(stats)
        except json.JSONDecodeError:
            print(f"Erro ao decodificar o arquivo '{file_path}'.")
    return stats_list

def map_file_types(all_stats):
    """
    Mapeia os nomes dos arquivos para seus respectivos tipos e operações.
    """
    file_type_mapping = {
        'input.txt': 'Arquivo TXT',
        'input.csv': 'Arquivo CSV',
        'input.bmp': 'Imagem BMP',
        'input.log': 'Arquivo LOG'
    }

    stats_file_mapping = {
        'compression_stats.json': 'input.txt',
        'compression_stats2.json': 'input.csv',
        'compression_stats3.json': 'input.bmp',
        'compression_stats4.json': 'input.log',
        'decompression_stats.json': 'input.txt',
        'decompression_stats2.json': 'input.csv',
        'decompression_stats3.json': 'input.bmp',
        'decompression_stats4.json': 'input.log'
    }

    for stats in all_stats:
        stats_file_name = stats.get('file_name', '')
        associated_input = stats_file_mapping.get(stats_file_name)
        if associated_input:
            stats['input_file'] = associated_input
            stats['file_type'] = file_type_mapping.get(associated_input, 'Desconhecido')
            # Identificar a operação com base no nome do arquivo de estatísticas
            if 'compression' in stats_file_name:
                stats['operation'] = 'Compressão'
            elif 'decompression' in stats_file_name:
                stats['operation'] = 'Descompressão'
            else:
                stats['operation'] = 'Desconhecida'
        else:
            stats['input_file'] = 'N/A'
            stats['file_type'] = 'Desconhecido'
            stats['operation'] = 'Desconhecida'

    # Filtrar para incluir apenas os tipos desejados e operações conhecidas
    desired_types = ['Arquivo TXT', 'Arquivo CSV', 'Imagem BMP', 'Arquivo LOG']
    desired_operations = ['Compressão', 'Descompressão']
    all_stats[:] = [stats for stats in all_stats if stats.get('file_type') in desired_types and stats.get('operation') in desired_operations]

def generate_summary(all_stats):
    """
    Gera um resumo consolidado das estatísticas.
    """
    summary = ""
    for stats in all_stats:
        summary += f"### Arquivo: {stats.get('file_type')} - {stats.get('operation')}\n"
        if stats.get('operation') == 'Compressão':
            summary += f"- **Tamanho Original:** {stats.get('original_size_bytes', 'N/A')} bytes\n"
            summary += f"- **Tamanho Comprimido:** {stats.get('compressed_size_bytes', 'N/A')} bytes\n"
            summary += f"- **Razão de Compressão:** {stats.get('compression_ratio', 'N/A')}\n"
        elif stats.get('operation') == 'Descompressão':
            summary += f"- **Tamanho Comprimido:** {stats.get('compressed_size_bytes', 'N/A')} bytes\n"
            summary += f"- **Tamanho Descomprimido:** {stats.get('decompressed_size_bytes', 'N/A')} bytes\n"
            summary += f"- **Razão de Compressão:** {stats.get('compression_ratio', 'N/A')}\n"
        summary += f"- **Tempo de Execução:** {stats.get('execution_time_seconds', 'N/A')} segundos\n"
        summary += f"- **Espaço em Memória:** {stats.get('peak_memory_usage_bytes', 'N/A')} bytes\n\n"
    return summary

def main():
    stats_directory = 'stats'  # Diretório onde os arquivos de estatísticas estão armazenados
    all_stats = load_all_stats(stats_directory)

    if not all_stats:
        print("Nenhuma estatística encontrada para exibir.")
        return

    map_file_types(all_stats)

    summary_text = generate_summary(all_stats)
    print("===== Resumo das Estatísticas =====\n")
    print(summary_text)

    # Opcional: Imprimir dados detalhados
    show_detailed = input("Deseja ver os dados brutos detalhados? (s/n): ").strip().lower()
    if show_detailed == 's':
        for stats in all_stats:
            print(f"--- Dados Detalhados para {stats.get('file_type')} - {stats.get('operation')} ---")
            print(json.dumps(stats, indent=4))
            print("\n")

if __name__ == '__main__':
    main()