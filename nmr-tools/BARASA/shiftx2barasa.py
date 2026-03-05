#!/usr/bin/env python3
"""
Convert SHIFTX2 output to BARASA predicted chemical shift file format.

Usage:
    shiftx2barasa.py input.txt output.txt [CA_err CB_err CO_err N_err H_err]

Default errors (from SHIFTX2, 2011):
    CA_err = 0.4412, CB_err = 0.5163, CO_err = 0.5330,
    N_err  = 1.1169, H_err  = 0.1711
"""

import argparse
import sys
import os

# Default errors from SHIFTX2 (RMS errors reported in the paper)
DEFAULT_ERRORS = {
    'CA': 0.4412,
    'CB': 0.5163,
    'CO': 0.5330,
    'N': 1.1169,
    'H': 0.1711
}

def parse_shiftx(input_file):
    """
    Parse SHIFTX2 output file.
    Returns list of tuples: (num, res, ca, cb, co, n, h)
    where missing values are represented as None.
    """
    if not os.path.isfile(input_file):
        print(f"Error: Input file '{input_file}' not found.", file=sys.stderr)
        sys.exit(1)

    data = []
    with open(input_file, 'r') as f:
        lines = f.readlines()

    # Find start of data (after the dashed line)
    start_idx = None
    for i, line in enumerate(lines):
        if line.strip().startswith('---'):
            start_idx = i + 1
            break

    if start_idx is None:
        print("Error: Could not find data section (no dashed line).", file=sys.stderr)
        sys.exit(1)

    for line in lines[start_idx:]:
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) < 8:
            print(f"Skipping malformed line: {line}", file=sys.stderr)
            continue

        num = parts[0]
        res = parts[1]
        # HA is parts[2] – ignored
        h_str = parts[3]
        n_str = parts[4]
        ca_str = parts[5]
        cb_str = parts[6]
        co_str = parts[7]

        # Convert to float to detect zero (missing)
        def clean(value_str):
            try:
                val = float(value_str)
                if abs(val) < 1e-6:  # treat as missing
                    return None
                return value_str  # keep original formatting
            except ValueError:
                return None

        data.append((
            num,
            res,
            clean(ca_str),
            clean(cb_str),
            clean(co_str),
            clean(n_str),
            clean(h_str)
        ))

    return data

def write_barasa_pred(output_file, data, errors):
    """
    Write BARASA predicted shift file.
    errors: dict with keys 'CA','CB','CO','N','H'
    """
    with open(output_file, 'w') as f:
        # Header
        header = ['Num', 'RES', 'CA', 'CA_err', 'CB', 'CB_err',
                  'CO', 'CO_err', 'N', 'N_err', 'H', 'H_err']
        f.write('\t'.join(header) + '\n')

        for num, res, ca, cb, co, n, h in data:
            # Build row, using '-' for missing values
            row = [
                num,
                res,
                ca if ca is not None else '-',
                str(errors['CA']),
                cb if cb is not None else '-',
                str(errors['CB']),
                co if co is not None else '-',
                str(errors['CO']),
                n if n is not None else '-',
                str(errors['N']),
                h if h is not None else '-',
                str(errors['H'])
            ]
            f.write('\t'.join(row) + '\n')

def main():
    parser = argparse.ArgumentParser(
        description="Convert SHIFTX2 output to BARASA predicted shifts."
    )
    parser.add_argument("input", help="Input SHIFTX2 file")
    parser.add_argument("output", help="Output BARASA file")
    parser.add_argument("errors", nargs='*', type=float,
                        metavar="CA_err CB_err CO_err N_err H_err",
                        help="Override default errors (provide all five if used)")

    args = parser.parse_args()

    # Validate errors
    if args.errors:
        if len(args.errors) != 5:
            print("Error: You must provide either zero or exactly five error values.",
                  file=sys.stderr)
            sys.exit(1)
        errors = dict(zip(['CA', 'CB', 'CO', 'N', 'H'], args.errors))
    else:
        errors = DEFAULT_ERRORS
        print(f"Using default SHIFTX2 errors: {errors}", file=sys.stderr)

    data = parse_shiftx(args.input)
    if not data:
        print("No data found. Please check input format.", file=sys.stderr)
        sys.exit(1)

    write_barasa_pred(args.output, data, errors)
    print(f"Converted {len(data)} residues to {args.output}")

if __name__ == "__main__":
    main()
