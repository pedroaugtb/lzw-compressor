# main.py

import argparse
from compressor import lzw_compress
from decompressor import lzw_decompress

"""
Usage example: 
    python main.py compress input.txt compressed.lzw --test
    python main.py decompress compressed.lzw output.txt --test
"""
def main():
    parser = argparse.ArgumentParser(description='LZW Compressor and Decompressor')
    parser.add_argument('mode', choices=['compress', 'decompress'], help='Mode: compress or decompress')
    parser.add_argument('input_file', help='Input file path')
    parser.add_argument('output_file', help='Output file path')
    parser.add_argument('-b', '--bits', type=int, default=12, help='Maximum number of bits (default: 12)')
    parser.add_argument('-v', '--variable', action='store_true', help='Use variable code size')
    parser.add_argument('-t', '--test', action='store_true', help='Enable test mode to collect statistics')
    args = parser.parse_args()

    if args.mode == 'compress':
        stats = lzw_compress(
            args.input_file,
            args.output_file,
            max_bits=args.bits,
            variable_code_size=args.variable,
            collect_stats=args.test
        )
        if args.test:
            print("Compression Statistics:")
            for key, value in stats.items():
                print(f"{key}: {value}")
    elif args.mode == 'decompress':
        stats = lzw_decompress(
            args.input_file,
            args.output_file,
            max_bits=args.bits,
            variable_code_size=args.variable,
            collect_stats=args.test
        )
        if args.test:
            print("Decompression Statistics:")
            for key, value in stats.items():
                print(f"{key}: {value}")

if __name__ == '__main__':
    main()
