#!/bin/tcsh

setenv NAME nhsqc

bruk2pipe -in ser \
  -bad 0.0 -ext -aswap -AMX -decim 2376 -dspfvs 20 -grpdly 67.9872589111328  \
  -xN              1024  -yN               700  \
  -xT               512  -yT               350  \
  -xMODE            DQD  -yMODE    States-TPPI  \
  -xSW         8417.508  -ySW         2979.738  \
  -xOBS         700.183  -yOBS          70.957  \
  -xCAR           4.700  -yCAR         115.000  \
  -xLAB              HN  -yLAB             15N  \
  -ndim               2  -aq2D         Complex  \
  -out ${NAME}.fid -verb -ov

nmrPipe -in ${NAME}.fid				                        \
| nmrPipe -fn SOL				                            \
| nmrPipe -fn SP -c 0.5 -off 0.35 -end 0.95 -size 512	    \
| nmrPipe -fn ZF -size 4096			                        \
| nmrPipe -fn FT -verb				                        \
| nmrPipe -fn PS -p0 0 -p1 0 -di	                	    \
| nmrPipe -fn EXT -x1 6.0ppm -xn 11.0ppm -sw	            \
| nmrPipe -fn TP				                            \
| nmrPipe -fn LP -auto				                        \
| nmrPipe -fn SP -c 0.5 -off 0.5 -end 1 -pow 2 -size 256    \
| nmrPipe -fn ZF -size 1024			                        \
| nmrPipe -fn FT -verb -alt			                        \
| nmrPipe -fn PS -p0 0 -p1 0 -di   		                    \
| nmrPipe -fn POLY -auto -ord 0                             \
| nmrPipe -fn TP				                            \
| nmrPipe -fn POLY -auto -ord 0			                    \
| nmrPipe -out ${NAME}.ft2 -ov
