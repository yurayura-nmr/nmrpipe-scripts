#!/bin/csh

setenv FILE $argv[1]

nmrPipe -in ${FILE}.fid					\
| nmrPipe -fn SOL					\
| nmrPipe -fn SP -c 0.5 -off 0.45 -end 0.98 -pow 1	\
| nmrPipe -fn ZF -auto					\
| nmrPipe -fn FT					\
| nmrPipe -fn PS -p0 205 -p1 -5 -di			\
| nmrPipe -fn TP					\
| nmrPipe -fn SP -c 0.5 -off 0.5 -end 1 -pow 2		\
| nmrPipe -fn ZF -auto					\
| nmrPipe -fn FT 					\
| nmrPipe -fn PS -p0 -90 -p1 0 -di			\
| nmrPipe -fn POLY -auto -ord 0				\
| nmrPipe -fn TP					\
| nmrPipe -fn POLY -auto -ord 0				\
| nmrPipe -fn EXT -x1 5.7ppm -xn 9.7ppm -sw		\
| nmrPipe -out ${FILE}.ft2 -ov

#pipe2xyz -nv -in ${FILE}.ft2 -out ${FILE}.nv -ov
#pipe2ucsf ${FILE}.ft2 ${FILE}.ucsf
