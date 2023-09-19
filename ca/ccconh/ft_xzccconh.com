#!/bin/csh

setenv NAME ccconh

$NMRTXT/ext.xz.com fid/${NAME}%03d.fid fid/${NAME}_1xz.fid
$NMRTXT/ext.xz.com fid/${NAME}%03d.fid fid/${NAME}_1xz.fid 2
 
nmrPipe -in fid/${NAME}_1xz.fid			\
| nmrPipe -fn SOL				\
| nmrPipe -fn SP -c 0.5 -off 0.35 -end 0.95	\
| nmrPipe -fn ZF -auto				\
| nmrPipe -fn FT -verb				\
| nmrPipe -fn PS -p0 -32 -p1 0 -di		\
| nmrPipe -fn POLY -auto -ord 0			\
| nmrPipe -fn EXT -x1 6.3ppm -xn 10.5ppm -sw	\
| nmrPipe -fn TP				\
| nmrPipe -fn LP -f -auto			\
| nmrPipe -fn SP -c 0.5 -off 0.5 -end 1 -pow 2 	\
| nmrPipe -fn FT -alt -verb			\
| nmrPipe -fn PS -p0 -14 -p1 34 -di		\
| nmrPipe -fn POLY -auto -ord 0			\
| nmrPipe -fn TP				\
| nmrPipe -fn POLY -auto -ord 0			\
| nmrPipe -out xz.ft2 -ov
