# decompressor.py

from bitreader import BitReader
import time
import json
import os
import psutil
import sys

def read_codes_from_file(input_file, max_bits, variable_code_size):
    bit_reader = BitReader(input_file)
    codes = []
    code_size = 9 if variable_code_size else max_bits
    max_table_size = 2 ** max_bits
    next_code_increase = 2 ** code_size
    next_code = 256

    while True:
        code = bit_reader.read_bits(code_size)
        if code is None:
            break
        codes.append(code)
        if variable_code_size:
            if next_code >= next_code_increase and code_size < max_bits:
                code_size += 1
                next_code_increase = 2 ** code_size
            next_code += 1
    return codes

def lzw_decompress(input_file_path, output_file_path, max_bits=12, variable_code_size=False, collect_stats=False, stats_file_path="stats/decompression_stats4.json"):
    # Initialize the dictionary
    dictionary = {i: chr(i) for i in range(256)}
    next_code = 256
    max_table_size = 2 ** max_bits
    dictionary_sizes = []
    
    # Initialize statistics
    stats = {
        "compressed_size_bytes": 0,
        "decompressed_size_bytes": 0,
        "execution_time_seconds": 0.0,
        "dictionary_size_over_time": [],
        "peak_memory_usage_bytes": 0  # Optional
    }
    
    start_time = time.time()
    
    process = psutil.Process(os.getpid())
    peak_memory = 0
    
    # Read input codes from the file
    with open(input_file_path, 'rb') as input_file:
        codes = read_codes_from_file(input_file, max_bits, variable_code_size)
        stats["compressed_size_bytes"] = os.path.getsize(input_file_path)
    
    if not codes:
        # Empty input file, write empty output
        with open(output_file_path, 'wb') as output_file:
            pass  # Create an empty file
        return stats
    
    # Decompression variables
    result = []
    code_size = 9 if variable_code_size else max_bits
    next_code_increase = 2 ** code_size
    
    # Process the codes
    try:
        previous_code = codes.pop(0)
    except IndexError:
        # No codes to process
        with open(output_file_path, 'wb') as output_file:
            pass
        return stats
    
    string = dictionary.get(previous_code, '')
    result.append(string)
    
    for code in codes:
        if code in dictionary:
            entry = dictionary[code]
        elif code == next_code:
            entry = string + string[0]
        else:
            raise ValueError(f"Bad compressed code: {code}")
        result.append(entry)
    
        # Add new sequence to the dictionary
        if next_code < max_table_size:
            dictionary[code_size] = string + entry[0]
            dictionary[next_code] = string + entry[0]
            next_code += 1
            dictionary_sizes.append(next_code)
            if variable_code_size and next_code >= next_code_increase and code_size < max_bits:
                code_size += 1
                next_code_increase = 2 ** code_size
        string = entry
    
    decompressed_data = ''.join(result)
    stats["decompressed_size_bytes"] = len(decompressed_data.encode('latin1'))
    stats["dictionary_size_over_time"] = dictionary_sizes.copy()
    
    # Write the decompressed data to the output file
    with open(output_file_path, 'wb') as output_file:
        output_file.write(decompressed_data.encode('latin1'))
    
    end_time = time.time()
    stats["execution_time_seconds"] = end_time - start_time
    
    current_memory = process.memory_info().rss
    if current_memory > peak_memory:
        peak_memory = current_memory
    stats["peak_memory_usage_bytes"] = peak_memory
    
    if collect_stats:
        # Ensure the stats directory exists
        os.makedirs(os.path.dirname(stats_file_path), exist_ok=True)
        # Write statistics to a JSON file
        with open(stats_file_path, 'w') as stats_file:
            json.dump(stats, stats_file, indent=4)
    
    return stats
