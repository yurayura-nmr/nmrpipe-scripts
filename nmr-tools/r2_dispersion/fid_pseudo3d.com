#!/bin/csh

bruk2pipe -in ./ser \
  -bad 0.0 -aswap -DMX -decim 2376 -dspfvs 20 -grpdly 67.9872589111328  \
  -xN              1024  -zN               128  -yN                19  \
  -xT               512  -zT                64  -yT                19  \
  -xMODE            DQD  -zMODE  Echo-AntiEcho  -yMODE           Real  \
  -xSW         8417.508  -zSW         2411.963  -ySW             19.0  \
  -xOBS         700.183  -zOBS          70.957  -yOBS               1  \
  -xCAR           4.700  -zCAR         118.075  -yCAR             0.0  \
  -xLAB              HN  -zLAB             15N  -yLAB              ID  \
  -ndim               3  -aq2D          States                         \
| nmrPipe -fn TP \
| nmrPipe -fn ZTP \
| nmrPipe -fn TP -hyper \
| pipe2xyz -out ./fid/%d.fid -verb -ov
