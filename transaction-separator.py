import argparse
import csv
from datetime import datetime
import os
import sys

def parse_date(date_str):
    return datetime.strptime(date_str, '%Y%m%d')

def get_output_filename(date, ext):
    return f"transactions_{date.strftime('%Y_%m')}.{ext}"

def process_transactions(input_file, results_dir, ext):
    # Dictionary to store transactions for each month
    monthly_transactions = {}

    with open(input_file, 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            # Assuming the date is in the 3rd column (index 2)
            transaction_date = parse_date(row[2])
            output_file = get_output_filename(transaction_date, ext)
            
            if output_file not in monthly_transactions:
                monthly_transactions[output_file] = []
            
            monthly_transactions[output_file].append(row)

    # Write transactions to separate files
    for output_file, transactions in monthly_transactions.items():
        full_output_path = os.path.join(results_dir, output_file)
        with open(full_output_path, 'w', newline='') as file:
            writer = csv.writer(file, delimiter='\t')
            writer.writerows(transactions)

    print(f"Processed {sum(len(trans) for trans in monthly_transactions.values())} transactions.")
    print(f"Created {len(monthly_transactions)} output files.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Split combined banking statements into separate monthly files."
    )
    parser.add_argument("input_file", help="Path to the input transaction file")
    parser.add_argument(
        "output_dir",
        nargs="?",
        help="Path to the output directory (default: folder named after input file)"
    )
    parser.add_argument(
        "--ext", "-e",
        default="csv",
        help="Output file extension (default: csv)"
    )
    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        print(f"Error: The file '{args.input_file}' does not exist.")
        sys.exit(1)

    output_dir = args.output_dir
    if output_dir is None:
        # Create directory named after input file (without extension)
        base_name = os.path.splitext(os.path.basename(args.input_file))[0]
        output_dir = os.path.join(os.path.dirname(args.input_file) or ".", base_name)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    process_transactions(args.input_file, output_dir, args.ext)
