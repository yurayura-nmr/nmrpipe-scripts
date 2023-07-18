#!/bin/tcsh

setenv NAME cnoesy

bruk2pipe -verb -in ./ser \
  -bad 0.0 -ext -aswap -AMX -decim 2040 -dspfvs 20 -grpdly 67.9862060546875  \
  -xN              1024  -yN                64  -zN               128  \
  -xT               512  -yT                32  -zT                64  \
  -xMODE            DQD  -yMODE  Echo-AntiEcho  -zMODE        Complex  \
  -xSW         9803.922  -ySW        12315.271  -zSW         9803.922  \
  -xOBS         700.183  -yOBS         176.065  -zOBS         700.183  \
  -xCAR           4.776  -yCAR         27.7404  -zCAR           4.776  \
  -xLAB              1H  -yLAB             13C  -zLAB              HC  \
  -ndim               3  -aq2D          States                         \
  -out fid/${NAME}%03d.fid -verb -ov
