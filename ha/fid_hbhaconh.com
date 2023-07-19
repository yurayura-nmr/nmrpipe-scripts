#!/bin/tcsh

setenv NAME hbhaconh

bruk2pipe -in ser \
  -bad 0.0 -noaswap -DMX -decim 24 -dspfvs 12 -grpdly -1  \
  -xN              1024  -yN                48  -zN                64  \
  -xT               512  -yT                24  -zT                32  \
  -xMODE            DQD  -yMODE  Echo-AntiEcho  -zMODE        Complex  \
  -xSW         7183.908  -ySW         1702.997  -zSW         4201.681  \
  -xOBS         600.133  -yOBS          60.818  -zOBS         600.133  \
  -xCAR           4.778  -yCAR         119.101  -zCAR           3.028  \
  -xLAB              HN  -yLAB               N  -zLAB               H  \
  -ndim               3  -aq2D          States                         \
  -out fid/${NAME}%03d.fid -verb -ov
