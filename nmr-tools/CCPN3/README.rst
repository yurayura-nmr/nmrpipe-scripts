Notes on CcpNmr AnalysisAssign (version 3.2)
--------------------------------------------

1. Install as usual into /opt/, include into path, call program with analysisassign. Will run some updates on first launch.
2. Load spectra into project (HSQC, HNCO, ...).
3. Make chain (from 1 or 3 letter sequence)
4. Display 3 windows: 2D_HN (HSQC), 3D_HCN (HNCO, HNcaCO), 3D_HCN_1 (HNCACB, CBCAcoNH, HNCA, ...)

To transfer previously established (FLYA etc.) assignments
----------------------------------------------------------

In panel *Pick and assign*:

1. Double click a dummy (@) residue, e.g. @14
2. Select Edit NmrResidue
3. Set sequence code: residue ID (e.g. 76 for G76)
4. Set residue type
5. For CO window: do restricted peak pick (this will transfer the assignment to the selected carbon strip).
6. For CACB window: do it again.
7. In carbon strip, select peak and then, in NmrAtomAssigner: select C-1 for HNCO atom, C for HNcaCO atom etc.

Peak pick order
---------------

1. CO: HNCO > HNcaCO
2. CA: HNcoCA > HNCA
3. CB: CBCOcoNH > HNCACB


Troubleshooting
---------------

Known bug 1::

  Error - "NoneType has no attribute ..." - save project and open project.
