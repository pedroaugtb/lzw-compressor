# compressor.py

from trie import Trie
from bitwriter import BitWriter
import time
import json
import os
import psutil

def lzw_compress_static(input_file_path, output_file_path, max_bits=12, collect_stats=False, stats_file_path="stats/compression_stats4.json"):
    # Initialize the Trie and variables
    trie = Trie()
    trie.initialize_with_ascii()
    max_table_size = 2 ** max_bits  # Maximum number of codes
    string = ''
    
    # Initialize statistics
    stats = {
        "original_size_bytes": 0,
        "compressed_size_bytes": 0,
        "compression_ratio": 0.0,
        "number_of_codes": 0,
        "execution_time_seconds": 0.0,
        "dictionary_size_over_time": [],  # Added
        "peak_memory_usage_bytes": 0  # Added
    }
    
    start_time = time.time()
    
    process = psutil.Process(os.getpid())
    peak_memory = process.memory_info().rss  # Initial memory usage
    
    # Read input data and compress
    with open(input_file_path, 'rb') as input_file, open(output_file_path, 'wb') as output_file:
        data = input_file.read()
        stats["original_size_bytes"] = len(data)
        
        # Convert data to string where each byte is a character
        data = data.decode('latin1')  # 'latin1' ensures a 1:1 mapping of bytes to characters
        
        bit_writer = BitWriter(output_file)
        next_code = 256  # Start assigning codes after the initial ASCII range
        
        # Main compression loop
        for symbol in data:
            combined = string + symbol
            if trie.search(combined) is not None:
                string = combined
            else:
                if string:
                    # Output the code for string
                    code = trie.search(string)
                    bit_writer.write_bits(code, max_bits)
                    stats["number_of_codes"] += 1
                    # Record dictionary size
                    stats["dictionary_size_over_time"].append(len(trie.dictionary))
                
                if trie.next_code < max_table_size:
                    trie.insert(combined)
                
                # Record dictionary size after insertion
                stats["dictionary_size_over_time"].append(len(trie.dictionary))
                
                string = symbol
        
        # Output the code for the last string
        if string:
            code = trie.search(string)
            bit_writer.write_bits(code, max_bits)
            stats["number_of_codes"] += 1
            # Record dictionary size
            stats["dictionary_size_over_time"].append(len(trie.dictionary))
        
        bit_writer.flush()
    
    end_time = time.time()
    stats["execution_time_seconds"] = end_time - start_time
    
    # Get peak memory usage
    current_memory = process.memory_info().rss
    stats["peak_memory_usage_bytes"] = max(peak_memory, current_memory)
    
    # Calculate compressed size
    stats["compressed_size_bytes"] = os.path.getsize(output_file_path)
    
    # Calculate compression ratio
    if stats["compressed_size_bytes"] > 0:
        stats["compression_ratio"] = stats["original_size_bytes"] / stats["compressed_size_bytes"]
    else:
        stats["compression_ratio"] = 0.0
    
    if collect_stats:
        # Ensure the stats directory exists
        os.makedirs(os.path.dirname(stats_file_path), exist_ok=True)
        # Write statistics to a JSON file
        with open(stats_file_path, 'w') as stats_file:
            json.dump(stats, stats_file, indent=4)
    
    return stats

def lzw_compress_dynamic(input_file_path, output_file_path, max_bits=12, collect_stats=False, stats_file_path="stats/compression_stats4.json"):
    stats = {
        "original_size_bytes": 0,
        "compressed_size_bytes": 0,
        "compression_ratio": 0.0,
        "number_of_codes": 0,
        "execution_time_seconds": 0.0,
        "peak_memory_usage_bytes": 0,
        "dictionary_size_over_time": []  # Added
    }
    
    start_time = time.time()
    
    process = psutil.Process(os.getpid())
    peak_memory = process.memory_info().rss  # Initial memory usage
    
    with open(input_file_path, 'r', encoding='latin1') as f:
        input_data = f.read()
    stats["original_size_bytes"] = len(input_data)
    
    current_bits = 9
    max_code = (1 << current_bits) - 1
    trie = {chr(i): i for i in range(256)}
    next_code = 256
    current_string = ""
    result = []
    
    for char in input_data:
        combined_string = current_string + char
        if combined_string in trie:
            current_string = combined_string
        else:
            result.append(trie[current_string])
            if next_code <= max_code:
                trie[combined_string] = next_code
                next_code += 1
                stats["dictionary_size_over_time"].append(len(trie))  # Record dictionary size
            
            if next_code > max_code and current_bits < max_bits:
                current_bits += 1
                max_code = (1 << current_bits) - 1
            
            current_string = char
    
    if current_string:
        result.append(trie[current_string])
        stats["dictionary_size_over_time"].append(len(trie))  # Record dictionary size
    
    with open(output_file_path, 'wb') as f:
        f.write(max_bits.to_bytes(1, byteorder='big'))  # Saves the maximum bits used
        for code in result:
            f.write(code.to_bytes((max_bits + 7) // 8, byteorder='big'))
    
    print(f"Arquivo comprimido salvo em: {output_file_path}")
    
    end_time = time.time()
    stats["execution_time_seconds"] = end_time - start_time
    stats["compressed_size_bytes"] = os.path.getsize(output_file_path)
    stats["compression_ratio"] = stats["original_size_bytes"] / stats["compressed_size_bytes"] if stats["compressed_size_bytes"] > 0 else 0.0
    stats["number_of_codes"] = next_code - 256
    stats["peak_memory_usage_bytes"] = max(peak_memory, process.memory_info().rss)
    
    if collect_stats:
        with open(stats_file_path, 'w') as stats_file:
            json.dump(stats, stats_file)
    
    return stats