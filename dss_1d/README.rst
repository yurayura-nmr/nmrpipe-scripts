DSS addition to sample
----------------------

Sample::

  0.2 mM DSS to sample (stock solution: 100 mM)
  For example: 0.7 ul DSS stock solution for 350 ul sample

1D NMR processing for chemical shift referencing (e.g., DSS proton shift)
-------------------------------------------------------------------------
  
This folder contains 1D NMR processing scripts for a 1D proton NMR experiment. 

Requires nmrpipe and tcsh (or csh), and python3 to be installed. 

The python file reads the measured (e.g., peak-picked in nmrDraw) methyl proton shift of DSS. 
It then calculates the properly referenced 0-ppm point for 1H, 15N, and 13C for any kind of multidimensional NMR experiment
For example, HBHAcoNH, 15N-edited NOESY etc., when executed correctly in the respective Bruker Topspin experiment directory
(i.e., the script needs access to the experimental parameters stored in the acqus etc. files).
