Sample
""""""

Do not forget to add DSS.
0.5 ul of 100 mM DSS stock solution is sufficient for a 250 ul sample.

Example:

#. 237  ul protein sample in buffer
#. 12.5 ul D2O
#. 0.5  ul DSS stock solution


Calibration
"""""""""""

Calibrate hard pulses 1H as always, 13C and 15N using hsqcf2calib, hsqcf3calib.

Measurements
""""""""""""

Various experiments out of our assign3d folder

1. DSS (zgesgp) 1
2. nHSQC (~gpsi2) 2
3. cHSQC 11
4. cHSQC 12
5. cHSQC 21
6. hnco 3
7. hncaco 4
8. hncoca 5
9. hnca 6
10. cbcaconh 7
11. hncacb 8
12. (h)ccconh 9
13. nnoesy 10
14. h(cc)(co)nh 15
15. hbha(co)nh 16
16. hbhanh 17
17. cnoesy 20

Processing
----------

DSS 1D
""""""

#. In NMRPIPE, process 1D spectrum of DSS measurement using fidft_dss.com
#. Find the DSS peak around 0.0 ppm. Note down its actual chemical shift (e.g., -0.076ppm).

nHSQC
-----

#. In NMRPIPE, process the 15N-HSQC.
#. Execute python3 dss.py script. 
#. According to the output of that script, replace the 1H/15N spectral centers (in ppm) in the ft_nhsqc.com script.
#. Can now already import the nHSQC to CCPN.
#. Set up a molecule from the one-letter sequence.
#. Can already start picking peaks.

hnco
----

#. In NMRPIPE, process the HNCO using the fid_hnco.com and ft_hnco.com scripts.
#. Execute python3 dss.py script. 
#. According to the output of that script, replace the 1H/15N/13C spectral centers (in ppm) in the fid script.
#. Can now already import the HNCO to CCPN.
#. Make new window: HN-C (HSQC with additional 13C z-dimension): make sure that the HNCO peaks match up in 1H/15N with the HSQC peaks.
#. Make new window: co   (CO strip to pick the CO peaks).

Preliminary check of data quality after HNCO/HSQC / Set a base for assignment peak picking
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

In CCPN, use peak lists -> nhsqc. Switch on the following options:

#. Find Peak: Window HN (locates a picked peak in the HSQC. We will use that to navigate to the corresponding HNCO slice).
#. Go To Position: 1H-15N in co (this will conveniently navigate so we can easily pick the CO (of amino acid i-1) peaks)

* FLYA will not require this but for good CCPN book-keeping, can already set up resonances for "good HSQC peaks" with "good HNCO connectivity".
* This might help later to avoid passing bad peaks to FLYA. It will also give us a good count of how many peaks we have / how many we expect from the amino acid sequence. 
* Set up spin system in HSQC and propagate assignment to the HNCO peak. Do not add the 13C connectivity yet.
* CCPN will also estimate our chemical shift tolerance for FLYA if we peak the same spin system in multiple spectra (e.g. HSQC and HNCO overlap in 1H and 15N).
* Note: we are using CCPN here but the route is a bit reminiscent of KUJIRA/MAGRO. There you also start with picking the HNCO (not the HSQC) to set the base for the assignment.
* The great advantage of the HNCO is its high sensitivity, that it eliminates sidechains etc. from the HSQC peak picking and can show us where we picked too many / missed any HSQC peaks, and it can already tell us a lot of HSQC peak overlap and sort out if there is actually 2 peaks hidden in "one peak".

For later easy reference:

* HSQC peaks with HNCO connectivity -> assign to spin system
* HSQC peaks without HNCO connectivity -> do not assign to a spin system; these are likely sidechains etc.

Check HNCO for completeness of root-resonance picking
"""""""""""""""""""""""""""""""""""""""""""""""""""""

* After picking all CO peaks starting from the HSQC root, navigate through the entire HNCO and see if any unpicked peaks exist.
* e.g. start with low 15N (130 ppm) and go through all CH slices until high 15N frequency end (110 ppm or so).
* Whenever not sure if we picked this peak, try to auto-peak pick the whole slice in CCPN (the program will reject this if the peak was picked before). CCPN will find peaks even if below the current contour level!
* If any peaks without CCPN spin system number show up, these were likely missed when picking the HSQC.
* Can also pick up sidechains at this point.
* This consistency check is also good for HNCA. Walk through 15N-dimension from 130 to 110 or so and see if anything was missed here.
* Can do a peak check every 2-planes, but be extremely careful in crowded regions - the CCPN peak picker easily misses close/partially overlapped peaks and ignores them.

Export peaklists for FLYA
"""""""""""""""""""""""""

Use the format converter -> xeasy -> peaks -> Write as cyana format.

* Export -> XEasy -> Peaks export
* Peak list: 1 by 1 export all of them
* Export file: ~.peaks
* Write as CYANA format - yes
* Peak integration method - height
* Force positive intensity - yes


Map dimensions (see cyana demo flya folder for examples on format for each spectrum)::

  * HSQC. Dimension 0 H(acqu); Dimension 1 N
  * HNCO. Dimension 0 H(acqu); Dimension 1 C; Dimension 2 N 

Cyana / FLYA calls H(acqu) in our case HN.




Add more data to FLYA from additional experiments
"""""""""""""""""""""""""""""""""""""""""""""""""

hncaco
------

#. In NMRPIPE, process the HNCO using the fid_hncaco.com and ft_hncaco.com scripts.
#. Execute python3 dss.py script. 
#. According to the output of that script, replace the 1H/15N/13C spectral centers (in ppm) in the fid script.


hncacb
------

#. In NMRPIPE, process the HNCACB using the fid_hncacb.com and ft_hncacb.com scripts.
#. Execute python3 dss.py script. 
#. According to the output of that script, replace the 1H/15N/13C spectral centers (in ppm) in the fid script.
#. CCPN: make a new window for CA/CB (this will likely have different aspect ratio than CO and of course a different range, so it is convenient to have separate windows).
#. CCPN: contours: enable positive/negative. Peak finding: enable positive/negatitve.


hnca
----

#. In NMRPIPE, process the HNCO using the fid_hncaco.com and ft_hncaco.com scripts.
#. Execute python3 dss.py script. 
#. According to the output of that script, replace the 1H/15N/13C spectral centers (in ppm) in the fid script.


CCPN hotkeys for peak picking
"""""""""""""""""""""""""""""

#. q - propagate assignments
#. n - delete marks


Headers for *.peaks files
-------------------------

HNCACB ("CBCANH")::

  # Number of dimensions 3
  #FORMAT xeasy3D
  #INAME 1 HN
  #INAME 2 N
  #INAME 3 C
  #SPECTRUM CBCANH HN N C

HNCO::

  # Number of dimensions 3
  #INAME 1 HN
  #INAME 2 C
  #INAME 3 N
  #SPECTRUM HNCO HN C N

HNcaCO::

  # Number of dimensions 3
  #INAME 1 HN
  #INAME 2 C
  #INAME 3 N
  #SPECTRUM HNcaCO HN C N

13C-HSQC::

  # Number of dimensions 2
  #FORMAT xeasy2D
  #INAME 1 H
  #INAME 2 C
  #SPECTRUM C13HSQC H C

HNCA::

  #FORMAT xeasy3D
  #INAME 1 HN
  #INAME 2 C
  #INAME 3 N
  #SPECTRUM HNCA HN C N

HNcoCA::

  # Number of dimensions 3
  #FORMAT xeasy3D
  #INAME 1 HN
  #INAME 2 C
  #INAME 3 N
  #SPECTRUM HNcoCA HN C N

C13NOESY::

  #Number of dimensions 3
  #FORMAT xeasy3D
  #INAME 1 H
  #INAME 2 HC
  #INAME 3 C
  #SPECTRUM C13NOESY H HC C

  (To quickly discriminate H and HC: HC contains chemical shifts 0 - 4.4 or so; H contains the whole range including amides > 8 ppm and aromatic side chains > 9 ppm).

N15NOESY::

  # Number of dimensions 3
  #FORMAT xeasy3D
  #INAME 1 H
  #INAME 2 HN
  #INAME 3 N
  #SPECTRUM N15NOESY H HN N
  
  (To quickly discriminate H and HN: HN contains amide chemical shifts 7-9ppm or so; H contains the whole range including aliphatics < 1 ppm etc.).


Check the output files
""""""""""""""""""""""

* flya.txt (statistics)
* flya.tab (lists and their assessment: strong or not). No reference if de novo.
* To import assigned lists into CCPN, select Import > Single Files > Peaks > Cyana. 

Adding a structure to FLYA
""""""""""""""""""""""""""

This can help FLYA with the NOESY data (to make expected peaks).
Alphafold / x-ray structures have no hydrogens which are required by FLYA.
Pymol H_add will use a different format not understood by CYANA.

In CYANA::

  read x_ray_or_alphafold.pdb
  atoms attach
  write test.pdb

For tricky assignments
""""""""""""""""""""""

For larger proteins, often it is not possible to completely rely on FLYA (it will make mistakes) nor to manually fill in all the gaps.
In that case, it can be helpful to use the partial assignment that was manually confirmed in CCPN (based on FLYA but with user-confirmation) as a reference.
To CALC.cya::

  flya assignpeaks=$peaks structure=input.pdb shiftreference=ref.prot

, where ref.prot is the CCPN-exported list of chemical shifts that were confirmed by the user.
The resulting flya.pdf will then color in red the points where FLYA disagrees with the user-input.
That can be oversights, problems with aliasing/tolerancce, peak-picking, etc.

So, we can use an iterative process::

  Write updated fix.prot (user-provided fixed shifts) in CCPN
  |
  Re-run FLYA
  |
  Inspect flya.pdf
  |
  Fix red-colored problems (and go back to step 1)
  (or)
  Confirm some of FLYA's new assignments manually (and go back to step 1)
  


Notes
"""""

* In an older version of this script, it said that peak lists need to be edited to remove negative intensities and to swap the "T" to "a" in peaklists exported from CCPN. This seems no longer the case.
* To confirm, just check length of *.peaks file (e.g., HNCACB) containing negative files. The CYANA output will say, how many peaks it picked up::

  - calibration: read peaks HNCACB format= append
  - Peak list "HNCACB.peaks" read, 426 peaks, 0 assignments.
