# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Python utility to split combined ABN AMRO banking statements (tab-separated CSV) into separate monthly files.

## Running the Tool

**Direct Python execution:**
```bash
python3 transaction-separator.py <input_file> <output_directory>
```

**With automatic verification:**
```bash
./split-and-test.sh <input_file>
```
The shell script creates an output directory based on the input filename, runs the separator, and verifies the output matches the original by concatenating all generated files and diffing against the source.

## Architecture

- `transaction-separator.py`: Reads a tab-delimited transaction file, groups rows by month based on the date in column 3 (format: YYYYMMDD), and writes each month to `transactions_YYYY_MM.csv`
- `split-and-test.sh`: Wrapper that handles directory creation and validates output integrity

## Input Format

Tab-separated CSV where column index 2 (third column) contains the transaction date in `YYYYMMDD` format.
