#!/bin/csh

# dss.py will automatically calculate new center after applying SR

setenv NAME hcch-tocsy

bruk2pipe -in ser \
  -bad 0.0 -aswap -DMX -decim 2376 -dspfvs 20 -grpdly 67.9872589111328  \
  -xN              1024  -yN                64  -zN                80  \
  -xT               512  -yT                32  -zT                40  \
  -xMODE            DQD  -yMODE        Complex  -zMODE        Complex  \
  -xSW         9803.992  -ySW         4901.961  -zSW        12315.271  \
  -xOBS         700.183  -yOBS         700.183  -zOBS         176.068  \
  -xCAR           4.714  -yCAR      2.96374983  -zCAR          43.678  \
  -xLAB              1H  -yLAB             1Hy  -zLAB             13C  \
  -ndim               3  -aq2D          States                         \
  -out fid/${NAME}%03d.fid -verb -ov
