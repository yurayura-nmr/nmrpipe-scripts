To process pseudo3D
===================

Relaxation dispersion data are acquired as pseudo-3D experiments.

FID processing and Fourier transform
""""""""""""""""""""""""""""""""""""

1.	Execute ”fid_pseudo3d.com" where ser file exists: modify this file by using bruker script of NMRpipe; don't forget to exchange y and z (should be xzy in fid.com). x: 1H, z: 15N, y: pseudo (1 / tau_cp) dimension
2.	Move to "fid" folder and put "ft.com" in this folder (rename ft_pseudo3d.com as ft.com)
3.	"ft.com 1": process only 1 (if FT files are strange, delete fid files and re-process data by fid.com)
4. Then ... 

Execute (to process all 19 spectra or so):: 

  ft2d_all 600r2 -nv

where 600r2 is just a name that will be used for the spectrum files.

One can now visualize the original HSQC (ft2) and the R2 dispersion reference spectrum (nv) in CCPN to make sure that peak lists and assignments will be fine when transferred.

Prepare assigned peaklist
"""""""""""""""""""""""""

5.	Modify xpk file

In CCPN, open and assign the reference spectrum (1st nv file). Then,::

  FormatConverter -> Export -> NMRView -> filename.xpk

If assignment is correctly done in CCPN, this should transfer the assignments to the peaklist.
xpk file should need no manual editing and can be used just as it is in cpmg2glove below.

Intensity extraction
""""""""""""""""""""

6.	Move to "spect" folder
7.  Modify pkfit.in: verify / update the 15N base frequency (can easily get the 15N frequency from grep BF3 ../acqu). Make sure constant CPMG time is correct (d20 in pulseprogram). 1/t_CP values are obtained from our spreadsheet (it lists all cases like CPMG time = 30 ms, 40 ms, 50 ms ...).
8.	Start intensity extraction.

In terminal:: 

  pkfiti –i pkfit.in –o pkfit.out

9.	“Int” file will be created
10.	Create GLOVE input file. (Check the measurement temperature)

In terminal::

  cpmg2glove –i Int_ 298 > glove.in 

Fitting of relaxation dispersion profiles
"""""""""""""""""""""""""""""""""""""""""

11.	Create a new folder
12.	Move “glove.in” to the folder

Execute fitting in the terminal::

  glove –dvx
  mplot -pdf

If constant profile, change function to: CPMG_CONST in glove.in or use cpmg2glove to do it faster for all residues::

  cpmg2glove -t CONST -i ../Int_60.81 298 > glove.in

Publication quality (SI)
""""""""""""""""""""""""

If all glove plots should be included in the Supporting Information, copy & pasting ghostscript-conversions of the plot.pdf is the easiest option. After installing hostscript in chocolatey::

   gswin64c -sDEVICE=png16m -r1200 -o output_%d.png -dLastPage=3 plot.pdf

Make sure to turn off image compression in Word or this nice picture creation was for nothing!^-^
