Sample preparation
""""""""""""""""""

Note: lower sample volume (4-mm shigemi) to conserve expensive phage

Sample:

* 55 ul Pf1 phage [12.5 mg/ml final assuming 220 ul total volume]
* 11 ul D2O [4% assuming 220 ul total volume]
* 154 ul protein [in NMR buffer, dilute if necessary]
* 0-3 ul 5 M sodium chloride [if interaction too strong]


Set for measurement
"""""""""""""""""""

* cnst4: = J(NH) [set to 93 (Hz), J-coupling for H-N]
* d21: = [set to 5.3 (ms); it is 1/2J. For some reason this is not automatically calculated in the pulse program]
* d26: = [calculated in pulseprogram from cnst4. For some reason this one is calculated in the pulse program whereas d21 is not and needs to be set]



Notes for IPAP measurements
"""""""""""""""""""""""""""

The F1 time domain is the number of point of IP + AP, so it should be at least 700 or up to 1024. 
In HSQC terms, this would be 350 or 512 points, respectively.
Verified that up to 1400 points can be safely set. Even 1536 seems to work (is what I had used for NBR1 in 2014: 1536/2 = 768).

In TopSpin split the 2D experiment containing IP + AP into two separate processed files by::

  $ split ipap 2

It allows us to choose a relaxation-accomodating factor ~1.04 and then creates 2 new clean files e.g., 10000 and 10001 for the separate FIDs / spectra.

One can then just process these separate files as standard HSQC experiments.

For some reason, in some pulse programs this differs, e.g., the SI-version on our 700 MHz system wants the command::

  $ splitipap2
