#!/bin/tcsh

setenv NAME hccconh

bruk2pipe -in ser \
  -bad 0.0 -aswap -DMX -decim 2376 -dspfvs 20 -grpdly 67.9872589111328  \
  -xN              1024  -yN                48  -zN                64  \
  -xT               512  -yT                24  -zT                32  \
  -xMODE            DQD  -yMODE  Echo-AntiEcho  -zMODE        Complex  \
  -xSW         8417.508  -ySW         1773.679  -zSW         4901.964  \
  -xOBS         700.183  -yOBS          70.957  -zOBS         700.183  \
  -xCAR           4.776  -yCAR         117.092  -zCAR       3.0259935  \
  -xLAB              HN  -yLAB               N  -zLAB               H  \
  -ndim               3  -aq2D          States                         \
  -out fid/${NAME}%03d.fid -verb -ov
