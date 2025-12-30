"""Command-line interface for tx-separator."""

import argparse
import sys
from pathlib import Path

from tx_separator.separator import process_transactions
from tx_separator.verifier import verify_output


def create_output_dir(input_file: Path, custom_output_dir: Path | None) -> Path:
    """
    Create and return the output directory.

    If custom_output_dir is provided, use it. Otherwise, create a directory
    based on the input filename (without extension) in the current directory.
    """
    if custom_output_dir:
        output_dir = custom_output_dir
    else:
        # Use input file's stem (name without extension) as directory name
        output_dir = Path.cwd() / input_file.stem

    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def main() -> int:
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        prog="tx-separator",
        description="Split ABN AMRO bank transaction files by month",
        epilog="Output files are named transactions_YYYY_MM.csv (or .xlsx)",
    )
    parser.add_argument(
        "input_file",
        type=Path,
        help="Path to the input transaction file (CSV or Excel)",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        dest="output_dir",
        help="Output directory (default: directory named after input file)",
    )
    parser.add_argument(
        "--header",
        action="store_true",
        help="Input file has a header row (preserved in each output file)",
    )
    parser.add_argument(
        "--output-format",
        choices=["csv", "xlsx", "auto"],
        default="auto",
        dest="output_format",
        help="Output format: csv, xlsx, or auto to match input (default: auto)",
    )
    parser.add_argument(
        "--skip-verify",
        action="store_true",
        help="Skip verification step (not recommended)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose output",
    )

    args = parser.parse_args()

    # Resolve input file to absolute path
    input_file = args.input_file.resolve()

    # Validate input file exists
    if not input_file.exists():
        print(f"Error: Input file '{input_file}' does not exist.", file=sys.stderr)
        return 1

    if not input_file.is_file():
        print(f"Error: '{input_file}' is not a file.", file=sys.stderr)
        return 1

    # Create output directory
    output_dir = create_output_dir(input_file, args.output_dir)

    if args.verbose:
        print(f"Input file: {input_file}")
        print(f"Output directory: {output_dir}")
        print(f"Has header: {args.header}")
        print(f"Output format: {args.output_format}")

    # Process transactions
    try:
        file_counts, header = process_transactions(
            input_file,
            output_dir,
            has_header=args.header,
            output_format=args.output_format,
        )
    except Exception as e:
        print(f"Error processing transactions: {e}", file=sys.stderr)
        return 1

    total_transactions = sum(file_counts.values())
    print(f"Processed {total_transactions} transactions.")
    print(f"Created {len(file_counts)} output files in {output_dir}")

    if args.verbose:
        for filename, count in sorted(file_counts.items()):
            print(f"  {filename}: {count} transactions")

    # Verification step (always runs unless --skip-verify)
    if not args.skip_verify:
        if args.verbose:
            print("\nVerifying output...")

        success, message = verify_output(
            input_file,
            output_dir,
            has_header=args.header,
            output_format=args.output_format,
        )

        if success:
            print(f"Verification: {message}")
            return 0
        else:
            print(f"Verification FAILED: {message}", file=sys.stderr)
            return 1
    else:
        print("Warning: Verification skipped (--skip-verify)")
        return 0


if __name__ == "__main__":
    sys.exit(main())
