#!/bin/tcsh

# 15N-HSQC

# Optional lines (commented out here) for tricky (low S/N) data
# -size : to specify size of window to optimize signal-to-noise versus resolution
# -fn LP: low quality data might be better without LP

bruk2pipe -in ./ser \
  -bad 0.0 -aswap -DMX -decim 2376 -dspfvs 20 -grpdly 67.9872589111328  \
  -xN              1024  -yN               512  \
  -xT               512  -yT               256  \
  -xMODE            DQD  -yMODE  Echo-AntiEcho  \
  -xSW         8417.508  -ySW         2128.565  \
  -xOBS         700.183  -yOBS          70.957  \
  -xCAR           4.773  -yCAR         119.075  \
  -xLAB              HN  -yLAB             15N  \
  -ndim               2  -aq2D          States  \
  -out ./nhsqc.fid -verb -ov

nmrPipe -in nhsqc.fid \
| nmrPipe -fn SOL                                            \
| nmrPipe -fn SP -c 0.5 -off 0.4 -end 0.95 -pow 1            \
#| nmrPipe -fn SP -c 0.5 -off 0.4 -end 0.95 -pow 1 -size 512 \
| nmrPipe -fn ZF -size 4096                                  \
| nmrPipe -fn FT -verb                                       \
| nmrPipe -fn PS -p0 0 -p1 0 -di                             \
| nmrPipe -fn TP                                             \
#| nmrPipe -fn LP -auto                                      \
| nmrPipe -fn SP -c 0.5 -off 0.5 -end 1 -pow 1               \
#| nmrPipe -fn SP -c 0.5 -off 0.5 -end 1 -pow 1 -size 64     \
| nmrPipe -fn ZF -size 2048                                  \
| nmrPipe -fn FT -verb                                       \
| nmrPipe -fn PS -p0 -90 -p1 0 -di                           \
| nmrPipe -fn POLY -auto -ord 0                              \
| nmrPipe -fn TP                                             \
| nmrPipe -fn POLY -auto -ord 0                              \
#| nmrPipe -fn EXT -left -sw                                 \
| nmrPipe -fn EXT -x1 11.0ppm -xn 6.0ppm -sw                 \
| nmrPipe -out nhsqc.ft2 -ov
