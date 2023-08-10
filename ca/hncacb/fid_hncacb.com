#!/bin/tcsh

setenv NAME hncacb

bruk2pipe -verb -in ./ser \
  -bad 0.0 -ext -aswap -AMX -decim 2040 -dspfvs 20 -grpdly 67.9862060546875  \
  -xN              1024  -yN                48  -zN                80  \
  -xT               512  -yT                24  -zT                40  \
  -xMODE            DQD  -yMODE  Echo-AntiEcho  -zMODE    States-TPPI  \
  -xSW         9803.922  -ySW         2483.855  -zSW        11261.261  \
  -xOBS         700.183  -yOBS          70.957  -zOBS         176.068  \
  -xCAR           4.776  -yCAR       117.09234  -zCAR          43.740  \
  -xLAB              HN  -yLAB             15N  -zLAB             13C  \
  -ndim               3  -aq2D          States                         \
  -out fid/${NAME}%03d.fid -verb -ov
