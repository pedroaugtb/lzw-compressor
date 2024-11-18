# Compressão e Descompressão de Arquivos com LZW

## Universidade Federal de Minas Gerais
### Instituto de Ciências Exatas
#### Departamento de Ciência da Computação
##### DCC207 -- Algoritmos 2

---

## Trabalho Prático 1: Manipulação de Sequências

### Prof. Renato Vimieiro

#### Pedro Augusto Torres Bento - 2022104352
#### Yan Aquino Amorim - 2022043221
---

## Índice

1. [Descrição](#descrição)
2. [Funcionalidades](#funcionalidades)
3. [Estrutura do Projeto](#estrutura-do-projeto)
4. [Requisitos](#requisitos)
5. [Instalação](#instalação)
6. [Uso](#uso)
    - [Compressão](#compressão)
    - [Descompressão](#descompressão)
    - [Processamento de Estatísticas](#processamento-de-estatísticas)
7. [Coleta de Estatísticas](#coleta-de-estatísticas)
8. [Geração de Relatórios](#geração-de-relatórios)
9. [Testes](#testes)
12. [Referências](#referências)
13. [Contato](#contato)

---

## Descrição

Este projeto implementa o algoritmo de compressão e descompressão Lempel-Ziv-Welch (LZW) utilizando árvores de prefixo (Trie) para gerenciar o dicionário. O objetivo principal é manipular sequências de dados de forma eficiente, reduzindo o tamanho dos arquivos através da substituição de sequências repetitivas por códigos.

Além da compressão e descompressão, o projeto inclui funcionalidades para coleta de estatísticas durante o processamento dos arquivos, permitindo a análise de desempenho e eficiência do algoritmo implementado.

---

## Funcionalidades

- **Compressão LZW:** Compressão de arquivos utilizando o algoritmo LZW com suporte para tamanhos de código fixo e variável.
- **Descompressão LZW**: Descompressão de arquivos previamente comprimidos com o LZW.
- **Tamanho de Código Variável**: Implementação que permite ajustar dinamicamente o tamanho dos códigos conforme o dicionário cresce.
- **Coleta de Estatísticas**: Registro de métricas como taxa de compressão, tempo de execução, uso de memória, entre outras.
- **Geração de Relatórios**: Ferramenta para processar as estatísticas coletadas e gerar gráficos e resumos em formato visual e CSV.

---

## Estrutura do Projeto

```
├── bitreader.py
├── bitwriter.py
├── compressor.py
├── decompressor.py
├── main.py
├── process_stats.py
├── trie.py
├── README.md
├── requirements.txt
└── stats/
    ├── compression_stats.json
    └── decompression_stats.json
```

- **bitreader.py**: Classe para leitura de bits a partir de um arquivo.
- **bitwriter.py**: Classe para escrita de bits em um arquivo.
- **compressor.py**: Implementação do algoritmo LZW para compressão.
- **decompressor.py**: Implementação do algoritmo LZW para descompressão.
- **main.py**: Interface de linha de comando para utilizar as funcionalidades de compressão e descompressão.
- **process_stats.py**: Script para processar e gerar relatórios a partir das estatísticas coletadas.
- **trie.py**: Implementação da árvore de prefixo (Trie) utilizada como dicionário no LZW.
- **requirements.txt**: Lista de dependências necessárias para executar o projeto.
- **stats/**: Diretório para armazenar arquivos de estatísticas coletadas.

---

## Requisitos

- **Python 3.6+**
- Bibliotecas Python:
  - `argparse`
  - `json`
  - `os`
  - `psutil`
  - `sys`
  - `matplotlib`
  - `pandas`

---

## Instalação

1. **Clone o repositório:**

    ```bash
    git clone https://github.com/pedroaugtb/lzw-compressor.git
    cd lzw-compressor
    ```

2. **Crie e ative um ambiente virtual (opcional, mas recomendado):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ```

3. **Instale as dependências:**

    ```bash
    pip install -r requirements.txt
    ```

---

## Uso

O programa principal é o `main.py`, que permite comprimir e descomprimir arquivos via linha de comando.

### Compressão

```bash
python main.py compress <arquivo_entrada> <arquivo_saida> [opções]
```

**Exemplo:**

```bash
python main.py compress exemplo.txt exemplo.lzw --bits 12 --variable --test
```

**Parâmetros:**

- `<arquivo_entrada>`: Caminho para o arquivo que será comprimido.
- `<arquivo_saida>`: Caminho para o arquivo comprimido resultante.
- `--bits (-b)`: Número máximo de bits para os códigos (padrão: 12).
- `--variable (-v)`: Utiliza tamanho de código variável.
- `--test (-t)`: Habilita o modo de teste para coleta de estatísticas.

### Descompressão

```bash
python main.py decompress <arquivo_entrada> <arquivo_saida> [opções]
```

**Exemplo:**

```bash
python main.py decompress exemplo.lzw exemplo_descomprimido.txt --bits 12 --variable --test
```

**Parâmetros:**

- `<arquivo_entrada>`: Caminho para o arquivo comprimido que será descomprimido.
- `<arquivo_saida>`: Caminho para o arquivo descomprimido resultante.
- `--bits (-b)`: Número máximo de bits para os códigos (padrão: 12).
- `--variable (-v)`: Utiliza tamanho de código variável.
- `--test (-t)`: Habilita o modo de teste para coleta de estatísticas.

### Processamento de Estatísticas

Após a compressão ou descompressão com a opção `--test`, você pode gerar relatórios a partir das estatísticas coletadas.

```bash
python process_stats.py <arquivo_estatisticas.json> --output_dir <diretorio_saida>
```

**Exemplo:**

```bash
python process_stats.py stats/compression_stats.json --output_dir reports/compression_reports
```

**Parâmetros:**

- `<arquivo_estatisticas.json>`: Caminho para o arquivo JSON contendo as estatísticas coletadas.
- `--output_dir (-o)`: Diretório onde os relatórios serão salvos (padrão: `reports`).

---

## Coleta de Estatísticas

Ao utilizar a opção `--test` durante a compressão ou descompressão, o programa irá coletar diversas métricas, incluindo:

- Tamanho original e comprimido dos arquivos.
- Taxa de compressão.
- Número de códigos gerados.
- Crescimento do tamanho do dicionário ao longo do processamento.
- Tempo total de execução.
- Uso máximo de memória durante o processamento.

As estatísticas são armazenadas em arquivos JSON no diretório `stats/`, permitindo uma análise posterior detalhada.

---

## Geração de Relatórios

O script `process_stats.py` processa os arquivos de estatísticas JSON e gera relatórios visuais e resumos em CSV.

### Funcionalidades:

- **Gráfico de Crescimento do Dicionário**: Mostra como o tamanho do dicionário evolui ao longo do número de códigos processados.
- **Gráfico de Razão de Compressão**: Compara o tamanho original e comprimido dos arquivos.
- **Resumo em CSV**: Exporta as estatísticas para um arquivo CSV para análises adicionais.

Os relatórios são salvos no diretório especificado pelo usuário, facilitando a visualização e interpretação dos resultados.

---

## Testes

Para garantir o funcionamento correto e avaliar o desempenho do algoritmo, realize os seguintes passos:

1. **Preparar Arquivos de Teste**: Utilize diferentes tipos de arquivos, como textos, imagens em formato bitmap, entre outros.
2. **Compressão e Descompressão**: Execute o processo de compressão e descompressão com diferentes configurações de bits e tamanho de código.
3. **Coleta de Estatísticas**: Utilize a opção `--test` para coletar métricas durante os processos.
4. **Análise dos Resultados**: Utilize o `process_stats.py` para gerar relatórios e avaliar a eficiência do algoritmo.

---

## Contribuição

Este projeto é parte de um trabalho acadêmico realizado para a disciplina de Algoritmos 2 na Universidade Federal de Minas Gerais. Entretanto, contribuições e sugestões são bem-vindas para melhorias futuras.

1. **Fork o Repositório**
2. **Crie uma Branch para sua Feature**: `git checkout -b feature/nova-feature`
3. **Commit suas Alterações**: `git commit -m 'Adiciona nova feature'`
4. **Push para a Branch**: `git push origin feature/nova-feature`
5. **Abra um Pull Request**


## Referências

- **Documentação do LZW**: [Wikipedia - LZW](https://en.wikipedia.org/wiki/Lempel%E2%80%93Ziv%E2%80%93Welch)
- **Árvores de Prefixo (Trie)**: [Wikipedia - Trie](https://en.wikipedia.org/wiki/Trie)
- **Implementação do LZW**: Salomon, David. *Data Compression: The Complete Reference*.
- **Recursos Adicionais**:
    - [Implementação de Tries](https://www.geeksforgeeks.org/trie-insert-and-search/)
    - [Uso de Bit Manipulation em Python](https://stackoverflow.com/questions/12688968/python-bit-manipulation)
