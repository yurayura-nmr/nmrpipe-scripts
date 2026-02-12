#!/usr/bin/python3

"""
Chemical shift referencing using DSS according to:
Markley, J. L. et al. J. Biomol. NMR 12 (1), 1−23. (1998)

Erik Walinda
Kyoto University
Graduate School of Medicine

https://github.com/yurayura-nmr/
For Bruker TopSpin

    1. Record 1D spectrum of DSS in the same buffer (external)
       or the actual protein sample (internal) standard
       using 1D pulse with water suppression (e.g., p3919fpgp).
    2. Process the 1D in nmrPipe/nmrDraw and note the observed 
       frequency (in ppm) of the DSS methyl resonance line 
       (the sharp peak around 0 ppm).
    3. Run this script in the folder containing the Bruker NMR 
       data, i.e., where the acqu, acqus files etc. are located.
       When asked, plug in the observed DSS-methyl shift in ppm.
    4. The script will give you the new, referenced spectral
       centers in ppm. Use these in your nmrPipe fid.com file 
       and you will obtain properly referenced spectra.

    Note: This script assumes the 
          15N channel is on O3 and that the 
          13C channel is on O2.

Optimized version with automatic SR(F1) handling (e.g., for HCCH-TOCSY).

Supports:
    SR(F1) = fraction * SWH(F1)

For Bruker TopSpin datasets.
"""

import os
import sys
from decimal import Decimal, getcontext


# -----------------------------
# ---- USER SETTINGS ----------
# -----------------------------

apply_SR_F1 = False                    # Enable SR correction
SR_fraction = Decimal(1) / Decimal(4)  # SR(F1) = 1/4 SWH(F1)


def main():
    dimensions = fileCheck()
    SFO1, O1, SFO2, O2, SFO3, O3, DSS_ppm = getPars()
    calc(dimensions, SFO1, O1, SFO2, O2, SFO3, O3, DSS_ppm)


def fileCheck():
    dimensions = 0

    if os.path.exists("./acqus"):
        dimensions += 1
    else:
        print("acqus not found. Run inside Bruker experiment folder.")
        sys.exit()

    if os.path.exists("./acqu2s"):
        dimensions += 1

    if os.path.exists("./acqu3s"):
        dimensions += 1

    print(f"{dimensions}D experiment detected.")
    return dimensions


def getPars():

    SFO1 = O1 = SFO2 = O2 = SFO3 = O3 = None

    with open("acqus") as f:
        for line in f:
            if line.startswith("##$SFO1"):
                SFO1 = float(line.split("=")[1])
            elif line.startswith("##$O1"):
                O1 = float(line.split("=")[1])
            elif line.startswith("##$SFO2"):
                SFO2 = float(line.split("=")[1])
            elif line.startswith("##$O2"):
                O2 = float(line.split("=")[1])
            elif line.startswith("##$SFO3"):
                SFO3 = float(line.split("=")[1])
            elif line.startswith("##$O3"):
                O3 = float(line.split("=")[1])

    if None in (SFO1, O1):
        print("Critical parameters missing in acqus.")
        sys.exit()

    print("Found parameters:")
    print("SFO1:", SFO1, "MHz")
    print("O1:", O1, "Hz")
    print("SFO2:", SFO2)
    print("O2:", O2)
    print("SFO3:", SFO3)
    print("O3:", O3)
    print()

    DSS_ppm = input("Enter measured DSS chemical shift (ppm): ")

    return SFO1, O1, SFO2, O2, SFO3, O3, DSS_ppm


def get_SWH_F1(dimensions):
    if dimensions == 3:
        filename = "acqu3s"
    elif dimensions == 2:
        filename = "acqu2s"
    else:
        print("SR only meaningful for >=2D experiments.")
        return None

    if not os.path.exists(filename):
        print(f"{filename} not found. Cannot apply SR.")
        sys.exit()

    with open(filename) as f:
        for line in f:
            if line.startswith("##$SW_h"):
                SW_h = Decimal(line.split("=")[1])
                print(f"Found SW_h (F1) in {filename}: {SW_h} Hz")
                return SW_h

    print("SW_h not found in", filename)
    sys.exit()


def calc(dimensions, SFO1, O1, SFO2, O2, SFO3, O3, DSS_ppm):

    getcontext().prec = 15

    DSS_ppm = Decimal(DSS_ppm)
    DSS_fraction = DSS_ppm * Decimal(1E-6)

    hydrogen_sf = Decimal(SFO1)
    hydrogen_o1 = Decimal(O1)

    carbon_sf = Decimal(SFO2) if SFO2 else None
    nitrogen_sf = Decimal(SFO3) if SFO3 else None

    # Conversion factors relative to 1H
    conv_H = Decimal("1.0")
    conv_C = Decimal("0.251449530")
    conv_N = Decimal("0.101329118")

    # --- Proton carrier frequency ---
    hydrogen_sf_Hz = hydrogen_sf * Decimal(1E6)
    carrier_MHz = (hydrogen_sf_Hz - hydrogen_o1) / Decimal(1E6)

    carrier_Hz = carrier_MHz * Decimal(1E6)

    # DSS drift
    DSS_drift_Hz = carrier_Hz * DSS_fraction
    DSS_zero_MHz = carrier_MHz + (DSS_drift_Hz * Decimal(1E-6))

    # True zero frequencies
    zero_H = DSS_zero_MHz * conv_H
    zero_C = DSS_zero_MHz * conv_C if carbon_sf else None
    zero_N = DSS_zero_MHz * conv_N if nitrogen_sf else None

    # New spectral centers
    center_H = ((hydrogen_sf - zero_H) / zero_H) * Decimal(1E6)
    center_C = ((carbon_sf - zero_C) / zero_C) * Decimal(1E6) if zero_C else None
    center_N = ((nitrogen_sf - zero_N) / zero_N) * Decimal(1E6) if zero_N else None

    # -----------------------------
    # ---- PRINT RESULTS ----------
    # -----------------------------

    print("\n--- DSS Referencing ---\n")
    print("Carrier (1H) [MHz]:", carrier_MHz)
    print("DSS drift [Hz]:", DSS_drift_Hz)
    print("DSS zero frequency [MHz]:", DSS_zero_MHz)
    print()

    print("New centers:")
    print("1H  [ppm]:", center_H)
    if center_C:
        print("13C [ppm]:", center_C)
    if center_N:
        print("15N [ppm]:", center_N)

    # -----------------------------
    # ---- SR CORRECTION ----------
    # -----------------------------

    if apply_SR_F1 and dimensions >= 2:

        SW_h_F1 = get_SWH_F1(dimensions)
        SR_Hz = SR_fraction * SW_h_F1
        SR_ppm = SR_Hz / DSS_zero_MHz

        print("\n--- SR(F1) Correction ---\n")
        print("SR fraction:", SR_fraction)
        print("SR (Hz):", SR_Hz)
        print("SR (ppm):", SR_ppm)
        print()
        print("1H center after SR [ppm]:", center_H - SR_ppm)


if __name__ == "__main__":
    main()

