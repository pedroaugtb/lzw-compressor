# compressor.py

from trie import Trie
from bitwriter import BitWriter
import time
import json
import os
import psutil
import sys
import logging

# Configure logging to include DEBUG messages
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

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
        next_code = trie.next_code  # Start from trie's next_code

        logging.info(f"Initial code size: {code_size} bits")
        logging.info(f"Next code increase at: {next_code_increase}")

        # Main compression loop
        for idx, symbol in enumerate(data):
            combined = string + symbol
            if trie.search(combined) is not None:
                string = combined
                logging.debug(f"Extended string to: '{string}'")
            else:
                if string:
                    # Output the code for string
                    code = trie.search(string)
                    bit_writer.write_bits(code, code_size)
                    stats["number_of_codes"] += 1
                    logging.debug(f"Wrote code: {code} for string: '{string}' (index {idx}) with code_size: {code_size} bits")
                if trie.next_code < max_table_size:
                    trie.insert(combined)
                    # Track dictionary size over time
                    dictionary_sizes.append(trie.next_code - 1)
                    stats["dictionary_size_over_time"].append(trie.next_code - 1)
                    logging.debug(f"Added to trie: '{combined}' with code: {trie.next_code - 1}")

                    # Adjust code size if necessary
                    if variable_code_size and trie.next_code >= next_code_increase and code_size < max_bits:
                        code_size += 1
                        next_code_increase = 1 << code_size
                        logging.info(f"Code size increased to {code_size} bits")
                        logging.info(f"Next code increase at: {next_code_increase}")
                string = symbol
                logging.debug(f"Reset string to: '{string}'")

            # Update peak memory usage
            current_memory = process.memory_info().rss
            if current_memory > peak_memory:
                peak_memory = current_memory
                logging.debug(f"Updated peak memory usage: {peak_memory} bytes")

        # Output the code for the last string
        if string:
            code = trie.search(string)
            bit_writer.write_bits(code, code_size)
            stats["number_of_codes"] += 1
            logging.debug(f"Wrote final code: {code} for string: '{string}' with code_size: {code_size} bits")

        bit_writer.flush()
        logging.info("Bit writing flushed")

    end_time = time.time()
    stats["execution_time_seconds"] = end_time - start_time

    # Calculate compressed size
    stats["compressed_size_bytes"] = os.path.getsize(output_file_path)
    logging.debug(f"Compressed size: {stats['compressed_size_bytes']} bytes")

    # Calculate compression ratio
    if stats["compressed_size_bytes"] > 0:
        stats["compression_ratio"] = stats["original_size_bytes"] / stats["compressed_size_bytes"]
    else:
        stats["compression_ratio"] = 0.0
    logging.debug(f"Compression ratio: {stats['compression_ratio']}")

    # Get peak memory usage
    stats["peak_memory_usage_bytes"] = peak_memory
    logging.debug(f"Peak memory usage during compression: {peak_memory} bytes")

    logging.info(f"Compression completed in {stats['execution_time_seconds']} seconds")
    logging.info(f"Original size: {stats['original_size_bytes']} bytes")
    logging.info(f"Compressed size: {stats['compressed_size_bytes']} bytes")
    logging.info(f"Compression ratio: {stats['compression_ratio']}")
    logging.info(f"Peak memory usage: {stats['peak_memory_usage_bytes']} bytes")

    if collect_stats:
        # Ensure the stats directory exists
        os.makedirs(os.path.dirname(stats_file_path), exist_ok=True)
        # Write statistics to a JSON file
        with open(stats_file_path, 'w') as stats_file:
            json.dump(stats, stats_file, indent=4)
        logging.info(f"Statistics written to {stats_file_path}")

    return stats