import argparse
from compressor import lzw_compress
from decompressor import lzw_decompress
import sys

"""
Main module for running the LZW Compressor and Decompressor.

This script provides a command-line interface for compressing and decompressing files
using the LZW algorithm. It supports options for variable code size, test mode for
collecting statistics, and custom maximum bit sizes.

Usage example:
    python3 main.py compress inputs/input.txt compressed.lzw --variable --test
    python3 main.py decompress compressed.lzw outputs/output.txt --variable --test
"""


def write_compressed_file(output_path, compressed_data, max_bits):
    """
    Writes compressed data to a binary file.

    Args:
        output_path (str): Path to the output file.
        compressed_data (list[int]): List of compressed codes.
        max_bits (int): Maximum number of bits used for encoding.

    The file format starts with the `max_bits` encoded in 1 byte, followed
    by the compressed data encoded with the corresponding number of bits.
    """
    with open(output_path, "wb") as f:
        f.write(
            max_bits.to_bytes(1, byteorder="big")
        )  # Salva o número máximo de bits usado
        for code in compressed_data:
            f.write(code.to_bytes((max_bits + 7) // 8, byteorder="big"))


def main():
    """
    Main function for handling command-line arguments and running the LZW compressor or decompressor.

    Parses command-line arguments to determine the mode (compress or decompress),
    input and output file paths, and optional parameters such as maximum bits, variable
    code size, and test mode.

    Command-line arguments:
        mode (str): "compress" or "decompress".
        input_file (str): Path to the input file.
        output_file (str): Path to the output file.
        -b, --bits (int, optional): Maximum number of bits (default is 12).
        -v, --variable (bool, optional): Enable variable code size.
        -t, --test (bool, optional): Enable test mode for collecting statistics.

    Calls `lzw_compress` or `lzw_decompress` based on the mode and handles any exceptions during decompression.

    Prints statistics if test mode is enabled.
    """
    parser = argparse.ArgumentParser(description="LZW Compressor and Decompressor")
    parser.add_argument(
        "mode", choices=["compress", "decompress"], help="Mode: compress or decompress"
    )
    parser.add_argument("input_file", help="Input file path")
    parser.add_argument("output_file", help="Output file path")
    parser.add_argument(
        "-b",
        "--bits",
        type=int,
        default=12,
        help="Maximum number of bits (default: 12)",
    )
    parser.add_argument(
        "-v",
        "--variable",
        action="store_true",
        help="Use variable code size (dynamic approach)",
    )
    parser.add_argument(
        "-t",
        "--test",
        action="store_true",
        help="Enable test mode to collect statistics",
    )
    args = parser.parse_args()

    if args.mode == "compress":
        stats = lzw_compress(
            args.input_file,
            args.output_file,
            max_bits=args.bits,
            collect_stats=args.test,
            use_variable=args.variable,
        )
        if args.test:
            print("Compression Statistics:")
            for key, value in stats.items():
                print(f"{key}: {value}")

    if args.mode == "decompress":
        try:
            stats = lzw_decompress(
                args.input_file,
                args.output_file,
                max_bits=args.bits,
                collect_stats=args.test,
                use_variable=args.variable,
            )
        except ValueError as e:
            print(e)
            sys.exit(1)

        if args.test:
            print("Decompression Statistics:")
            for key, value in stats.items():
                print(f"{key}: {value}")


if __name__ == "__main__":
    main()
