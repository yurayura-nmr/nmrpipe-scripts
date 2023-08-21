Adding a structure to FLYA
""""""""""""""""""""""""""

This can help FLYA with the NOESY data (to make expected peaks).
Alphafold / x-ray structures have no hydrogens which are required by FLYA.
Pymol H_add will use a different format not understood by CYANA.

In CYANA::

  read x_ray_or_alphafold.pdb
  atoms attach
  write test.pdb

