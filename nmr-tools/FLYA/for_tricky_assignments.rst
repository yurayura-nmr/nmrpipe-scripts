For tricky assignments
""""""""""""""""""""""

For larger proteins, often it is not possible to completely rely on FLYA (it will make mistakes) nor to manually fill in all the gaps.
In that case, it can be helpful to use the partial assignment that was manually confirmed in CCPN (based on FLYA but with user-confirmation) as a reference.
To CALC.cya::

  shiftassing_fix:=fix.prot
  flya assignpeaks=$peaks structure=input.pdb shiftreference=fix.prot

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
  
