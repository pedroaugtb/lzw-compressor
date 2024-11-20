import time
import json
import os
import sys


def lzw_decompress(
    input_file_path,
    output_file_path,
    max_bits=12,
    collect_stats=False,
    stats_file_path="stats/decompression_stats.json",
    use_variable=False,
):
    """
    Decompresses a file compressed using the LZW algorithm.

    This function implements both static and dynamic versions of the LZW decompression
    algorithm based on the value of `use_variable`. It reads a compressed input file,
    decompresses its content, and writes the decompressed data to an output file. Optionally,
    it collects and saves decompression statistics.

    Args:
        input_file_path (str): Path to the compressed input file.
        output_file_path (str): Path to save the decompressed output file.
        max_bits (int, optional): Maximum number of bits used for encoding (default: 12).
        collect_stats (bool, optional): If True, collects and saves decompression statistics (default: False).
        stats_file_path (str, optional): Path to save the statistics file (default: "stats/decompression_stats.json").
        use_variable (bool, optional): If True, enables dynamic code size mode; otherwise, uses static mode (default: False).

    Returns:
        dict: A dictionary containing decompression statistics, including:
            - compressed_size_bytes (int): Size of the compressed input file in bytes.
            - decompressed_size_bytes (int): Size of the decompressed output file in bytes.
            - compression_ratio (float): Ratio of decompressed size to compressed size.
            - number_of_codes (int): Total number of codes processed during decompression.
            - execution_time_seconds (float): Time taken to decompress the file in seconds.

    Raises:
        ValueError: If an invalid code is encountered during decompression.
        FileNotFoundError: If the input file does not exist.
        IOError: If an error occurs while reading or writing files.
    """
    stats = {
        "compressed_size_bytes": 0,
        "decompressed_size_bytes": 0,
        "compression_ratio": 0.0,
        "number_of_codes": 0,
        "execution_time_seconds": 0.0,
    }

    start_time = time.time()

    # Read the compressed file
    with open(input_file_path, "rb") as f:
        max_bits = int.from_bytes(
            f.read(1), byteorder="big"
        )  # Read the maximum number of bits
        code_size = (max_bits + 7) // 8
        compressed_data = []
        while chunk := f.read(code_size):
            compressed_data.append(int.from_bytes(chunk, byteorder="big"))
    stats["compressed_size_bytes"] = os.path.getsize(input_file_path)

    # Initialize the dictionary with ASCII characters
    dictionary = {i: chr(i) for i in range(256)}
    next_code = 256

    curr_bits = 9  # Initial code size in bits
    max_code = (1 << curr_bits) - 1  # Maximum code for the current bit size
    result = []

    # Decompression logic
    prev_code = compressed_data[0]
    if prev_code not in dictionary:
        raise ValueError("Invalid code encountered during decompression.")
    curr_string = dictionary[prev_code]
    result.append(curr_string)

    for code in compressed_data[1:]:
        if code in dictionary:
            entry = dictionary[code]
        elif code == next_code:
            entry = curr_string + curr_string[0]
        else:
            raise ValueError("Invalid code encountered during decompression.")

        result.append(entry)

        # Add a new entry to the dictionary
        if next_code <= max_code:
            dictionary[next_code] = curr_string + entry[0]
            next_code += 1

        # Update the number of bits if in dynamic mode
        if use_variable and next_code > max_code and curr_bits < max_bits:
            curr_bits += 1
            max_code = (1 << curr_bits) - 1

        curr_string = entry

    # Write the decompressed result to the output file
    with open(output_file_path, "w", encoding="latin1") as f:
        f.write("".join(result))

    end_time = time.time()
    stats["execution_time_seconds"] = end_time - start_time

    # Calculate decompressed file size
    stats["decompressed_size_bytes"] = os.path.getsize(output_file_path)

    # Calculate compression ratio
    if stats["decompressed_size_bytes"] > 0:
        stats["compression_ratio"] = (
            stats["decompressed_size_bytes"] / stats["compressed_size_bytes"]
        )
    else:
        stats["compression_ratio"] = 0.0

    # Save statistics if requested
    if collect_stats:
        os.makedirs(os.path.dirname(stats_file_path), exist_ok=True)
        with open(stats_file_path, "w") as stats_file:
            json.dump(stats, stats_file, indent=4)

    print(f"Decompressed file saved to: {output_file_path}")
    return stats