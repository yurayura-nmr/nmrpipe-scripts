;fhsqccxf3gpph3d
;avance-version (07/04/04)
;fast-HSQC
;2D H-1/X correlation via double inept transfer
;phase sensitive
;with decoupling during acquisition
;using CLEANEX_PM filter for exchanging protons
;as pseudo3D
;
;T.L. Hwang, P.C.M. van Zijl & S. Mori,
;   J. Biomol. NMR 11, 221-226 (1998)
;
;$CLASS=HighRes
;$DIM=2D
;$TYPE=
;$SUBTYPE=
;$COMMENT=


prosol relations=<triple2>


#include <Avance.incl>
#include <Grad.incl>
#include <Delay.incl>


define list<delay> spinlock=<$VDLIST>

"p2=p1*2"
"p22=p21*2"
"d11=30m"
"d12=20u"
"d26=1s/(cnst4*4)"


"in0=inf1/2"

"d0=3u"


"DELTA1=d26-p16-4u"
"DELTA3=p21*2/3.1416"
"DELTA4=d26-p16-d16-p27*3-d19*5"
"DELTA5=d19-p22/2"
"DELTA6=d26-p16-d16-p27*2-p0-d19*5-de-8u"

#   ifdef LABEL_CN
"DELTA2=d0+larger(p2,p14)/2"
#   else
"DELTA2=d0+p2/2"
#   endif /*LABEL_CN*/

"nbl=td1"

"acqt0=0"
baseopt_echo


aqseq 312

1 ze
  d11 pl16:f3 st0
2 6m do:f3
3 6m
4 d1 do:f3
  d12 pl1:f1

  "l1=(spinlock/(p10*8.11))"

  50u UNBLKGRAD
  (p1 ph1)

if "spinlock == 0"
{
  10u
}
else
{
  6u
  p16:gp4
  d16 pl0:f1
  p7:sp21:f1 ph9:r
  p16:gp4
  d16 pl27:f1
  6u gron0
                                                 ;begin CLEANEX_PM
5 (p10*1.500 ph21)
  (p10*1.333 ph23)
  (p10*1.222 ph21)
  (p10*1.222 ph23)
  (p10*1.333 ph21)
  (p10*1.500 ph23)
  lo to 5 times l1
                                                 ;end CLEANEX_PM
  10u groff
}

  p16:gp1
  DELTA1 pl1:f1 pl3:f3
  (center (p2 ph1) (p22 ph6):f3 )
  10u
  p16:gp1
  DELTA1
  (p1 ph2)

  4u
  p16:gp2
  d16

  (p21 ph3):f3
  DELTA2
  (p22 ph3):f3
  DELTA3
  d0

#   ifdef LABEL_CN
  (center (p2 ph5) (p14:sp3 ph1):f2 )
#   else
  (p2 ph5)
#   endif /*LABEL_CN*/

  d0
  DELTA3
  (p22 ph4):f3
  DELTA2
  (p21 ph4):f3

  4u
  p16:gp2
  d16

if "spinlock == 0"
{
  (p1 ph7):f1
}
else
{
  (p1 ph10):f1
}
  DELTA4
  p16:gp3
  d16 pl18:f1
  p27*0.231 ph2
  d19*2
  p27*0.692 ph2
  d19*2
  p27*1.462 ph2
  DELTA5
  (p22 ph1):f3
  DELTA5
  p27*1.462 ph8
  d19*2
  p27*0.692 ph8
  d19*2
  p0*0.231 ph8
  4u
  p16:gp3
  d16
  4u BLKGRAD
  DELTA6 pl16:f3
  goscnp ph31 cpd3:f3

  3m do:f3
  3m st spinlock.inc
  lo to 3 times nbl

  3m spinlock.res
  3m ipp3 ipp4 ipp5 ipp7 ipp9 ipp10 ipp31
  lo to 4 times ns

  d1 mc #0 to 4
     F1QF()
     F2PH(calph(ph3, +90) & calph(ph6, +90) & exec(rppall), caldel(d0, +in0))

exit


ph1=0
ph2=1
ph3=0 2
ph4=0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2
ph5=0 0 0 0 2 2 2 2
ph6=0
ph7=0 0 2 2
ph8=3
ph9=0 0 1 1
ph10=0 0 2 2
ph21=0
ph23=2
ph31=0 2 0 2 0 2 0 2 2 0 2 0 2 0 2 0


;pl0 : 120dB
;pl1 : f1 channel - power level for pulse (default)
;pl3 : f3 channel - power level for pulse (default)
;pl16: f3 channel - power level for CPD/BB decoupling
;pl18: f1 channel - power level for 3-9-19-pulse (watergate)
;pl27: f1 channel - power level for CLEANEX spinlock
;sp3 : f2 channel - shaped pulse 180 degree (adiabatic)
;sp21: f1 channel - shaped pulse 180 degree (H2O on resonance)
;p0 : f1 channel -  90 degree pulse at pl18
;                      use for fine adjustment
;p1 : f1 channel -  90 degree high power pulse
;p2 : f1 channel - 180 degree high power pulse
;p7 : f1 channel - 180 degree shaped pulse (H2O on resonance)  [7.5 ms]
;p10: f1 channel -  90 degree low power pulse (CLEANEX spinlock)
;p14: f2 channel - 180 degree shaped pulse for inversion (adiabatic)
;p16: homospoil/gradient pulse
;p21: f3 channel -  90 degree high power pulse
;p22: f3 channel - 180 degree high power pulse
;p27: f1 channel -  90 degree pulse at pl18
;d0 : incremented delay (2D)                                   [3 usec]
;d1 : relaxation delay; 1-5 * T1
;d11: delay for disk I/O                                       [30 msec]
;d12: delay for power switching                                [20 usec]
;d16: delay for homospoil/gradient recovery
;d19: delay for binomial water suppression
;     d19 = (1/(2*d)), d = distance of next null (in Hz)
;d26: 1/(4J(YH))
;d31: length of CLEANEX spinlock as used
;vdlist: mixing time for CLEANEX spinlock, 0 for reference
;cnst4: = J(YH)
;l1: loop for CLEANEX spinlock: (p10 * 8.11 * l1) = mixing time
;inf1: 1/SW(X) = 2 * DW(X)
;in0: 1/(2 * SW(X)) = DW(X)
;nd0: 2
;NS: 8 * n
;DS: 16
;td1: number of experiments
;FnMODE: States-TPPI (or TPPI)
;cpd3: decoupling according to sequence defined by cpdprg3
;pcpd3: f3 channel - 90 degree pulse for decoupling sequence


;use gradient ratio:          gp 0 : gp 1 : gp 2 : gp 3 : gp 4
;                              0.2 :   50 :   80 :   30 :   19

;for z-only gradients:
;gpz0: 0.2%
;gpz1: 50%
;gpz2: 80%
;gpz3: 30%
;gpz4: 19%

;use gradient files:
;gpnam1: SINE.100
;gpnam2: SINE.100
;gpnam3: SINE.100
;gpnam4: SINE.100


                                          ;preprocessor-flags-start
;LABEL_CN: for C-13 and N-15 labeled samples start experiment with
;             option -DLABEL_CN (eda: ZGOPTNS)
                                          ;preprocessor-flags-end



;$Id: fhsqccxf3gpph,v 1.5 2007/04/11 13:34:29 ber Exp $
