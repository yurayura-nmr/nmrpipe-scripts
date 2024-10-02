#!/bin/sh
# usage example
# ft2d_all 700r1
# ft2d_all 700r1 -nv
# ft2d_all 700r1 -ucsf

if [ $# -eq 0 ]
  then
    echo "usage example:"
    echo "    ft2d_all 700r1"
    echo "    ft2d_all 700r1 -nv"
    echo "    ft2d_all 700r1 -uscf"
    exit 0
fi

SPECT_DIR="../spect"
FT_COM="ft.com test"



if [ $# -eq 0 ]; then
	echo "ERROR: specify a prefix of the output file name" 1>&2
	exit 1
fi

if [ ! -e $SPECT_DIR ]; then
	mkdir $SPECT_DIR
fi

# nmrpipe format
for myfile in *.fid
do
	i=${myfile%.*}
	cp $i.fid test.fid
	./$FT_COM
	mv test.ft2  $SPECT_DIR/$1_$i.ft2
done
rm test.fid

if [ $# -eq 2 ]; then
	# ucsf format
	if [ $2 = "-ucsf" ]; then
		cd $SPECT_DIR
		for myfile in *.ft2
		do
			spectnm=${myfile%.*}
			pipe2ucsf $spectnm.ft2 $spectnm.ucsf
		done
		rm -f *.ft2
	fi

	# nv format
	if [ $2 = "-nv" ]; then
		cd $SPECT_DIR
		for myfile in *.ft2
		do
			spectnm=${myfile%.*}
			pipe2xyz -nv -in $spectnm.ft2 -out $spectnm.nv -ov
		done
		rm -f *.ft2
	fi
fi
