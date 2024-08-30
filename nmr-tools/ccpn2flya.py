#!/usr/bin/python3

"""

Erik Walinda
Kyoto University
Graduate School of Medicine

CCPN to FLYA converter
2016/04/29 (First version: python2)
2023/06/05 (Last update : python3)

1) Use Format Converter in CCPN to write XEASY peak lists for each peak-picked spectrum.
   It is not necessary to manually select the "correct order" of axes in FormatConverter, as this is handled by the script.
2) Use this script to convert them to FLYA input peak lists.
   For example:
   ./ccpn2flya.py -hnca HNCA.peaks

# Groups:
#	NHSQC
#	NOESY, HCcoNH, HBHAcoNH
#	CHSQC (ali), CHSQC (aro)

"""

import numpy
import argparse
import os


##############################################################################################

def parseArguments():

    parser = argparse.ArgumentParser(description='CCPN2FLYA dev')

    parser.add_argument("input_file", help="provide an input file", type=str, default='list.in')
    parser.add_argument("-cnoesy_ali", help="Input list is a [13C]-edited aliphatic NOESY experiment", action="store_true")
    parser.add_argument("-cnoesy_aro", help="Input list is a [13C]-edited aromatic NOESY experiment", action="store_true")
    parser.add_argument("-nnoesy", help="Input list is a [15N]-edited NOESY experiment", action="store_true")
    parser.add_argument("-nhsqc", help="Input list is a [1H, 15N]-HSQC experiment", action="store_true")
    parser.add_argument("-hnco", help="Input list is a HNCO experiment", action="store_true")
    parser.add_argument("-hncaco", help="Input list is a HNcaCO experiment", action="store_true")
    parser.add_argument("-hnca", help="Input list is a HNCA experiment", action="store_true")
    parser.add_argument("-hncoca", help="Input list is a HNcoCA experiment", action="store_true")
    parser.add_argument("-hncacb", help="Input list is a HNCACB/CBCANH experiment", action="store_true")
    parser.add_argument("-cbcaconh", help="Input list is a CBCAcoNH experiment", action="store_true")
    parser.add_argument("-chsqc", help="Input list is a [1H, 13C]-HSQC experiment", action="store_true")
    parser.add_argument("-hcconh", help="Input list is a HCcoNH experiment", action="store_true")
    parser.add_argument("-hbhaconh", help="Input list is a HBHAcoNH experiment", action="store_true")
    parser.add_argument("-cconh", help="Input list is a CcoNH experiment", action="store_true")

    args = parser.parse_args()

    return args


##############################################################################################


def readInputPeaklist3D(filename):

    dim_1 = []
    dim_2 = []
    dim_3 = []
    filearray = []

    with open(filename, "rt") as fin:
        for line in fin:
            columns = line.split()
            if '#' in columns[0]:
                pass
            else:
                dim_1.append(float(columns[1]))
                dim_2.append(float(columns[2]))
                dim_3.append(float(columns[3]))
                filearray.append(columns)

    return dim_1, dim_2, dim_3, filearray 


##############################################################################################


def readInputPeaklist2D(filename):

    dim_1 = []
    dim_2 = []
    filearray = []

    with open(filename, "rt") as fin:
        for line in fin:
            columns = line.split()
            if '#' in columns[0]:
                pass
            else:
                dim_1.append(float(columns[1]))
                dim_2.append(float(columns[2]))
                filearray.append(columns)

    return dim_1, dim_2, filearray 


##############################################################################################



def average(dim_array):
    array = numpy.array(dim_array)

    # Calculate average of chemical shift

    return numpy.mean(array)




##############################################################################################

def CNOESY_aro_dimcheck(dim, idx, H, HC, C):

    print(average(dim))    # debug

    if average(dim) < 6:
        print ("Dimension ", str(idx), ": Proton (NOE)")
        H = dim

    elif average(dim) > 100:
        print ("Dimension ", str(idx), ": Aromatic carbon")
        C = dim

    elif average(dim) > 6:
        print ("Dimension ", str(idx), ": Aromatic proton")
        HC = dim

    else:
        print ("Could not determine dimension from input list.")

    return H, HC, C


##############################################################################################


def CNOESY_dimcheck(dim, idx, H, HC, C):

    print (average(dim))    # debug

    if average(dim) > 4:
        if average(dim) < 10:
            print ("Dimension ", str(idx), ": Proton (NOE)")
            H = dim
        elif average(dim) > 30:
            print ("Dimension ", str(idx), ": Aliphatic carbon")
            C = dim

    elif average(dim) < 4:
        print ("Dimension ", str(idx), ": Aliphatic proton")
        HC = dim

    else:
        print ("Could not determine dimension from input list.")

    return H, HC, C


##############################################################################################


def NNOESY_dimcheck(dim, idx, H, HN, N):

    #print average(dim)    # debug

    if average(dim) > 7:
        if average(dim) < 9:
            print ("Dimension ", str(idx), ": Amide proton")
            HN = dim
        elif average(dim) > 100:
            print ("Dimension ", str(idx), ": Amide nitrogen")
            N = dim

    elif average(dim) < 7:
        print ("Dimension ", str(idx), ": Indirect proton (NOE / Sidechain)")
        H = dim

    else:
        print ("Could not determine dimension from input list.")

    return H, HN, N


##############################################################################################

def HNCO_dimcheck(dim, idx, HN, C, N):

    #print average(dim)    # debug

    if average(dim) > 7:
        if average(dim) < 9:
            print ("Dimension ", str(idx), ": Amide proton")
            HN = dim
        elif average(dim) > 150:
            print ("Dimension ", str(idx), ": CO")
            C = dim
        elif average(dim) < 150:
            print ("Dimension ", str(idx), ": Amide nitrogen")
            N = dim
 
    else:
        print ("Could not determine dimension from input list.")

    return HN, C, N


##############################################################################################


def HNCA_dimcheck(dim, idx, HN, C, N):


    if average(dim) > 7:
        if average(dim) < 9:
            print ("Dimension ", str(idx), ": Amide proton")
            HN = dim
        elif average(dim) > 100:
            print ("Dimension ", str(idx), ": Amide nitrogen")
            N = dim
        elif average(dim) < 80:
            print ("Dimension ", str(idx), ": CA")
            C = dim
  
    else:
        print ("Could not determine dimension from input list.")

    return HN, C, N


##############################################################################################


def CHSQC_dimcheck(dim, idx, H, C):

    #print average(dim)    # debug

    if average(dim) < 9:
        print ("Dimension ", str(idx), ": Aliphatic or aromatic proton")
        H = dim
    elif average(dim) > 30:
        print ("Dimension ", str(idx), ": Aliphatic or aromatic carbon")
        C = dim

    else:
        print ("Could not determine dimension from input list.")

    return H, C


##############################################################################################


def NHSQC_dimcheck(dim, idx, H, N):

    #print average(dim)    # debug

    if average(dim) > 7:
        if average(dim) < 9:
            print ("Dimension ", str(idx), ": Amide proton")
            H = dim
        elif average(dim) > 100:
            print ("Dimension ", str(idx), ": Amide nitrogen")
            N = dim

    else:
        print ("Could not determine dimension from input list.")

    return H, N


##############################################################################################



def NHSQC(filename):

    dim_1, dim_2, filearray = readInputPeaklist2D(filename)

    # Initialize empty peak lists

    H = []
    N = []


    # Determine content of each dimension of the input file

    H, N = NHSQC_dimcheck(dim_1, 1, H, N)
    H, N = NHSQC_dimcheck(dim_2, 2, H, N)


    # Write as FLYA format:

    header_1 = '# Number of dimensions 2'
    header_2 = '#FORMAT xeasy2D\n#INAME 1 H\n#INAME 2 N'
    header_3 = '#SPECTRUM N15HSQC H N'

    DIM1 = H
    DIM2 = N

    outfile = './FLYA/N15HSQC.peaks'

    write2D(outfile, header_1, header_2, header_3, DIM1, DIM2, filearray)
    # done


##############################################################################################


def CHSQC(filename):

    dim_1, dim_2, filearray = readInputPeaklist2D(filename)

    # Initialize empty peak lists

    H = []
    C = []


    # Determine content of each dimension of the input file

    H, C = CHSQC_dimcheck(dim_1, 1, H, C)
    H, C = CHSQC_dimcheck(dim_2, 2, H, C)


    # Write as FLYA format:

    header_1 = '# Number of dimensions 2'
    header_2 = '#FORMAT xeasy2D\n#INAME 1 H\n#INAME 2 C'
    header_3 = '#SPECTRUM C13HSQC H C'

    DIM1 = H
    DIM2 = C

    outfile = './FLYA/C13HSQC.peaks'

    write2D(outfile, header_1, header_2, header_3, DIM1, DIM2, filearray)
    # done


##############################################################################################


def HNcaCO(filename):

    dim_1, dim_2, dim_3, filearray = readInputPeaklist3D(filename)


    # Initialize empty peak lists

    HN = []
    C = []
    N = []


    # Determine content of each dimension of the input file
    # can use same function as HNCO

    HN, C, N = HNCO_dimcheck(dim_1, 1, HN, C, N)
    HN, C, N = HNCO_dimcheck(dim_2, 2, HN, C, N)
    HN, C, N = HNCO_dimcheck(dim_3, 3, HN, C, N)


    # Write as FLYA format:

    header_1 = '# Number of dimensions 3'
    header_2 = '#FORMAT xeasy3D\n#INAME 1 H\n#INAME 2 C\n#INAME 3 N'
    header_3 = '#SPECTRUM HNcaCO HN C N'

    DIM1 = HN
    DIM2 = C
    DIM3 = N

    outfile = './FLYA/HNcaCO.peaks'

    write3D(outfile, header_1, header_2, header_3, DIM1, DIM2, DIM3, filearray)
    # done


##############################################################################################


def HNCO(filename):

    dim_1, dim_2, dim_3, filearray = readInputPeaklist3D(filename)


    # Initialize empty peak lists

    HN = []
    C = []
    N = []


    # Determine content of each dimension of the input file

    HN, C, N = HNCO_dimcheck(dim_1, 1, HN, C, N)
    HN, C, N = HNCO_dimcheck(dim_2, 2, HN, C, N)
    HN, C, N = HNCO_dimcheck(dim_3, 3, HN, C, N)


    # Write as FLYA format:

    header_1 = '# Number of dimensions 3'
    header_2 = '#FORMAT xeasy3D\n#INAME1 HN\n#INAME 2 C\n#INAME 3 N'
    header_3 = '#SPECTRUM HNCO HN C N'

    DIM1 = HN
    DIM2 = C
    DIM3 = N

    outfile = './FLYA/HNCO.peaks'

    write3D(outfile, header_1, header_2, header_3, DIM1, DIM2, DIM3, filearray)
    # done


##############################################################################################
##############################################################################################


def HNcoCA(filename):

    dim_1, dim_2, dim_3, filearray = readInputPeaklist3D(filename)


    # Initialize empty peak lists

    HN = []
    C = []
    N = []


    # Determine content of each dimension of the input file

    HN, C, N = HNCA_dimcheck(dim_1, 1, HN, C, N)
    HN, C, N = HNCA_dimcheck(dim_2, 2, HN, C, N)
    HN, C, N = HNCA_dimcheck(dim_3, 3, HN, C, N)


    # Write as FLYA format:

    header_1 = '# Number of dimensions 3'
    header_2 = '#FORMAT xeasy3D\n#INAME1 HN\n#INAME 2 C\n#INAME 3 N'
    header_3 = '#SPECTRUM HNcoCA HN C N'

    DIM1 = HN
    DIM2 = C
    DIM3 = N

    outfile = './FLYA/HNcoCA.peaks'

    write3D(outfile, header_1, header_2, header_3, DIM1, DIM2, DIM3, filearray)
    # done


##############################################################################################


def CcoNH(filename):

    dim_1, dim_2, dim_3, filearray = readInputPeaklist3D(filename)


    # Initialize empty peak lists

    HN = []
    C = []
    N = []


    # Determine content of each dimension of the input file

    HN, C, N = HNCA_dimcheck(dim_1, 1, HN, C, N)
    HN, C, N = HNCA_dimcheck(dim_2, 2, HN, C, N)
    HN, C, N = HNCA_dimcheck(dim_3, 3, HN, C, N)


    # Write as FLYA format:

    header_1 = '# Number of dimensions 3'
    header_2 = '#FORMAT xeasy3D\n#INAME1 HN\n#INAME 2 c\n#INAME 3 S'
    header_3 = '#SPECTRUM CcoNH HN C N'

    DIM1 = HN
    DIM2 = C
    DIM3 = N

    outfile = './FLYA/CcoNH.peaks'

    write3D(outfile, header_1, header_2, header_3, DIM1, DIM2, DIM3, filearray)
    # done


##############################################################################################


def HNCACB(filename):

    dim_1, dim_2, dim_3, filearray = readInputPeaklist3D(filename)


    # Initialize empty peak lists

    HN = []
    C = []
    N = []


    # Determine content of each dimension of the input file

    HN, C, N = HNCA_dimcheck(dim_1, 1, HN, C, N)
    HN, C, N = HNCA_dimcheck(dim_2, 2, HN, C, N)
    HN, C, N = HNCA_dimcheck(dim_3, 3, HN, C, N)


    # Write as FLYA format:

    header_1 = '# Number of dimensions 3'
    header_2 = '#FORMAT xeasy3D\n#INAME1 HN\n#INAME 2 C\n#INAME 3 N'
    header_3 = '#SPECTRUM CBCANH HN C N'

    DIM1 = HN
    DIM2 = C
    DIM3 = N

    outfile = './FLYA/CBCANH.peaks'

    write3D(outfile, header_1, header_2, header_3, DIM1, DIM2, DIM3, filearray)
    # done


##############################################################################################


def CBCAcoNH(filename):

    dim_1, dim_2, dim_3, filearray = readInputPeaklist3D(filename)


    # Initialize empty peak lists

    HN = []
    C = []
    N = []


    # Determine content of each dimension of the input file

    HN, C, N = HNCA_dimcheck(dim_1, 1, HN, C, N)
    HN, C, N = HNCA_dimcheck(dim_2, 2, HN, C, N)
    HN, C, N = HNCA_dimcheck(dim_3, 3, HN, C, N)


    # Write as FLYA format:

    header_1 = '# Number of dimensions 3'
    header_2 = '#FORMAT xeasy3D\n#INAME 1 HN\n#INAME 2 C\n#INAME 3 N'
    header_3 = '#SPECTRUM CBCAcoNH HN C N'

    DIM1 = HN
    DIM2 = C
    DIM3 = N

    outfile = './FLYA/CBCAcoNH.peaks'

    write3D(outfile, header_1, header_2, header_3, DIM1, DIM2, DIM3, filearray)
    # done


##############################################################################################




def HNCA(filename):

    dim_1, dim_2, dim_3, filearray = readInputPeaklist3D(filename)


    # Initialize empty peak lists

    HN = []
    C = []
    N = []


    # Determine content of each dimension of the input file

    HN, C, N = HNCA_dimcheck(dim_1, 1, HN, C, N)
    HN, C, N = HNCA_dimcheck(dim_2, 2, HN, C, N)
    HN, C, N = HNCA_dimcheck(dim_3, 3, HN, C, N)


    # Write as FLYA format:

    header_1 = '# Number of dimensions 3'
    header_2 = '#FORMAT xeasy3D\n#INAME1 HN\n#INAME 2 C\n#INAME 3 N'
    header_3 = '#SPECTRUM HNCA HN C N'

    DIM1 = HN
    DIM2 = C
    DIM3 = N

    outfile = './FLYA/HNCA.peaks'

    write3D(outfile, header_1, header_2, header_3, DIM1, DIM2, DIM3, filearray)
    # done


##############################################################################################


def NNOESY(filename):

    dim_1, dim_2, dim_3, filearray = readInputPeaklist3D(filename)


    # Initialize empty peak lists

    H = []
    HN = []
    N = []


    # Determine content of each dimension of the input file

    H, HN, N = NNOESY_dimcheck(dim_1, 1, H, HN, N)
    H, HN, N = NNOESY_dimcheck(dim_2, 2, H, HN, N)
    H, HN, N = NNOESY_dimcheck(dim_3, 3, H, HN, N)


    # Write as FLYA format:

    header_1 = '# Number of dimensions 3'
    header_2 = '#FORMAT xeasy3D'
    header_3 = '#SPECTRUM N15NOESY HN H N'

    DIM1 = HN
    DIM2 = H
    DIM3 = N

    outfile = './FLYA/N15NOESY.peaks'

    write3D(outfile, header_1, header_2, header_3, DIM1, DIM2, DIM3, filearray)
    # done


##############################################################################################


def HCcoNH(filename):

    dim_1, dim_2, dim_3, filearray = readInputPeaklist3D(filename)


    # Initialize empty peak lists

    H = []
    HN = []
    N = []


    # Determine content of each dimension of the input file

    H, HN, N = NNOESY_dimcheck(dim_1, 1, H, HN, N)
    H, HN, N = NNOESY_dimcheck(dim_2, 2, H, HN, N)
    H, HN, N = NNOESY_dimcheck(dim_3, 3, H, HN, N)


    # Write as FLYA format:

    header_1 = '# Number of dimensions 3'
    header_2 = '#FORMAT xeasy3D\n#INAME 1 H\n#INAME 2 h\n#INAME 3 N'
    header_3 = '#SPECTRUM HCcoNH HN H N'

    DIM1 = HN
    DIM2 = H
    DIM3 = N

    outfile = './FLYA/HCcoNH.peaks'

    write3D(outfile, header_1, header_2, header_3, DIM1, DIM2, DIM3, filearray)
    # done


##############################################################################################


def HBHAcoNH(filename):

    dim_1, dim_2, dim_3, filearray = readInputPeaklist3D(filename)


    # Initialize empty peak lists

    H = []
    HN = []
    N = []


    # Determine content of each dimension of the input file

    H, HN, N = NNOESY_dimcheck(dim_1, 1, H, HN, N)
    H, HN, N = NNOESY_dimcheck(dim_2, 2, H, HN, N)
    H, HN, N = NNOESY_dimcheck(dim_3, 3, H, HN, N)


    # Write as FLYA format:

    header_1 = '# Number of dimensions 3'
    header_2 = '#FORMAT xeasy3D\n#INAME 1 H\n#INAME 2 h\n#INAME 3 N'
    header_3 = '#SPECTRUM HBHAcoNH HN H N'

    DIM1 = HN
    DIM2 = H
    DIM3 = N

    outfile = './FLYA/HBHAcoNH.peaks'

    write3D(outfile, header_1, header_2, header_3, DIM1, DIM2, DIM3, filearray)
    # done


##############################################################################################

def CNOESY_ali(filename):

    dim_1, dim_2, dim_3, filearray = readInputPeaklist3D(filename)


    # Initialize empty peak lists

    H = []
    HC = []
    C = []


    # Determine content of each dimension of the input file

    H, HC, C = CNOESY_dimcheck(dim_1, 1, H, HC, C)
    H, HC, C = CNOESY_dimcheck(dim_2, 2, H, HC, C)
    H, HC, C = CNOESY_dimcheck(dim_3, 3, H, HC, C)


    # Write as FLYA format:

    header_1 = '# Number of dimensions 3'
    header_2 = '#FORMAT xeasy3D\n#INAME 1 H\n#INAME 2 h\n#INAME 3 C'
    header_3 = '#SPECTRUM C13NOESY HC H C'

    DIM1 = HC
    DIM2 = H
    DIM3 = C

    outfile = './FLYA/C13NOESY_ali.peaks'

    write3D(outfile, header_1, header_2, header_3, DIM1, DIM2, DIM3, filearray)
    # done


##############################################################################################


def CNOESY_aro(filename):

    dim_1, dim_2, dim_3, filearray = readInputPeaklist3D(filename)


    # Initialize empty peak lists

    H = []
    HC = []
    C = []


    # Determine content of each dimension of the input file

    H, HC, C = CNOESY_aro_dimcheck(dim_1, 1, H, HC, C)
    H, HC, C = CNOESY_aro_dimcheck(dim_2, 2, H, HC, C)
    H, HC, C = CNOESY_aro_dimcheck(dim_3, 3, H, HC, C)


    # Write as FLYA format:

    header_1 = '# Number of dimensions 3'
    header_2 = '#FORMAT xeasy3D\n#INAME 1 H\n#INAME 2 h\n#INAME 3 C'
    header_3 = '#SPECTRUM C13NOESY HC H C'

    DIM1 = HC
    DIM2 = H
    DIM3 = C

    outfile = './FLYA/C13NOESY_aro.peaks'

    write3D(outfile, header_1, header_2, header_3, DIM1, DIM2, DIM3, filearray)
    # done


#####



def write2D(outfile, header_1, header_2, header_3, DIM1, DIM2, filearray):

    with open(outfile, "wt") as fout:
        fout.write(header_1 + '\n')
        fout.write(header_2 + '\n')
        fout.write(header_3 + '\n')

        for i in range(len(filearray)):
            fout.write(str(filearray[i][0]).rjust(7))		# Peak Number
            fout.write(str(DIM1[i]).rjust(11))			# w(HN)
            fout.write(str(DIM2[i]).rjust(11))			# w(H)
            fout.write(str(filearray[i][3]).rjust(7))		# Peak Number
            fout.write(str(filearray[i][4]).rjust(7))		# Peak Number
            fout.write(str(filearray[i][5]).rjust(12))		# Peak Number
            fout.write(str(filearray[i][6]).rjust(12))		# Peak Number
            fout.write(str(filearray[i][7]).rjust(3))		# Peak Number
            fout.write(str(filearray[i][8]).rjust(3))		# Peak Number
            fout.write(str(filearray[i][9]).rjust(3))		# Peak Number
            fout.write(str(filearray[i][10]).rjust(3))		# Peak Number
            fout.write(str(filearray[i][11]).rjust(3))	 	# Peak Number
            fout.write('\n')

    fout.close()


##############################################################################################


def write3D(outfile, header_1, header_2, header_3, DIM1, DIM2, DIM3, filearray):

    with open(outfile, "wt") as fout:
        fout.write(header_1 + '\n')
        fout.write(header_2 + '\n')
        fout.write(header_3 + '\n')

        for i in range(len(filearray)):
            fout.write(str(filearray[i][0]).rjust(7))		# Peak Number
            fout.write(str(DIM1[i]).rjust(11))			# w(HN)
            fout.write(str(DIM2[i]).rjust(11))			# w(H)
            fout.write(str(DIM3[i]).rjust(11))			# w(N)
            fout.write(str(filearray[i][4]).rjust(7))		# Peak Number
            fout.write(str(filearray[i][5]).rjust(7))		# Peak Number
            fout.write(str(filearray[i][6]).rjust(12))		# Peak Number
            fout.write(str(filearray[i][7]).rjust(12))		# Peak Number
            fout.write(str(filearray[i][8]).rjust(3))		# Peak Number
            fout.write(str(filearray[i][9]).rjust(3))		# Peak Number
            fout.write(str(filearray[i][10]).rjust(3))		# Peak Number
            fout.write(str(filearray[i][11]).rjust(3))		# Peak Number
            fout.write(str(filearray[i][12]).rjust(3))	 	# Peak Number
            fout.write('\n')

    fout.close()


##############################################################################################


def main():

    args = parseArguments()

    os.system('mkdir FLYA')

    if args.nnoesy:
        NNOESY(args.input_file)       
    if args.nhsqc:
        NHSQC(args.input_file)        
    if args.hnco:
        HNCO(args.input_file)         
    if args.hncaco:
        HNcaCO(args.input_file)       
    if args.hnca:
        HNCA(args.input_file)         
    if args.hncoca:
        HNcoCA(args.input_file)         
    if args.hncacb:
        HNCACB(args.input_file)         
    if args.chsqc:
        CHSQC(args.input_file)         
    if args.hcconh:
        HCcoNH(args.input_file)         
    if args.cbcaconh:
        CBCAcoNH(args.input_file)         
    if args.hbhaconh:
        HBHAcoNH(args.input_file)         
    if args.cconh:
        CcoNH(args.input_file)         
    if args.cnoesy_ali:
        CNOESY_ali(args.input_file)         
    if args.cnoesy_aro:
        CNOESY_aro(args.input_file)         


##############################################################################################


main()
