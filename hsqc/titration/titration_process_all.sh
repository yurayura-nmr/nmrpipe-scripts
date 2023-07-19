#!/bin/bash

: ' 
====================================================================================
--- Edit this part ---

Declare all measurements done
The array should contain the folder names of all titration experiments
e.g., in the simplest case just the TopSpin data folders : 1 2 3 4 5 ...
      or if more explicit names are chosen something like: 1_0eq 2_0.2eq 3_0.5eq ...
====================================================================================
' 
# Define datafolders
declare -a SpectraArray=("1" "2" "3" "4" "5" "6" "7")

# Define fidft script to be executed in all subfolders (make sure it outputs nhsqc.ft2).
procScript="fidft_nhsqc.com"




# --- Do not edit from here ---

# Make sure the script is executable.
chmod +x $procScript

# Make a folder to store the resulting titration spectra
mkdir -p all_processed


: '
*************************************************************
Start the processing loop
*************************************************************
'

for val in "${SpectraArray[@]}"; do
    echo "[ Processing titration spectrum ... ]" $val
    cd $val
    cp ../$procScript .
    ./$procScript
    cp nhsqc.ft2 ../all_processed/$val.ft2
    cd ..
done
