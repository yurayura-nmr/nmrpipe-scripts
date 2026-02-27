#!/usr/bin/env python3
"""
Apply hardcoded referencing offsets to a MARS chemical shift file.
Offsets are defined for carbon, proton, and nitrogen based on provided old/new values.
Compatible with Python 3.2+.
"""

import sys
import re

# Hardcoded offsets (new_referenced - old_before_referencing)
CARBON_DELTA = 24.9789 - 25.1930     # -0.2141 (measured by e.g., referencing a HNCACB spectrum with respect to DSS)
PROTON_DELTA = 7.1322 - 7.2792       # -0.1470 (measured by e.g., referencing a 1H/15N HSQC spectrum with respect to DSS)
NITROGEN_DELTA = 124.2821 - 124.42   # -0.1379 (measured by e.g., referencing a 1H/15N HSQC spectrum with respect to DSS)

def apply_offset(value, nucleus):
    """Apply appropriate offset to value string, return modified string."""
    try:
        val = float(value)
    except ValueError:
        return value  # keep as is (e.g., '-')
    if nucleus.startswith('C'):  # carbon column (CA, CB, CO, ...)
        new_val = val + CARBON_DELTA
    elif nucleus.startswith('H'):  # proton column (HN, HA, H, ...)
        new_val = val + PROTON_DELTA
    elif nucleus == 'N':
        new_val = val + NITROGEN_DELTA
    else:
        new_val = val  # no offset for other types
    # Format with 4 decimal places (adjust if needed) – compatible with older Python
    formatted = "{:.4f}".format(new_val).rstrip('0').rstrip('.')
    return formatted

def process_file(input_file, output_file):
    with open(input_file, 'r') as fin, open(output_file, 'w') as fout:
        lines = fin.readlines()
        if not lines:
            return

        # Find header line (first non‑comment, non‑empty)
        header_idx = 0
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped and not stripped.startswith('#'):
                header_idx = i
                break
        else:
            print("No header line found. Exiting.")
            return

        # Extract column names from header
        header_line = lines[header_idx].strip()
        col_names = re.split(r'\s+', header_line)   # list of shift types
        # Write header unchanged
        fout.write(lines[header_idx])

        # Process remaining lines
        for line in lines[header_idx+1:]:
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                fout.write(line)
                continue

            # Split data line into fields
            fields = re.split(r'\s+', stripped)
            if len(fields) < len(col_names) + 1:
                # Malformed line; write as is (should not happen)
                print("Warning: Skipping line with insufficient fields: {}".format(line.strip()), file=sys.stderr)
                fout.write(line)
                continue

            # First field is pseudoresidue name
            new_fields = [fields[0]]
            # Apply offsets to shift columns
            for i, val in enumerate(fields[1:]):
                if i >= len(col_names):
                    break
                nucleus = col_names[i]
                new_fields.append(apply_offset(val, nucleus))

            # Reconstruct line with tabs
            fout.write("\t".join(new_fields) + "\n")

    print("Processed {} -> {}".format(input_file, output_file))
    print("Applied offsets: Carbon {:.4f}, Proton {:.4f}, Nitrogen {:.4f}".format(
        CARBON_DELTA, PROTON_DELTA, NITROGEN_DELTA))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python rereference.py input.tab output.tab")
        sys.exit(1)
    process_file(sys.argv[1], sys.argv[2])
