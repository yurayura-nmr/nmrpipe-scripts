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

Intensity extraction
""""""""""""""""""""

5.	Move to "spect" folder
6.	Modify xpk file 
6.  Modify pkfit.in: verify / update the 15N base frequency (can easily get the 15N frequency from grep BF3 ../acqu). Make sure constant CPMG time is correct (d20 in pulseprogram). 1/t_CP values are obtained from our spreadsheet (it lists all cases like CPMG time = 30 ms, 40 ms, 50 ms ...).
7.	pkfiti –i pkfit.in –o pkfit.out
8.	“Int” file will be created
9.	cpmg2glove –i Int_### 298>glove.in (Check the measurement temperature)
10.	Create a new folder
11.	Move “glove.in” to the folder
12.	glove –dvx
13.	mplot -pdf
