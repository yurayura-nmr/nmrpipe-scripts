#!/bin/tcsh

# 13-HSQC (constant time)

bruk2pipe -verb -in ./ser \
  -bad 0.0 -ext -aswap -AMX -decim 2040 -dspfvs 20 -grpdly 67.9862060546875  \
  -xN              1024  -yN               256  \
  -xT               512  -yT               128  \
  -xMODE            DQD  -yMODE  Echo-AntiEcho  \
  -xSW         9803.922  -ySW        12315.271  \
  -xOBS         700.183  -yOBS         176.067  \
  -xCAR           4.776  -yCAR          40.740  \
  -xLAB              1H  -yLAB             13C  \
  -ndim               2  -aq2D          States  \
  -out ./cthsqc.fid -verb -ov

nmrPipe -in cthsqc.fid                              \
| nmrPipe -fn POLY -time                            \
| nmrPipe -fn SP -c 0.5 -off 0.4 -end 0.95 -pow 1   \
| nmrPipe -fn ZF -size 4096                         \
| nmrPipe -fn FT -verb                              \
| nmrPipe -fn PS -p0 0 -p1 0 -di                    \
| nmrPipe -fn TP                                    \
| nmrPipe -fn LP -auto                              \
| nmrPipe -fn SP -c 0.5 -off 0.5 -end 1 -pow 1      \
| nmrPipe -fn ZF -size 4096                         \
| nmrPipe -fn FT -verb                              \
| nmrPipe -fn PS -p0 -90 -p1 0 -di                  \
| nmrPipe -fn POLY -auto -ord 0                     \
| nmrPipe -fn TP                                    \
| nmrPipe -fn POLY -auto -ord 0                     \
| nmrPipe -out cthsqc.ft2 -ov
