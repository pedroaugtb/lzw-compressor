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

Este projeto implementa o algoritmo de compressão e descompressão Lempel-Ziv-Welch (LZW), utilizando uma estrutura Trie para gerenciar o dicionário de códigos. Ele permite comprimir e descomprimir arquivos de forma eficiente, analisando o desempenho com base em estatísticas como taxa de compressão, tempo de execução e uso de memória.

---

## Funcionalidades

- **Compressão LZW:** Compactação de arquivos com suporte a código de tamanho fixo ou variável.
- **Descompressão LZW:** Reconstrução de arquivos previamente compactados.
- **Estatísticas:** Coleta de métricas detalhadas durante o processamento, como razão de compressão, tamanho dos arquivos e número de códigos gerados.
- **Geração de Relatórios:** Processamento e visualização de estatísticas em gráficos e resumos.

---

## Estrutura do Projeto

```
├── README.md                  # Documentação do projeto
├── requirements.txt           # Dependências necessárias
├── main.py                    # Interface principal CLI para compressão e descompressão
├── compressor.py              # Algoritmo de compressão LZW
├── decompressor.py            # Algoritmo de descompressão LZW
├── trie.py                    # Implementação da estrutura Trie
├── process_stats.py           # Processamento de estatísticas coletadas
├── streamlit_app.py           # Interface visual em Streamlit
├── compressed_variable.lzw    # Exemplo de arquivo compactado
├── compressed.lzw             # Exemplo de arquivo compactado
├── inputs/                    # Diretório com arquivos de entrada
│   ├── input.bmp
│   ├── input.csv
│   ├── input.log
│   └── input.txt
├── outputs/                   # Diretório com arquivos de saída
│   ├── output.bmp
│   ├── output.csv
│   ├── output.log
│   └── output.txt
└── stats/                     # Estatísticas de compressão/descompressão
    ├── compression_stats.json
    ├── compression_stats2.json
    ├── decompression_stats.json
    └── decompression_stats2.json
```

---

## Requisitos

- **Python 3.6+**
- Bibliotecas Python:
  - `argparse`
  - `json`
  - `os`
  - `time`
  - `pandas`
  - `matplotlib`
  - `streamlit`

---

## Instalação

1. **Clone o repositório:**

    ```bash
    git clone <URL_DO_REPOSITORIO>
    cd <DIRETORIO_DO_PROJETO>
    ```

2. **Crie e ative um ambiente virtual (opcional):**

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

### Compressão

```bash
python main.py compress <arquivo_entrada> <arquivo_saida> [opções]
```

### Descompressão

```bash
python main.py decompress <arquivo_entrada> <arquivo_saida> [opções]
```

As estatísticas coletadas são salvas no diretório `stats/`.

### Interface Visual

Use o Streamlit para uma interface gráfica:

```bash
streamlit run streamlit_app.py
```
Link para o site:
```bash
https://trabalho-algoritmos-2.streamlit.app
```

## Testes

Para realizar testes, utilize arquivos de entrada variados, como `.txt`, `.csv` e `.bmp`, e compare os resultados antes e depois da compressão. Acompanhe as métricas geradas para avaliar o desempenho.

---

## Referências

- **Documentação LZW:** [Wikipedia - LZW](https://en.wikipedia.org/wiki/Lempel%E2%80%93Ziv%E2%80%93Welch)  
- **Estrutura Trie:** [Wikipedia - Trie](https://en.wikipedia.org/wiki/Trie)  
- **Recursos Adicionais:**  
    - [GeeksforGeeks - Implementação de Tries](https://www.geeksforgeeks.org/trie-insert-and-search/)  
    - [Documentação do Python para Manipulação de Bits](https://docs.python.org/3/library/struct.html)

