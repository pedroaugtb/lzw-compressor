# decompressor.py

from bitreader import BitReader
import time
import json
import os
import psutil
import sys
import logging

# Configure logging to include DEBUG messages
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def lzw_decompress(input_file_path, output_file_path, max_bits=12, variable_code_size=False, collect_stats=False, stats_file_path="stats/decompression_stats.json"):
    # Initialize the dictionary with single-byte entries
    dictionary = {i: chr(i) for i in range(256)}
    next_code = 256
    max_table_size = 2 ** max_bits

    # Initialize statistics
    stats = {
        "compressed_size_bytes": 0,
        "decompressed_size_bytes": 0,
        "execution_time_seconds": 0.0,
        "dictionary_size_over_time": [],
        "peak_memory_usage_bytes": 0
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

        logging.info(f"Initial code size: {code_size} bits")
        logging.info(f"Next code increase at: {next_code_increase}")

        # Read the first code
        previous_code = bit_reader.read_bits(code_size)
        if previous_code is None:
            logging.warning("Input file is empty.")
            return stats

        if previous_code not in dictionary:
            logging.error(f"First code {previous_code} not found in dictionary.")
            raise ValueError(f"Bad compressed code: {previous_code}")

        string = dictionary[previous_code]
        output_file.write(string.encode('latin1'))
        logging.debug(f"Write initial string: '{string}' with code: {previous_code}")

        while True:
            # Update peak memory usage
            current_memory = process.memory_info().rss
            if current_memory > peak_memory:
                peak_memory = current_memory
                logging.debug(f"Updated peak memory usage: {peak_memory} bytes")

            code = bit_reader.read_bits(code_size)
            if code is None:
                logging.info("Reached end of compressed file.")
                break

            logging.debug(f"Read code: {code} with current code size: {code_size} bits")

            if code in dictionary:
                entry = dictionary[code]
                logging.debug(f"Code {code} found in dictionary: '{entry}'")
            elif code == next_code:
                entry = string + string[0]
                logging.debug(f"Special case encountered. Creating entry: '{entry}'")
            else:
                logging.error(f"Bad compressed code: {code}")
                logging.error(f"Current string: '{string}'")
                logging.error(f"Next code to assign: {next_code}")
                logging.error(f"Current code size: {code_size} bits")
                logging.error(f"Next code increase at: {next_code_increase}")
                raise ValueError(f"Bad compressed code: {code}")

            output_file.write(entry.encode('latin1'))
            logging.debug(f"Write string: '{entry}'")

            # Add new entry to the dictionary
            if next_code < max_table_size:
                new_entry = string + entry[0]
                dictionary[next_code] = new_entry
                stats["dictionary_size_over_time"].append(next_code)
                logging.debug(f"Added to dictionary: {next_code} -> '{new_entry}'")
                next_code += 1
                logging.debug(f"Next code to assign: {next_code}")

                # Adjust code size if necessary
                if variable_code_size and next_code >= next_code_increase and code_size < max_bits:
                    code_size += 1
                    next_code_increase = 1 << code_size
                    logging.info(f"Code size increased to {code_size} bits")
                    logging.info(f"Next code increase at: {next_code_increase}")

            else:
                logging.debug("Reached maximum table size. No more dictionary entries will be added.")

            string = entry
            logging.debug(f"Set string to: '{string}'")

    end_time = time.time()
    stats["execution_time_seconds"] = end_time - start_time

    # Calculate decompressed size
    stats["decompressed_size_bytes"] = os.path.getsize(output_file_path)
    logging.debug(f"Decompressed size: {stats['decompressed_size_bytes']} bytes")

    # Get peak memory usage
    stats["peak_memory_usage_bytes"] = peak_memory
    logging.debug(f"Peak memory usage during decompression: {peak_memory} bytes")

    if collect_stats:
        os.makedirs(os.path.dirname(stats_file_path), exist_ok=True)
        with open(stats_file_path, 'w') as stats_file:
            json.dump(stats, stats_file, indent=4)
        logging.info(f"Statistics written to {stats_file_path}")

    logging.info(f"Decompression completed in {stats['execution_time_seconds']} seconds")
    logging.info(f"Compressed size: {stats['compressed_size_bytes']} bytes")
    logging.info(f"Decompressed size: {stats['decompressed_size_bytes']} bytes")
    logging.info(f"Peak memory usage: {stats['peak_memory_usage_bytes']} bytes")

    return stats