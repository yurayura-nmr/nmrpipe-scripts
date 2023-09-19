#!/bin/csh

setenv NAME ccconh

bruk2pipe -in ser \
  -bad 0.0 -noaswap -DMX -decim 24 -dspfvs 12 -grpdly -1  \
  -xN              1024  -yN                48  -zN                80  \
  -xT               512  -yT                24  -zT                40  \
  -xMODE            DQD  -yMODE  Echo-AntiEcho  -zMODE        Complex  \
  -xSW         7183.908  -ySW         1702.997  -zSW        10111.223  \
  -xOBS         600.133  -yOBS          60.818  -zOBS         150.909  \
  -xCAR           4.778  -yCAR         119.101  -zCAR          40.746  \
  -xLAB              HN  -yLAB               N  -zLAB               C  \
  -ndim               3  -aq2D          States                         \
  -out fid/${NAME}%03d.fid -verb -ov
