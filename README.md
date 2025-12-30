# tx-separator

Split ABN AMRO bank transaction files by month.

## Installation

```bash
# Install from source (editable mode for development)
pip install -e .

# Or install normally
pip install .
```

## Usage

```bash
# Basic usage (CSV without header)
tx-separator transactions.csv

# Excel file with header row
tx-separator transactions.xlsx --header

# CSV file with header row
tx-separator transactions.csv --header

# Specify custom output directory
tx-separator transactions.csv -o output/

# Excel input, force CSV output
tx-separator transactions.xlsx --header --output-format csv

# Verbose output
tx-separator transactions.csv -v

# Skip verification (not recommended)
tx-separator transactions.csv --skip-verify
```

## Options

| Option | Description |
|--------|-------------|
| `--header` | Input file has a header row (preserved in each output file) |
| `--output-format {csv,xlsx,auto}` | Output format (default: auto = match input) |
| `-o, --output-dir` | Output directory (default: directory named after input file) |
| `-v, --verbose` | Enable verbose output |
| `--skip-verify` | Skip verification step |

## What it does

1. Reads a transaction file (tab-delimited CSV or Excel)
2. Groups transactions by month based on the date column (column 3, YYYYMMDD format)
3. Creates separate files named `transactions_YYYY_MM.csv` (or `.xlsx`) for each month
4. If `--header` is specified, preserves the header row in each output file
5. Verifies that the output files match the original input

## Output

Files are created in the output directory:
- `transactions_2024_01.csv` (or `.xlsx`)
- `transactions_2024_02.csv` (or `.xlsx`)
- etc.
