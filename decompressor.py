# decompressor.py

from bitreader import BitReader
import time
import json
import os
import psutil
import sys

def lzw_decompress_static(input_file_path, output_file_path, max_bits=12, collect_stats=False, stats_file_path="stats/decompression_stats4.json"):
    # Initialize the dictionary
    dictionary = {i: chr(i) for i in range(256)}
    next_code = 256
    max_table_size = 2 ** max_bits
    
    # Initialize statistics
    stats = {
        "compressed_size_bytes": 0,
        "decompressed_size_bytes": 0,
        "compression_ratio": 0.0,
        "number_of_codes": 0,
        "execution_time_seconds": 0.0,
        "dictionary_size_over_time": [],  # Added
        "peak_memory_usage_bytes": 0  # Added
    }
    
    start_time = time.time()
    
    process = psutil.Process(os.getpid())
    peak_memory = process.memory_info().rss  # Initial memory usage
    
    # Read input data and decompress
    with open(input_file_path, 'rb') as input_file, open(output_file_path, 'wb') as output_file:
        bit_reader = BitReader(input_file)
        stats["compressed_size_bytes"] = os.path.getsize(input_file_path)
        
        # Read the first code
        previous_code = bit_reader.read_bits(max_bits)
        if previous_code is None:
            # Empty input file
            return stats
        
        string = dictionary.get(previous_code, '')
        output_file.write(string.encode('latin1'))
        stats["dict_size_over_time"] = [len(dictionary)]  # Initialize
        
        while True:
            code = bit_reader.read_bits(max_bits)
            if code is None:
                break
            
            if code in dictionary:
                entry = dictionary[code]
            elif code == next_code:
                entry = string + string[0]
            else:
                raise ValueError(f"Bad compressed code: {code}")
            
            output_file.write(entry.encode('latin1'))
            stats["number_of_codes"] += 1
            
            # Add new entry to the dictionary
            if next_code < max_table_size:
                dictionary[next_code] = string + entry[0]
                next_code += 1
                stats["dictionary_size_over_time"].append(len(dictionary))  # Record dictionary size
            
            string = entry
    
    end_time = time.time()
    stats["execution_time_seconds"] = end_time - start_time
    
    # Get peak memory usage
    current_memory = process.memory_info().rss
    stats["peak_memory_usage_bytes"] = max(peak_memory, current_memory)
    
    # Calculate decompressed size
    stats["decompressed_size_bytes"] = os.path.getsize(output_file_path)
    
    # Calculate compression ratio
    if stats["decompressed_size_bytes"] > 0:
        stats["compression_ratio"] = stats["decompressed_size_bytes"] / stats["compressed_size_bytes"]
    else:
        stats["compression_ratio"] = 0.0
    
    if collect_stats:
        # Ensure the stats directory exists
        os.makedirs(os.path.dirname(stats_file_path), exist_ok=True)
        # Write statistics to a JSON file
        with open(stats_file_path, 'w') as stats_file:
            json.dump(stats, stats_file, indent=4)
    
    return stats

def lzw_decompress_dynamic(input_file_path, output_file_path, max_bits=12, collect_stats=False, stats_file_path="stats/decompression_stats4.json"):
    # Initialize the dictionary
    # dictionary = {i: chr(i) for i in range(256)}
    # next_code = 256
    # current_bits = 9
    # max_code = (1 << current_bits) - 1
    # max_table_size = 2 ** max_bits
    
    # Initialize statistics
    stats = {
        "compressed_size_bytes": 0,
        "decompressed_size_bytes": 0,
        "compression_ratio": 0.0,
        "number_of_codes": 0,
        "execution_time_seconds": 0.0,
        "peak_memory_usage_bytes": 0,  # Optional
        "dictionary_size_over_time": []  # Added
    }
    
    start_time = time.time()
    
    process = psutil.Process(os.getpid())
    peak_memory = process.memory_info().rss  # Initial memory usage
    
    stats["compressed_size_bytes"] = os.path.getsize(input_file_path)
    
    with open(input_file_path, 'rb') as f:
        max_bits_dynamic = int.from_bytes(f.read(1), byteorder='big')
        code_size = (max_bits_dynamic + 7) // 8
        compressed_data = []
        while chunk := f.read(code_size):
            compressed_data.append(int.from_bytes(chunk, byteorder='big'))

    current_bits = 9
    max_code = (1 << current_bits) - 1
    dictionary = {i: chr(i) for i in range(256)}
    next_code = 256

    result = []
    if not compressed_data:
        return stats  # Empty input
    
    current_string = dictionary[compressed_data[0]]
    result.append(current_string)
    stats["dictionary_size_over_time"].append(len(dictionary))  # Initialize

    for code in compressed_data[1:]:
        if code in dictionary:
            entry = dictionary[code]
        elif code == next_code:
            entry = current_string + current_string[0]
        else:
            raise ValueError("Código inválido durante a descompressão.")
        
        result.append(entry)
        stats["number_of_codes"] += 1

        if next_code <= max_code:
            dictionary[next_code] = current_string + entry[0]
            next_code += 1
            stats["dictionary_size_over_time"].append(len(dictionary))  # Record dictionary size

        if next_code > max_code and current_bits < max_bits:
            current_bits += 1
            max_code = (1 << current_bits) - 1
        
        current_string = entry

    with open(output_file_path, 'w', encoding='latin1') as f:
        f.write(''.join(result))
    
    print(f"Arquivo descomprimido salvo em: {output_file_path}")
    
    end_time = time.time()
    stats["execution_time_seconds"] = end_time - start_time
    
    # Get peak memory usage
    current_memory = process.memory_info().rss
    stats["peak_memory_usage_bytes"] = max(peak_memory, current_memory)
    
    # Calculate decompressed size
    stats["decompressed_size_bytes"] = os.path.getsize(output_file_path)
    
    # Calculate compression ratio
    if stats["decompressed_size_bytes"] > 0:
        stats["compression_ratio"] = stats["decompressed_size_bytes"] / stats["compressed_size_bytes"]
    else:
        stats["compression_ratio"] = 0.0
    
    if collect_stats:
        # Ensure the stats directory exists
        os.makedirs(os.path.dirname(stats_file_path), exist_ok=True)
        # Write statistics to a JSON file
        with open(stats_file_path, 'w') as stats_file:
            json.dump(stats, stats_file, indent=4)
    
    return stats