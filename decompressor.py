# decompressor.py

from bitreader import BitReader
import time
import json
import os
import psutil
import sys

def lzw_decompress(input_file_path, output_file_path, max_bits=12, variable_code_size=False, collect_stats=False, stats_file_path="stats/decompression_stats.json"):
    # Initialize the dictionary
    dictionary = {i: chr(i) for i in range(256)}
    next_code = 256
    max_table_size = 2 ** max_bits
    
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
    
    # Open the input and output files
    with open(input_file_path, 'rb') as input_file, open(output_file_path, 'wb') as output_file:
        bit_reader = BitReader(input_file)
        stats["compressed_size_bytes"] = os.path.getsize(input_file_path)
        
        # Initialize code size
        code_size = 9 if variable_code_size else max_bits
        next_code_increase = 1 << code_size
        
        # Read the first code
        previous_code = bit_reader.read_bits(code_size)
        if previous_code is None:
            # Empty input file
            return stats
        
        string = dictionary.get(previous_code, '')
        output_file.write(string.encode('latin1'))
        
        while True:
            code = bit_reader.read_bits(code_size)
            if code is None:
                break
            
            if code in dictionary:
                entry = dictionary[code]
            elif code == next_code:
                entry = string + string[0]
            else:
                raise ValueError(f"Bad compressed code: {code}")
            
            output_file.write(entry.encode('latin1'))
            
            # Add new entry to the dictionary
            if next_code < max_table_size:
                dictionary[next_code] = string + entry[0]
                stats["dictionary_size_over_time"].append(next_code)
                next_code += 1
                
                # Adjust code size if necessary
                if variable_code_size and next_code == next_code_increase and code_size < max_bits:
                    code_size += 1
                    next_code_increase = 1 << code_size
            
            string = entry
    
    end_time = time.time()
    stats["execution_time_seconds"] = end_time - start_time
    
    # Calculate decompressed size
    stats["decompressed_size_bytes"] = os.path.getsize(output_file_path)
    
    # Get peak memory usage
    current_memory = process.memory_info().rss
    stats["peak_memory_usage_bytes"] = current_memory
    
    if collect_stats:
        # Ensure the stats directory exists
        os.makedirs(os.path.dirname(stats_file_path), exist_ok=True)
        # Write statistics to a JSON file
        with open(stats_file_path, 'w') as stats_file:
            json.dump(stats, stats_file, indent=4)
    
    return stats