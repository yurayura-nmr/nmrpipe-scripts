#!/usr/bin/env python3

"""
Generate CYANA .prot file from FLYA HSQC peak list
for selected residues.

Edit FIXED_RESIDUES below to define which residues
should be written to fix.prot
"""

INPUT_FILE = "N15HSQC_asn.peaks"
OUTPUT_FILE = "fix.prot"

# === DEFINE RESIDUES TO FIX HERE ===
FIXED_RESIDUES = {164, 165, 166, 167, 168, 169}
# ====================================

SHIFT_ERROR = 0.010


def parse_peaklist(filename):

    residues = {}

    with open(filename) as f:
        for line in f:

            if line.startswith("#"):
                continue

            parts = line.split()
            if len(parts) < 5:
                continue

            try:
                h_shift = float(parts[1])
                n_shift = float(parts[2])
            except ValueError:
                continue

            # Find H.xxx token dynamically
            h_token = None
            for p in parts:
                if p.startswith("H."):
                    h_token = p
                    break

            if not h_token:
                continue

            resid = int(h_token.split(".")[1])

            if resid in FIXED_RESIDUES:
                residues[resid] = {
                    "H": h_shift,
                    "N": n_shift
                }

    return residues


def write_prot(residues, filename):

    index = 1

    with open(filename, "w") as f:
        for resid in sorted(residues):

            f.write(f"{index:6d} {residues[resid]['N']:8.3f} {SHIFT_ERROR:7.3f} N   {resid:4d}\n")
            index += 1

            f.write(f"{index:6d} {residues[resid]['H']:8.3f} {SHIFT_ERROR:7.3f} H   {resid:4d}\n")
            index += 1


def main():
    residues = parse_peaklist(INPUT_FILE)
    write_prot(residues, OUTPUT_FILE)

    print(f"Found residues: {sorted(residues.keys())}")
    print(f"Wrote {len(residues)*2} entries to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
