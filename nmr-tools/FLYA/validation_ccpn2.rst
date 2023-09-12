CCPN2
-----

After FLYA, the chemical shift assignment needs to be validated manually.
At least, we have to make sure that the backbone connections established by FLYA make sense.

In the backbone assignment panel of CCPN2:

1. Make a query window:: 
  
  This will "query" from a (i-1) spectrum to find a fitting (i) residue in the other type of experiments.
  Experiments in queryC:
  HNCO
  HNcoCA
  CBCAcoNH

2. Make a match window:: 

  This will contain possible matches for the (i-1) queries. It contains only (i) experiments.
  Experiments in matchC:
  HNcaCO
  HNCA
  HNCACB

