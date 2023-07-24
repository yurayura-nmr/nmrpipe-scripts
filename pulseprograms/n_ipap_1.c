;hsqcf3gpiaphsiwg
;avance-version (10/02/12)
;HSQC - DSSE (IPAP)
;2D H-1/X correlation via double inept transfer
;phase sensitive
;with decoupling during acquisition
;using f3 - channel
;using flip-back pulse
;water suppression using watergate sequence
;
;F. Cordier, A.J. Dingley & S. Grzesiek, J. Biomol. NMR 13, 175-180 (1999)
;
;$CLASS=HighRes
;$DIM=2D
;$TYPE=
;$SUBTYPE=
;$COMMENT=


prosol relations=<triple>


#include <Avance.incl>
#include <Delay.incl>
#include <Grad.incl>


"p2=p1*2"
"p22=p21*2"
"d11=30m"
"d26=1s/(cnst4*4)"


"d0=3u"

"in0=inf1"


"DELTA1=d24-p16-d16-d0-p1"
"DELTA2=d24-p16-d16"
"DELTA3=d24-p19-p11*2-12u"
"DELTA4=d24-p19-p11-8u"


1 ze 
  d11 pl16:f3
2 d11 do:f3
3 d1 pl1:f1 pl3:f3
  50u UNBLKGRAD

  (p1 ph1)
  d26
  (center (p2 ph2) (p22 ph1):f3 )
  d26
  (p1 ph2)

  4u pl0:f1
  (p11:sp1 ph7:r):f1
  4u
  p16:gp1
  d16 pl1:f1

  (p21 ph3):f3
  d0

  (p1 ph2)
  p16:gp2
  d16
  DELTA1
  (center (p2 ph2) (p22 ph2):f3 )
  DELTA2
  p16:gp2
  d16

  (center (p1 ph4) (p21 ph5):f3 )

  4u pl0:f1
  (p11:sp1 ph2:r):f1
  p19:gp3
  DELTA3 pl0:f1
  (p11:sp1 ph7:r):f1
  4u
  4u pl1:f1
  (center (p2 ph1) (p22 ph1):f3 )
  4u pl0:f1
  (p11:sp1 ph7:r):f1
  p19:gp3
  DELTA4 pl16:f3
  4u BLKGRAD

  go=2 ph31 cpd3:f3
  d11 do:f3 mc #0 to 2 
     F1I(ip4*2 & ip5*2, 2)
     F1PH(calph(ph3, +90), caldel(d0, +in0))
exit 
  

ph1=0
ph2=1
ph3=0 2
ph4=2
ph5=3
ph6=2 0
ph7=2
ph31=0 2


;pl0 : 0W
;pl1 : f1 channel - power level for pulse (default)
;pl3 : f3 channel - power level for pulse (default)
;pl16: f3 channel - power level for CPD/BB decoupling
;sp1: f1 channel - shaped pulse  90 degree
;p1 : f1 channel -  90 degree high power pulse
;p2 : f1 channel - 180 degree high power pulse
;p11: f1 channel -  90 degree shaped pulse
;p16: homospoil/gradient pulse                       [1 msec]
;p19: gradient pulse 2                               [500 usec]
;p21: f3 channel -  90 degree high power pulse
;p22: f3 channel - 180 degree high power pulse
;d0 : incremented delay (2D)                         [3 usec]
;d1 : relaxation delay; 1-5 * T1
;d11: delay for disk I/O                             [30 msec]
;d16: delay for homospoil/gradient recovery
;d24: 1/(4J')NH                                      [2.7 msec]
;d26: 1/(4J)NH                                       [2.25 msec]
;cnst4: = J(NH)
;inf1: 1/SW(X) = 2 * DW(X)
;in0: 1/SW(X)) = 2 * DW(X)
;nd0: 1
;NS: 2 * n
;DS: 32
;td1: number of experiments
;FnMODE: States-TPPI, TPPI, States or QSEQ
;cpd3: decoupling according to sequence defined by cpdprg3
;pcpd3: f3 channel - 90 degree pulse for decoupling sequence


;use gradient ratio:    gp 1 : gp 2 : gp 3
;                         70 :   11 :   35

;for z-only gradients:
;gpz1: 70%
;gpz2: 11%
;gpz3: 35%

;use gradient files:   
;gpnam1: SMSQ10.100
;gpnam2: SMSQ10.100
;gpnam3: SMSQ10.50


;use AU-program splitipap2 to split data



;$Id: hsqcf3gpiaphsiwg,v 1.7 2010/02/12 15:03:55 ber Exp $
