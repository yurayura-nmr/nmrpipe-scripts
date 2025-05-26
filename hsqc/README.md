# HSQC processing
This folder contains 2D NMR processing scripts for 15N-1H and 13C-1H HSQC experiments. Requires nmrpipe and tcsh (or csh) to be installed.
Here's a **tutorial** for first timers in NMRPipe-based processing using our current Linux workstation setup:

# 🧪 NMR Data Processing Tutorial (Part 1: From Acquisition to Fourier Transform)

Welcome! If you've just measured your NMR spectrum for the first time, this tutorial will help you prepare your data for further analysis using **NMRPipe**. Let's begin by organizing and converting your data.

## Step 1: Copy Raw NMR Data from the Machine

Open a terminal and navigate to the raw data folder:

```bash
cd 1_raw_nmr_data
```

Now run the script to copy all your recent measurements from the 600 and 700 MHz NMR machines:

```bash
./rsync_copy_data.sh
```

This will transfer all available data to your local folder for analysis.

## Step 2: Set Up for Processing

Change to the analysis directory:

```bash
cd ../2_pipe_analysis
```

Copy the raw data from step 1 into this folder (you’ll work here to preserve the original data):

```bash
cp -r ../1_raw_nmr_data/your_dataset_folder ./
```

Replace `your_dataset_folder` with the actual name of your dataset.

## Step 3: Prepare the Processing Script

First, get the NMRPipe conversion script named `fid_ft.com`. You can:

* Download it from [my GitHub]([https://github.com/yurayura-nmr/nmrpipe-scripts/blob/main/hsqc/fidft_nhsqc.com]), or
* Copy it from a previous analysis folder if available.

Now enter **tcsh** shell and launch the **bruker** helper tool:

```bash
tcsh
bruker
```

Click **“Read Parameters”** in the interface.

This tool will output the correct parameters for your dataset. Use these to **update the upper section** of `fid_ft.com` (the format conversion part).
Make sure all the read-in parameters correspond to what you actually set up at the time of measurement (Spectral widths in Hz in 1H and 15N dimension, as well as center positions in ppm).

## Step 4: Run the Script

In the terminal (still in `tcsh`), run the processing script:

```bash
./fid_ft.com
```

If no errors appear, the Fourier Transform and format conversion were successful.

## Step 5: Visual Check in nmrDraw

Launch the NMR viewing tool nmrDraw:

```bash
nd
```

Check:

* Spectral width (SW)
* Size of the spectrum
* Baseline and peak shape

If everything looks OK — **great job!** You’ve completed Part 1. Next comes **phasing and further processing**.

Let me know if you have questions!
