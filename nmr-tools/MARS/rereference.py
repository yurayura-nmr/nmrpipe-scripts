#!/usr/bin/env python3
"""
Apply nucleus-specific referencing shifts to a MARS chemical shift table.
Usage: python apply_reference_shift.py input.tab output.tab --offsets N=0.5 HN=0.02 CA=-0.3 ...
"""

import argparse
import re
import sys

def main():
    parser = argparse.ArgumentParser(description='Apply referencing shifts to MARS chemical shift file.')
    parser.add_argument('input', help='Input .tab file')
    parser.add_argument('output', help='Output .tab file')
    parser.add_argument('--offsets', nargs='+', required=True,
                        help='Offsets in format NUCLEUS=value e.g. N=0.5 HN=0.02 CA=-0.3')
    args = parser.parse_args()

    # Parse offsets into a dictionary
    offset_dict = {}
    for item in args.offsets:
        if '=' not in item:
            sys.stderr.write(f"Warning: skipping invalid offset '{item}'. Use NUCLEUS=value.\n")
            continue
        nucleus, val = item.split('=', 1)
        try:
            offset_dict[nucleus.strip()] = float(val)
        except ValueError:
            sys.stderr.write(f"Warning: invalid number for {nucleus}: {val}\n")

    if not offset_dict:
        sys.stderr.write("No valid offsets provided. Exiting.\n")
        sys.exit(1)

    with open(args.input, 'r') as fin, open(args.output, 'w') as fout:
        lines = fin.readlines()
        if not lines:
            return

        # Find the first non‑comment line (the header)
        header_idx = 0
        for i, line in enumerate(lines):
            if line.strip() and not line.startswith('#'):
                header_idx = i
                break
        else:
            sys.stderr.write("No header line found.\n")
            sys.exit(1)

        # Process header: split into column names
        header_line = lines[header_idx]
        # Use whitespace split, but preserve the exact whitespace for output?
        # We'll reconstruct with tabs for simplicity, but better to keep original format.
        # Let's split on whitespace and store columns.
        cols = re.split(r'\s+', header_line.strip())
        # The first column is the pseudoresidue column (no header), but in the file it's present.
        # Actually, in MARS files, the first column has no header name (it's the PR ID column).
        # So cols[0] is the first shift type? Wait, the header line lists only the shift types,
        # and the first column (PR ID) has no header. So when we split, cols[0] is the first shift type.
        # Example: "N HN CA CB CO CO-1 CA-1 CB-1"
        # That means the data lines have: <PR_name> <N> <HN> ...
        # So we need to map each shift column to its nucleus name.
        # We'll create a list of column names as they appear (without the PR column).
        col_names = cols  # these are the shift types

        # Write the header unchanged (we keep it exactly as is)
        # But we need to ensure we write it back without modifying.
        fout.write(lines[header_idx])

        # Now process data lines after header
        for line in lines[header_idx+1:]:
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                # comment or empty line: write unchanged
                fout.write(line)
                continue

            # Split data line into fields (preserving whitespace? easier to split and rejoin with tabs)
            fields = re.split(r'\s+', stripped)
            if len(fields) < len(col_names) + 1:
                # Not enough fields: maybe the line is malformed; copy as is
                sys.stderr.write(f"Warning: line has fewer fields than header: {line}")
                fout.write(line)
                continue

            # First field is pseudoresidue name
            pr_name = fields[0]
            # Following fields are the shifts in the order of col_names
            new_fields = [pr_name]
            for j, shift_val in enumerate(fields[1:]):
                if j >= len(col_names):
                    break
                nucleus = col_names[j]
                if shift_val != '-' and shift_val.strip() != '':
                    try:
                        old = float(shift_val)
                        # Apply offset if defined for this nucleus
                        if nucleus in offset_dict:
                            new_val = old + offset_dict[nucleus]
                            # Format with appropriate precision (e.g., keep same decimal places?)
                            # Simple: convert back to string with 3-6 decimal places.
                            # We'll just use repr or format with 6 decimals.
                            new_fields.append(f"{new_val:.6f}".rstrip('0').rstrip('.'))
                        else:
                            new_fields.append(shift_val)  # unchanged
                    except ValueError:
                        # Not a number, keep as is (shouldn't happen)
                        new_fields.append(shift_val)
                else:
                    new_fields.append(shift_val)

            # Reconstruct line with original whitespace? We'll join with a tab.
            # To preserve original spacing, we'd need to use regex replacement, but simpler:
            fout.write("\t".join(new_fields) + "\n")

    print(f"Applied offsets {offset_dict} to {args.input}. Output written to {args.output}")

if __name__ == '__main__':
    main()
