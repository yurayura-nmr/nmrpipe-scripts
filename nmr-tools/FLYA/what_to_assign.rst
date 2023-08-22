What should FLYA assign?
------------------------

Sometimes we only want the backbone, sometimes we want the full protein.
Sometimes it is paradoxically easier to assign the backbone if we also use sidechain information.

In the ASSIGN.cya, we define what we ask from FLYA::

  command select_atoms
  atom select "N H HA CA CB C"
  end

In this example, we use the backbone plus HA because we have NOESY data and we have a 13C-HSQC.
If we remove HA from the list, then FLYA will tell us that it cannot make any expected peaks.
Of course, it is right in pointing that out. Since there are no amide protons (H) in the 13C-HSQC, it cannot simulate any peaks.
