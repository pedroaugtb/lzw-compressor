# process_stats.py

import json
import os
import argparse
import matplotlib.pyplot as plt
import pandas as pd

def load_stats(stats_file_path):
    with open(stats_file_path, 'r') as f:
        return json.load(f)

def plot_compression_ratio(stats, output_dir):
    plt.figure(figsize=(10, 6))
    plt.plot(range(len(stats['dictionary_size_over_time'])), stats['dictionary_size_over_time'], label='Dictionary Size')
    plt.xlabel('Number of Codes')
    plt.ylabel('Dictionary Size')
    plt.title('Dictionary Growth Over Time')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(output_dir, 'dictionary_growth.png'))
    plt.close()

def plot_compression_ratio_ratio(stats, output_dir):
    plt.figure(figsize=(6, 6))
    plt.bar(['Original Size', 'Compressed Size'], [stats['original_size_bytes'], stats['compressed_size_bytes']], color=['blue', 'orange'])
    plt.ylabel('Size (bytes)')
    plt.title(f"Compression Ratio: {stats['compression_ratio']:.2f}")
    plt.savefig(os.path.join(output_dir, 'compression_ratio.png'))
    plt.close()

"""
Usage example:
    python process_stats.py stats/compression_stats.json --output_dir reports/compression_reports
"""
def main():
    parser = argparse.ArgumentParser(description='Process LZW Compression/Decompression Statistics')
    parser.add_argument('stats_file', help='Path to the statistics JSON file')
    parser.add_argument('-o', '--output_dir', default='reports', help='Directory to save the reports (default: reports)')
    args = parser.parse_args()

    stats = load_stats(args.stats_file)

    # Ensure the output directory exists
    os.makedirs(args.output_dir, exist_ok=True)

    # Generate Dictionary Growth Plot
    if 'dictionary_size_over_time' in stats:
        plot_compression_ratio(stats, args.output_dir)

    # Generate Compression Ratio Plot
    if 'compression_ratio' in stats and 'original_size_bytes' in stats and 'compressed_size_bytes' in stats:
        plot_compression_ratio_ratio(stats, args.output_dir)

    # Save Statistics as a CSV (optional)
    df = pd.DataFrame.from_dict(stats, orient='index').transpose()
    df.to_csv(os.path.join(args.output_dir, 'stats_summary.csv'), index=False)

    print(f"Reports generated in '{args.output_dir}' directory.")

if __name__ == '__main__':
    main()
