#!/bin/csh

bruk2pipe -in ./fid \
  -bad 0.0 -noaswap -DMX -decim 16 -dspfvs 12 -grpdly -1  \
  -xN              8192  \
  -xT              4096  \
  -xMODE            DQD  \
  -xSW         9615.385  \
  -xOBS         600.133  \
  -xCAR          4.6729  \
  -xLAB              1H  \
  -ndim               1  \
  -out ./dss.fid -verb -ov

nmrPipe -in dss.fid					                \
| nmrPipe -fn SOL					                \
| nmrPipe -fn SP -c 0.5 -off 0.4 -end 0.95 -pow 2	\
| nmrPipe -fn ZF -auto					            \
| nmrPipe -fn FT -verb					            \
| nmrPipe -fn PS -p0 -0 -p1 0 -di			        \
| nmrPipe -fn POLY -auto -ord 2				        \
| nmrPipe -out dss.ft -ov
