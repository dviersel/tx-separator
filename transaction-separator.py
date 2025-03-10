import csv
from datetime import datetime
import os
import sys

def parse_date(date_str):
    return datetime.strptime(date_str, '%Y%m%d')

def get_output_filename(date):
    return f"transactions_{date.strftime('%Y_%m')}.csv"

def process_transactions(input_file):
    global results_dir
    # Dictionary to store transactions for each month
    monthly_transactions = {}

    with open(input_file, 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            # Assuming the date is in the 3rd column (index 2)
            transaction_date = parse_date(row[2])
            output_file = get_output_filename(transaction_date)
            
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
    if len(sys.argv) != 3:
        print("Usage: python script_name.py <path_to_input_file> <path_to_output_directory>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    results_dir = sys.argv[2]
    
    if not os.path.exists(input_file):
        print(f"Error: The file '{input_file}' does not exist.")
        sys.exit(1)

    if not os.path.exists(results_dir):
        print(f"Error: The directory '{results_dir}' does not exist.")
        sys.exit(1)
    
    process_transactions(input_file)
