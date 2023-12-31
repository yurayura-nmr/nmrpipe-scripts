#!/bin/csh

setenv NAME ccconh

bruk2pipe -verb -in ./ser \
  -bad 0.0 -ext -aswap -AMX -decim 2040 -dspfvs 20 -grpdly 67.9862060546875  \
  -xN              1024  -yN                48  -zN                80  \
  -xT               512  -yT                24  -zT                40  \
  -xMODE            DQD  -yMODE  Echo-AntiEcho  -zMODE        Complex  \
  -xSW         9803.922  -ySW         2483.855  -zSW        11261.261  \
  -xOBS         600.133  -yOBS          60.818  -zOBS         150.909  \
  -xCAR           4.778  -yCAR         119.101  -zCAR          40.746  \
  -xLAB              HN  -yLAB               N  -zLAB               C  \
  -ndim               3  -aq2D          States                         \
  -out fid/${NAME}%03d.fid -verb -ov
