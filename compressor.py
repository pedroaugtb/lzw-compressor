# compressor.py

from trie import Trie
from bitwriter import BitWriter
import time
import json
import os
import psutil
import sys

def lzw_compress(input_file_path, output_file_path, max_bits=12, variable_code_size=False, collect_stats=False, stats_file_path="stats/compression_stats.json"):
    # Initialize the Trie and variables
    trie = Trie()
    trie.initialize_with_ascii()
    max_table_size = 2 ** max_bits  # Maximum number of codes
    string = ''
    dictionary_sizes = []
    
    # Initialize statistics
    stats = {
        "original_size_bytes": 0,
        "compressed_size_bytes": 0,
        "compression_ratio": 0.0,
        "number_of_codes": 0,
        "dictionary_size_over_time": [],
        "execution_time_seconds": 0.0,
        "peak_memory_usage_bytes": 0  # Optional
    }
    
    start_time = time.time()
    
    process = psutil.Process(os.getpid())
    peak_memory = 0
    
    # Read input data and compress
    with open(input_file_path, 'rb') as input_file, open(output_file_path, 'wb') as output_file:
        data = input_file.read()
        stats["original_size_bytes"] = len(data)
        
        # Convert data to string where each byte is a character
        data = data.decode('latin1')  # 'latin1' ensures a 1:1 mapping of bytes to characters
        
        bit_writer = BitWriter(output_file)
        code_size = 9 if variable_code_size else max_bits
        next_code_increase = 1 << code_size
        next_code = 256
        
        # Main compression loop
        for symbol in data:
            combined = string + symbol
            if trie.search(combined) is not None:
                string = combined
            else:
                if string:
                    # Output the code for string
                    code = trie.search(string)
                    bit_writer.write_bits(code, code_size)
                    stats["number_of_codes"] += 1
                if trie.next_code < max_table_size:
                    trie.insert(combined)
                    # Track dictionary size over time
                    dictionary_sizes.append(trie.next_code)
                    stats["dictionary_size_over_time"].append(trie.next_code)
                    
                    next_code += 1
                    if variable_code_size and next_code == next_code_increase and code_size < max_bits:
                        code_size += 1
                        next_code_increase = 1 << code_size
                string = symbol
        
        # Output the code for the last string
        if string:
            code = trie.search(string)
            bit_writer.write_bits(code, code_size)
            stats["number_of_codes"] += 1
        
        bit_writer.flush()
    
    end_time = time.time()
    stats["execution_time_seconds"] = end_time - start_time
    
    # Calculate compressed size
    stats["compressed_size_bytes"] = os.path.getsize(output_file_path)
    
    # Calculate compression ratio
    if stats["compressed_size_bytes"] > 0:
        stats["compression_ratio"] = stats["original_size_bytes"] / stats["compressed_size_bytes"]
    else:
        stats["compression_ratio"] = 0.0
    
    # Get peak memory usage
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