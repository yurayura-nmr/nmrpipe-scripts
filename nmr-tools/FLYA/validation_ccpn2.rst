CCPN2
-----

After FLYA, the chemical shift assignment needs to be validated manually.
At least, we have to make sure that the backbone connections established by FLYA make sense.

In the backbone assignment panel of CCPN2:

1. Define new windows to help us

Make a query window:: 
  
  This will "query" from a (i-1) spectrum to find a fitting (i) residue in the other type of experiments.
  Experiments in queryC:
  HNCO
  HNcoCA
  CBCAcoNH
  Set aspect ratio of window = 8; max. strips = 2 for now (not de novo assignment)

Make a match window:: 

  This will contain possible matches for the (i-1) queries. It contains only (i) experiments.
  Experiments in matchC:
  HNcaCO
  HNCA
  HNCACB
  Set aspect ratio of window = 8; max. strips = 2 for now (not de novo assignment)

2. Set sequential links. Note: sometimes CCPN scoring system is very confused when a peak is not observed (i.e., it is not there, it is not that it does not match (that would be a mismatch) but the peak is just not observed. In such a case, can go back to the selection and unselect the type of spectra where the peak is not observed. So for example, if a CO peak is missing, unselect HNCO, HNcaCO. This should now allow CCPN to find the correct strip for the peak)).
