from trie import Trie
import time
import json
import os


def lzw_compress(
    input_file_path,
    output_file_path,
    max_bits=12,
    collect_stats=False,
    stats_file_path="stats/compression_stats.json",
    use_variable=False,
):
    """
    Compresses a file using the LZW algorithm.

    This function implements both static and dynamic versions of the LZW algorithm
    based on the value of `use_variable`. The function reads an input file, compresses
    its content, and writes the compressed data to an output file. Optionally, it can
    collect and save compression statistics.

    Args:
        input_file_path (str): Path to the input file to be compressed.
        output_file_path (str): Path to the output file where compressed data will be saved.
        max_bits (int, optional): Maximum number of bits for encoding (default: 12).
        collect_stats (bool, optional): If True, collects and saves compression statistics (default: False).
        stats_file_path (str, optional): Path to save the statistics file (default: "stats/compression_stats.json").
        use_variable (bool, optional): If True, enables dynamic code size mode; otherwise, uses static mode (default: False).

    Returns:
        dict: A dictionary containing compression statistics, including:
            - original_size_bytes (int): Size of the original input file in bytes.
            - compressed_size_bytes (int): Size of the compressed output file in bytes.
            - compression_ratio (float): Ratio of original size to compressed size.
            - number_of_codes (int): Total number of codes generated during compression.
            - execution_time_seconds (float): Time taken to compress the file in seconds.

    Raises:
        FileNotFoundError: If the input file does not exist.
        IOError: If an error occurs while reading or writing files.
    """
    stats = {
        "original_size_bytes": 0,
        "compressed_size_bytes": 0,
        "compression_ratio": 0.0,
        "number_of_codes": 0,
        "execution_time_seconds": 0.0,
    }

    start_time = time.time()

    # Initialize the Trie with ASCII characters
    trie = Trie()
    trie.initialize_with_ascii()

    # Read the input file
    with open(input_file_path, "r", encoding="latin1") as f:
        data = f.read()
    stats["original_size_bytes"] = len(data)

    curr_string = ""
    result = []

    # Dynamic approach
    if use_variable:
        curr_bits = 9  # Initial code size in bits
        max_code = (1 << curr_bits) - 1  # Maximum code value for current bit size
        next_code = 256  # Start inserting new codes from 256 onward

        for symbol in data:
            combined_string = curr_string + symbol
            if trie.search(combined_string) is not None:
                curr_string = combined_string
            else:
                result.append(trie.search(curr_string))
                stats["number_of_codes"] += 1

                if next_code <= max_code:
                    trie.insert(combined_string)
                    next_code += 1

                # Increase code size dynamically if max_code is exceeded
                if next_code > max_code and curr_bits < max_bits:
                    curr_bits += 1
                    max_code = (1 << curr_bits) - 1

                curr_string = symbol

        # Append the last code
        if curr_string:
            result.append(trie.search(curr_string))
            stats["number_of_codes"] += 1

    # Static approach
    else:
        max_table_size = 2**max_bits  # Maximum number of codes
        next_code = 256  # Start inserting new codes from 256 onward

        for symbol in data:
            combined_string = curr_string + symbol
            if trie.search(combined_string) is not None:
                curr_string = combined_string
            else:
                if curr_string:
                    result.append(trie.search(curr_string))
                    stats["number_of_codes"] += 1
                if trie.next_code < max_table_size:
                    trie.insert(combined_string)
                curr_string = symbol

        # Append the last code
        if curr_string:
            result.append(trie.search(curr_string))
            stats["number_of_codes"] += 1

    # Write the compressed data to the output file
    with open(output_file_path, "wb") as f:
        f.write(max_bits.to_bytes(1, byteorder="big"))  # Save max_bits as the first byte
        for code in result:
            f.write(code.to_bytes((max_bits + 7) // 8, byteorder="big"))

    end_time = time.time()
    stats["execution_time_seconds"] = end_time - start_time
    stats["compressed_size_bytes"] = os.path.getsize(output_file_path)
    stats["compression_ratio"] = (
        stats["original_size_bytes"] / stats["compressed_size_bytes"]
        if stats["compressed_size_bytes"] > 0
        else 0.0
    )

    # Save statistics if requested
    if collect_stats:
        os.makedirs(os.path.dirname(stats_file_path), exist_ok=True)
        with open(stats_file_path, "w") as stats_file:
            json.dump(stats, stats_file, indent=4)

    return stats