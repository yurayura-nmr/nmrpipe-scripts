#!/bin/csh

bruk2pipe -in ./ser \
  -bad 0.0 -ext -aswap -AMX -decim 2376 -dspfvs 20 -grpdly 67.9872589111328  \
  -xN              1024  -zN               512      -yN                 2  \
  -xT               512  -zT               256      -yT                 2  \
  -xMODE            DQD  -zMODE  Echo-AntiEcho      -yMODE           Real  \
  -xSW         8417.508  -zSW         3690.037      -ySW            1.000  \
  -xOBS         700.183  -zOBS          70.957      -yOBS           1.000  \
  -xCAR           4.774  -zCAR         119.575      -yCAR           0.000  \
  -xLAB              HN  -zLAB             15N      -yLAB              ID  \
  -ndim               3  -aq2D         States                             \
| nmrPipe -fn TP \
| nmrPipe -fn ZTP \
| nmrPipe -fn TP -hyper \
| pipe2xyz -out ./fid/%d.fid -verb -ov
# -out ./fid/test%03d.fid -verb -ov
