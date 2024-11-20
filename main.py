# main.py

import argparse
from compressor import lzw_compress_static, lzw_compress_dynamic
from decompressor import lzw_decompress_static, lzw_decompress_dynamic
import sys

"""
Usage example: 
    python3 main.py compress inputs/input.txt compressed.lzw --variable --test
    python3 main.py decompress compressed.lzw outputs/output.txt --variable --test
"""

def write_compressed_file(output_path, compressed_data, max_bits):
    with open(output_path, 'wb') as f:
        f.write(max_bits.to_bytes(1, byteorder='big'))  # Salva o número máximo de bits usado
        for code in compressed_data:
            f.write(code.to_bytes((max_bits + 7) // 8, byteorder='big'))

def main():
    parser = argparse.ArgumentParser(description='LZW Compressor and Decompressor')
    parser.add_argument('mode', choices=['compress', 'decompress'], help='Mode: compress or decompress')
    parser.add_argument('input_file', help='Input file path')
    parser.add_argument('output_file', help='Output file path')
    parser.add_argument('-b', '--bits', type=int, default=12, help='Maximum number of bits (default: 12)')
    parser.add_argument('-v', '--variable', action='store_true', help='Use variable code size (dynamic approach)')
    parser.add_argument('-t', '--test', action='store_true', help='Enable test mode to collect statistics')
    args = parser.parse_args()

    if args.mode == 'compress':
        if args.variable:
            stats = lzw_compress_dynamic(
                args.input_file,
                args.output_file,
                max_bits=args.bits,
                collect_stats=args.test
            )
            # write_compressed_file(args.output_file, results, final_bits)
        else:
            stats = lzw_compress_static(
                args.input_file,
                args.output_file,
                max_bits=args.bits,
                collect_stats=args.test
            )
        if args.test:
            print("Compression Statistics:")
            for key, value in stats.items():
                print(f"{key}: {value}")
    elif args.mode == 'decompress':
        if args.variable:
            try:
                stats = lzw_decompress_dynamic(
                    args.input_file,
                    args.output_file,
                    max_bits=args.bits,
                    collect_stats=args.test
                )
            except ValueError as e:
                print(e)
                sys.exit(1)
        else:
            try:
                stats = lzw_decompress_static(
                    args.input_file,
                    args.output_file,
                    max_bits=args.bits,
                    collect_stats=args.test
                )
            except ValueError as e:
                print(e)
                sys.exit(1)
        if args.test:
            print("Decompression Statistics:")
            for key, value in stats.items():
                print(f"{key}: {value}")

if __name__ == '__main__':
    main()