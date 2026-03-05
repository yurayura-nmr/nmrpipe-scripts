#!/usr/bin/env python3
"""
Convert XEASY 2D or 3D peak list to BARASA format.

Usage:
    xeasy2barasa.py input.txt output.txt [--exp EXPERIMENT] [tol1 tol2 ...]

Experiment types:
    hsqc       (2D)            N_H positive only
    hncacb     (3D, default)   CB positive, CA negative
    cbca conh  (3D)            CA positive, CB negative
    hnco       (3D)            CO(i-1)_N_H positive only
    hncaco     (3D)            CO_N_H and CO(i-1)_N_H, both positive

The number of tolerances must match the number of dimensions in the output order:
- For 2D: order is N, H → two tolerances (default: 0.3 0.01)
- For 3D: order is C, N, H → three tolerances (default: 0.2 0.3 0.01)

If tolerances are not supplied, built‑in defaults for the experiment type are used.
"""

import argparse
import sys
import re

# ----------------------------------------------------------------------
# Templates for different experiment types
# ----------------------------------------------------------------------
TEMPLATES = {
    2: {
        "hsqc": {
            "peak_types": ["N_H"],
            "positive": ["N_H"],
            "negative": [],
            "default_tols": [0.3, 0.01],          # N, H
            "reorder": [1, 0]                      # XEASY (H,N) -> BARASA (N,H)
        }
    },
    3: {
        "hncacb": {
            "peak_types": ["CB_N_H", "CB(i-1)_N_H", "CA_N_H", "CA(i-1)_N_H"],
            "positive": ["CB_N_H", "CB(i-1)_N_H"],
            "negative": ["CA_N_H", "CA(i-1)_N_H"],
            "default_tols": [0.2, 0.3, 0.01],      # C, N, H
            "reorder": [1, 2, 0]                    # XEASY (H,C,N) -> BARASA (C,N,H)
        },
        "cbca conh": {
            "peak_types": ["CA_N_H", "CA(i-1)_N_H", "CB_N_H", "CB(i-1)_N_H"],
            "positive": ["CA_N_H", "CA(i-1)_N_H"],
            "negative": ["CB_N_H", "CB(i-1)_N_H"],
            "default_tols": [0.2, 0.3, 0.01],      # C, N, H
            "reorder": [1, 2, 0]                    # XEASY (H,C,N) -> BARASA (C,N,H)
        },
        "hnco": {
            "peak_types": ["CO(i-1)_N_H"],
            "positive": ["CO(i-1)_N_H"],
            "negative": [],
            "default_tols": [0.2, 0.3, 0.01],      # CO, N, H (treated as C,N,H)
            "reorder": [1, 2, 0]                    # XEASY (H,CO,N) -> BARASA (CO,N,H)
        },
        "hncaco": {
            "peak_types": ["CO_N_H", "CO(i-1)_N_H"],
            "positive": ["CO_N_H", "CO(i-1)_N_H"],
            "negative": [],
            "default_tols": [0.2, 0.3, 0.01],      # CO, N, H
            "reorder": [1, 2, 0]                    # XEASY (H,CO,N) -> BARASA (CO,N,H)
        }
    }
}

# Indices of fields in XEASY data lines (0‑based)
XEASY_FIELD = {
    "id": 0,
    "shifts_start": 1,      # first shift column
    "intensity": {2: 5, 3: 6}   # intensity column index for each dimension
}

def read_xeasy_header(input_file):
    """Read XEASY header to get number of dimensions."""
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith("# Number of dimensions"):
                match = re.search(r"(\d+)", line)
                if match:
                    return int(match.group(1))
    return None

def parse_xeasy_peaks(input_file, dims):
    """
    Parse XEASY data lines.
    Returns list of tuples (shifts_in_original_order, intensity).
    """
    peaks = []
    shift_count = dims
    inten_idx = XEASY_FIELD["intensity"][dims]
    with open(input_file, 'r') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split()
            if len(parts) < inten_idx + 1:
                print(f"Warning: line {line_num} has too few fields, skipping.", file=sys.stderr)
                continue
            try:
                shifts = [float(parts[XEASY_FIELD["shifts_start"] + i]) for i in range(shift_count)]
                intensity = float(parts[inten_idx])
            except ValueError:
                print(f"Warning: line {line_num} contains non‑numeric data, skipping.", file=sys.stderr)
                continue
            peaks.append((shifts, intensity))
    return peaks

def write_barasa(output_file, peaks, tols, template):
    """Write peaks in BARASA format with given tolerances."""
    with open(output_file, 'w') as f:
        # Header lines
        f.write("CrossPeakTypes\t" + "\t".join(template["peak_types"]) + "\n")
        if template["positive"]:
            f.write("PositivePeakTypes\t" + "\t".join(template["positive"]) + "\n")
        else:
            f.write("PositivePeakTypes\n")
        if template["negative"]:
            f.write("NegativePeakTypes\t" + "\t".join(template["negative"]) + "\n")
        else:
            f.write("NegativePeakTypes\n")
        # Tolerance line (trailing tab as in examples)
        f.write("\t".join(str(t) for t in tols) + "\t\n")
        # Peak data
        reorder = template["reorder"]
        for shifts, intensity in peaks:
            ordered = [shifts[i] for i in reorder]
            f.write("\t".join(f"{x:g}" for x in ordered) + f"\t{intensity:g}\n")

def main():
    parser = argparse.ArgumentParser(
        description="Convert XEASY 2D/3D peak list to BARASA format."
    )
    parser.add_argument("input", help="Input XEASY file")
    parser.add_argument("output", help="Output BARASA file")
    parser.add_argument("--exp", "-e", 
                        choices=["hsqc", "hncacb", "cbca conh", "hnco", "hncaco"],
                        help="Experiment type (default: hsqc for 2D, hncacb for 3D)")
    parser.add_argument("tolerances", nargs='*', type=float,
                        help="Tolerances for each dimension in output order "
                             "(e.g., for 3D: C N H). If not given, defaults are used.")
    args = parser.parse_args()

    # Detect dimensionality
    dims = read_xeasy_header(args.input)
    if dims is None:
        print("Could not determine number of dimensions from header.", file=sys.stderr)
        sys.exit(1)
    if dims not in TEMPLATES:
        print(f"Unsupported dimensionality: {dims}. Only 2 and 3 are supported.", file=sys.stderr)
        sys.exit(1)

    # Determine experiment
    if args.exp:
        exp = args.exp
    else:
        # Default: hsqc for 2D, hncacb for 3D
        exp = "hsqc" if dims == 2 else "hncacb"

    # Check that experiment exists for this dimensionality
    if exp not in TEMPLATES[dims]:
        print(f"Error: Experiment '{exp}' is not defined for {dims}D data.", file=sys.stderr)
        sys.exit(1)

    template = TEMPLATES[dims][exp]

    # Handle tolerances
    if args.tolerances:
        if len(args.tolerances) != dims:
            print(f"Error: Expected {dims} tolerances, got {len(args.tolerances)}.", file=sys.stderr)
            sys.exit(1)
        tols = args.tolerances
    else:
        tols = template["default_tols"]
        print(f"Using default tolerances for {exp}: {' '.join(str(t) for t in tols)}", file=sys.stderr)

    # Parse peaks
    peaks = parse_xeasy_peaks(args.input, dims)
    if not peaks:
        print("No peaks found. Please check input format.", file=sys.stderr)
        sys.exit(1)

    # Write output
    write_barasa(args.output, peaks, tols, template)
    print(f"Converted {len(peaks)} peaks ({dims}D, experiment: {exp}) to {args.output}")

if __name__ == "__main__":
    main()
