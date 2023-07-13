#!/bin/tcsh

# Lineshape analysis, such as TITAN, requires -fn EM for apodization

setenv NAME nhsqc_1.5eq

bruk2pipe -in ser \
  -bad 0.0 -aswap -DMX -decim 2376 -dspfvs 20 -grpdly 67.9872589111328  \
  -xN              1024  -yN               256  \
  -xT               512  -yT               128  \
  -xMODE            DQD  -yMODE  Echo-AntiEcho  \
  -xSW         8417.508  -ySW         2696.872  \
  -xOBS         700.183  -yOBS          70.957  \
  -xCAR           4.774  -yCAR         119.590  \
  -xLAB              HN  -yLAB             15N  \
  -ndim               2  -aq2D          States  \
  -out ${NAME}.fid -verb -ov

nmrPipe -in ${NAME}.fid                         \
| nmrPipe -fn SOL                               \
| nmrPipe -fn EM -c 0.5 -lb 10                  \
| nmrPipe -fn ZF -size 2048                     \
| nmrPipe -fn FT -verb                          \
| nmrPipe -fn PS -p0 -184.8 -p1 -4.7 -di        \
| nmrPipe -fn POLY -auto -ord 0                 \
| nmrPipe -fn EXT -x1 6.0ppm -xn 10.0ppm -sw    \
| nmrPipe -fn TP                                \
| nmrPipe -fn EM -c 0.5 -lb 20                  \
| nmrPipe -fn ZF -size 2048                     \
| nmrPipe -fn FT -verb                          \
| nmrPipe -fn PS -p0 90 -p1 0 -di               \
| nmrPipe -fn POLY -auto -ord 0                 \
| nmrPipe -fn TP                                \
| nmrPipe -fn POLY -auto -ord 0                 \
| nmrPipe -out ${NAME}.ft2 -ov

pipe2xyz -nv -in ${NAME}.ft2 -out ${NAME}.nv -ov
