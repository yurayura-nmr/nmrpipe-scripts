;ks_fhsqccxf3gpph3d
;avance-version (10/02/12)
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

"plw0=0"
"plw27=plw1*pow(p1/p10,2)"
"plw16=plw3*pow((p21/pcpd3),2)"                 ; 15N decoupling power
"spw21=plw1*pow((p1/((p7/2)*0.4115776)),2)"     ; Gaus1_180r.1000

"d11=30m"
"d12=20u"
"d26=1s/(cnst4*4)"


"in10=inf2/2"

"d10=3u"



"DELTA=d19-p22/2"
"DELTA1=d26-p16-d16-p1*3-d19*5-p1*2/PI"
"DELTA2=d26-p16-d16-p1*2-p1-d19*5-de-8u"
"DELTA4=p21*2/PI"

#   ifdef LABEL_CN
"DELTA3=d0+larger(p2,p8)/2"
"spw13=plw2*pow((p3/((p8/2)*0.1023327)),2)"     ; 13C 180 adiabatic pulse power
#   else
"DELTA3=d0+p2/2"
#   endif /*LABEL_CN*/

"TAU=d26-p16-10u"

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
  (p1 ph1):f1
if "spinlock == 0"
{
  10u
}
else
{
  6u
  p16:gp4
  d16 pl0:f1
  p7:sp21:f1 ph10:r
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
  TAU pl1:f1 pl3:f3
  (center (p2 ph1) (p22 ph6):f3 )
  10u
  p16:gp1
  TAU
  (p1 ph2)

  4u
  p16:gp2
  d16

  (p21 ph3):f3
  DELTA3
  (p22 ph3):f3
  DELTA4
  d10

#   ifdef LABEL_CN
  (center (p2 ph5) (p8:sp13 ph1):f2 )
#   else
  (p2 ph5)
#   endif /*LABEL_CN*/

  d10
  DELTA4
  (p22 ph4):f3
  DELTA3
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
  (p1 ph11):f1
}
  DELTA1
  p16:gp3
  d16
  p1*0.231 ph8
  d19*2
  p1*0.692 ph8
  d19*2
  p1*1.462 ph8
  DELTA
  (p22 ph1):f3
  DELTA
  p1*1.462 ph9
  d19*2
  p1*0.692 ph9
  d19*2
  p1*0.231 ph9
  4u
  p16:gp3
  d16
  4u BLKGRAD
  DELTA2 pl16:f3
  goscnp ph31 cpd3:f3

  3m do:f3
  3m st spinlock.inc
  lo to 3 times nbl

  3m spinlock.res
  3m ipp3 ipp4 ipp5 ipp7 ipp10 ipp11 ipp31
  lo to 4 times ns

  d1 mc #0 to 4
     F1QF()
     F2PH(calph(ph3, +90) & calph(ph6, +90) & exec(rppall), caldel(d10, +in10))

exit


ph1=0
ph2=1
ph3=0 2
ph4=0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2
ph5=0 0 0 0 2 2 2 2
ph6=0
ph7=2
ph8=1
ph9=3
ph10=0 0 1 1
ph11=0 0 2 2
ph21=0
ph23=2
ph31=0 2 0 2 0 2 0 2 2 0 2 0 2 0 2 0


;pl0 : 0W
;pl1 : f1 channel - power level for pulse (default)
;pl3 : f3 channel - power level for pulse (default)
;pl16: f3 channel - power level for CPD/BB decoupling
;pl27: f1 channel - power level for CLEANEX spinlock
;sp13: f2 channel - shaped pulse 180 degree (adiabatic)
;spnam13: Crp60,0.5,20.1
;sp21: f1 channel - shaped pulse 180 degree (H2O on resonance)
;spnam21: Gaus1_180r.1000
;p1 : f1 channel -  90 degree high power pulse
;p2 : f1 channel - 180 degree high power pulse
;p3 : f2 channel -  90 degree high power pulse
;p7 : f1 channel - 180 degree shaped pulse (H2O on resonance)  [7.5 ms]
;p8 : f2 channel - 180 degree shaped pulse for inversion (adiabatic)
;p10: f1 channel -  90 degree low power pulse (CLEANEX spinlock)
;p16: homospoil/gradient pulse
;p21: f3 channel -  90 degree high power pulse
;p22: f3 channel - 180 degree high power pulse
;d10 : incremented delay (2D)                                   [3 usec]
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
;inf2: 1/SW(X) = 2 * DW(X)
;in10: 1/(2 * SW(X)) = DW(X)
;nd10: 2
;NS: 16 * n
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
;gpnam1: SMSQ10.100
;gpnam2: SMSQ10.100
;gpnam3: SMSQ10.100
;gpnam4: SMSQ10.100


                                          ;preprocessor-flags-start
;LABEL_CN: for C-13 and N-15 labeled samples start experiment with
;             option -DLABEL_CN (eda: ZGOPTNS)
                                          ;preprocessor-flags-end


;$Id: fhsqccxf3gpph,v 1.8 2010/02/12 15:03:55 ber Exp $
