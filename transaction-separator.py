import csv
from datetime import datetime
import os
import sys

def parse_date(date_str):
    return datetime.strptime(date_str, '%Y%m%d')

def get_output_filename(date):
    return f"transactions_{date.strftime('%Y_%m')}.csv"

def process_transactions(input_file):
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
        with open(output_file, 'w', newline='') as file:
            writer = csv.writer(file, delimiter='\t')
            writer.writerows(transactions)

    print(f"Processed {sum(len(trans) for trans in monthly_transactions.values())} transactions.")
    print(f"Created {len(monthly_transactions)} output files.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <path_to_input_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    if not os.path.exists(input_file):
        print(f"Error: The file '{input_file}' does not exist.")
        sys.exit(1)
    
    process_transactions(input_file)
