#!/bin/tcsh

setenv NAME cbcaconh

rm -f fid/*.ft3

xyz2pipe -in fid/${NAME}%03d.fid -z		        \
| nmrPipe -fn ZTP			                        \
| pipe2xyz -out fid/${NAME}%03d.ft3 -z -ov

xyz2pipe -in fid/${NAME}%03d.ft3 -x		          \
| nmrPipe -fn SOL				                        \    
| nmrPipe -fn SP -c 0.5 -off 0.35 -end 0.95	    \  
| nmrPipe -fn ZF -auto				                  \
| nmrPipe -fn FT -verb				                  \
| nmrPipe -fn PS -p0 0 -p1 0 -di		            \
| nmrPipe -fn POLY -auto -ord 0			            \
| nmrPipe -fn EXT -x1 6.3ppm -xn 11ppm -sw	    \
| pipe2xyz -out fid/${NAME}%03d.ft3 -x

xyz2pipe -in fid/${NAME}%03d.ft3 -z		          \
| nmrPipe -fn ZF -auto				                  \
| nmrPipe -fn FT -verb				                  \
| nmrPipe -fn PS -p0 0 -p1 0 -di   		          \
| nmrPipe -fn POLY -auto -ord 0                 \
| pipe2xyz -out fid/${NAME}%03d.ft3 -z -inPlace

xyz2pipe -in fid/${NAME}%03d.ft3 -y		          \
| nmrPipe -fn LP -f -auto 			                \
| nmrPipe -fn SP -c 0.5 -off 0.5 -end 1 -pow 2	\
| nmrPipe -fn ZF -auto				                  \
| nmrPipe -fn FT -alt -verb			                \
| nmrPipe -fn PS -p0 2 -p1 9 -di		            \
| nmrPipe -fn POLY -auto -ord 0                 \
| pipe2xyz -out fid/${NAME}%03d.ft3 -y -inPlace

xyz2pipe -in fid/${NAME}%03d.ft3 -z		          \
| nmrPipe -fn HT -auto				                  \
| nmrPipe -fn PS -inv -hdr			                \
| nmrPipe -fn FT -inv 				                  \
| nmrPipe -fn ZF -inv				                    \
| nmrPipe -fn LP -fb -auto 			                \
| nmrPipe -fn SP -c 0.5 -off 0.5 -end 1 -pow 2	\
| nmrPipe -fn ZF -auto				                  \
| nmrPipe -fn FT -verb				                  \
| nmrPipe -fn PS -hdr -di			                  \
| nmrPipe -fn POLY -auto -ord 0			            \
| pipe2xyz -out fid/${NAME}%03d.ft3 -z -inPlace

xyz2pipe -x -in fid/${NAME}%03d.ft3		          \
| nmrPipe -fn ZTP				                        \
| nmrPipe -fn POLY -auto -ord 0			            \
| nmrPipe -fn ZTP				                        \
| nmrPipe -fn POLY -auto -ord 0			            \
| pipe2xyz -x -out fid/${NAME}%03d.ft3 -inPlace

xyz2pipe -x -in fid/${NAME}%03d.ft3		          \
| pipe2xyz -nv -out ./${NAME}.nv

xyz2pipe -in fid/${NAME}%03d.ft3 -x > ${NAME}.ft

proj3D.tcl -in fid/${NAME}%03d.ft3
