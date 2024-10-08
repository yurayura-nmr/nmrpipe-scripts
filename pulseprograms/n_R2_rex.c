;hsqcNr2rex3d
;
;avance-version (05/23/2017)
;2D H-1/N-15 correlation via double inept transfer
;   using sensitivity improvement
;for measuring N-15 R(exchange) using a CPMG train
;phase sensitive using Echo/Antiecho-TPPI gradient selection
;with decoupling during acquisition
;using f3 - channel
;acquisition as pseudo-3D
;
;D.F. Hansen, P. Vallurupalli, and L.E. Kay
;  J. Phys. Chem. B, 2008, 112 (19), 5898-5904
;B. Jiang, B. Yu, X. Zhang, M. Liu, and D. Yang
;  J. Magn. Reson., 2015, 257, 1-7
;
;$CLASS=HighRes
;$DIM=3D
;$TYPE=
;$SUBTYPE=
;$COMMENT=



#include <Avance.incl>
#include <Grad.incl>
#include <Delay.incl>


define list<loopcounter> vc=<$VCLIST>

"p2=p1*2"
"p22=p21*2"

;"plw0=0"
;"plw16=plw3*pow((p21/pcpd3),2)"                        ; 15N decoupling power
;"plw19=plw1*pow((p1/p26),2)"                   ; 1H decoupling power
;"spw1=plw1*pow((p1/(p11*0.5889)),2)"           ; Water-flip-back pulse power

"d11=30m"

"d10=3u"
"in10=inf2/2"

;"l11=0"

define loopcounter L_Heat
define loopcounter L_CPMG
"d24=2.68817ms"
define delay Heat
define delay Teq
define delay Chi
define delay Zeta
"Heat=80ms"                                     ; Heat compensation delay
"Teq=5ms"
"Zeta=p21-p1*2/3.1416+4u"
"DELTA=p11*2+d20+28u"
"DELTA1=d1-Heat-DELTA-50u"
"DELTA2=Teq-p16-d16-4u"
"DELTA3=d24-p16-d16"

#   ifdef LABEL_CN
"DELTA4=d24-p16-d16-larger(p2,p8)-d10*2-8u"
;"spw13=plw2*pow((p3/((p8/2)*0.1023327)),2)"    ; 13C 180 adiabatic pulse power
#   else
"DELTA4=d24-p16-d16-p2-d10*2-8u"
#   endif /*LABEL_CN*/

"DELTA5=p16+d16+4u"
"DELTA6=d24-p16-d16"

"cnst3=300"

"acqt0=0"
;baseopt_echo

aqseq 312


1 ze
  d11 pl16:f3 st0
2 6m do:f3
3 6m
4 d11 do:f3
  4u
;******************************************** heat compensation

;  "vc.idx=l11"
  "L_CPMG=vc"

  "L_Heat=(l3-vc+1)*2"
  "TAU=(Heat/(2*L_Heat))-p21"

  if "p26 < p1*2"
  {
        "Chi=0u"
  }
  else
  {
        "Chi=p26*2/3.1416-p1*4/3.1416"
  }
  if (vc == 0)
  {
        4u pl0:f1 fq=cnst3 (bf ppm):f1
        (p11:sp1 ph1):f1
        4u
        4u pl19:f1
        d20 cpds1:f1 ph0
        4u do:f1
        4u pl0:f1
        (p11:sp1 ph3):f1
        4u
        4u pl1:f1 fq=0 (sfo hz):f1
  }
  else
  {
        DELTA
  }
  DELTA1 pl3:f3
5 TAU
                                (p22 ph0):f3
  TAU
  lo to 5 times L_Heat
  50u UNBLKGRAD
;********************************************
                                (p21 ph0):f3
  p16:gp6
  d16 pl0:f1
  (p11:sp1 ph3):f1
  4u
  4u pl1:f1
;******************************************** refocused INEPT
  (p1 ph0):f1
  d26
  (center (p2 ph0):f1           (p22 ph0):f3 )
  d26
  (center (p1 ph1):f1           (p21 ph4):f3 )
  d24
  (center (p2 ph0):f1           (p22 ph0):f3 )
  d24
  (center (p2 ph0):f1           (p21 ph1):f3 )
;********************************************
  p16:gp1
  d16
  DELTA2
  4u fq=cnst19 (bf ppm):f1
  (p1 ph11):f1
  Chi
  (p1 ph0):f1
  if "L_CPMG==1"
  {
        "TAU1=(d20/4)-p21"
        Zeta
        (p2 ph11):f1
        4u pl19:f1
                                        (p21 ph0):f3
        ;******************************************** Begin CW CPMG
        4u cpds1:f1 ph0
        TAU1
                                        (p22 ph20):f3
        TAU1
        TAU1
                                        (p22 ph20):f3
        TAU1
        4u do:f1
        ;******************************************** End CW CPMG
                                        (p21 ph0):f3
        4u pl1:f1
        (p2 ph12):f1
        Zeta
  }
  else
  {
  Zeta rpp20
  (p2 ph11):f1
  4u pl19:f1
                                (p21 ph0):f3
;******************************************** Begin CW CPMG
  if "L_CPMG==0" goto 7
        "TAU1=(d20/(4*vc))-p21"
  4u cpds1:f1 ph0
6 TAU1
                                (p22 ph20):f3
  TAU1 ipp20
  TAU1
                                (p22 ph20):f3
  TAU1 ipp20
  lo to 6 times L_CPMG
  4u do:f1
;******************************************** End CW CPMG
7                               (p21 ph0):f3
  4u pl1:f1
  (p2 ph12):f1
  Zeta
  }
  (p1 ph0):f1
  Chi
  (p1 ph12):f1
  4u fq=0 (sfo hz):f1
  DELTA2
  p16:gp7
  d16
                                (p21 ph1):f3
;******************************************** 15N chemical shift evolution + INEPT
  p16:gp2*-1*EA
  d16 pl1:f1
  DELTA3
                                (p22 ph7):f3
  d10 gron0*-1
  4u groff

#   ifdef LABEL_CN
  (center (p2 ph0):f1                           (p8:sp13 ph0):f2 )
#   else
  (p2 ph0):f1
#   endif /*LABEL_CN*/

  d10 gron0
  4u groff
  p16:gp2*EA
  d16
  DELTA4
;******************************************** PEP
  (center (p1 ph2):f1           (p21 ph6):f3 )
  p16:gp4
  d16
  DELTA6
  (center (p2 ph0):f1           (p22 ph0):f3 )
  DELTA6
  p16:gp4
  d16
  (center (p1 ph1):f1           (p21 ph5):f3 )
  p16:gp5
  d16
  DELTA6
  (center (p2 ph0):f1           (p22 ph0):f3 )
  DELTA6
  p16:gp5
  d16
  (p1 ph0):f1
  DELTA5
  (p2 ph0):f1
  p16:gp3
  d16 pl16:f3
  4u BLKGRAD

  goscnp ph31 cpd3:f3

  3m do:f3
  3m st vc.inc rpp20
  lo to 3 times nbl

  3m vc.res
  3m ipp4 ipp5 ipp6 ipp7 ipp11 ipp12 ipp31
  lo to 4 times ns

  d11 mc #0 to 4
     F1QF()
     F2EA(igrad EA & ip5*2 & rpp4 rpp5 rpp6 rpp7 rpp11 rpp12 rpp31, id10 & ip4*2 & ip31*2)


exit

ph0 = 0
ph1 = 1
ph2 = 2
ph3 = 3
ph4 = 0 2
ph5 = 3 3 1 1
ph6 = 0 0 2 2
ph7 = 0 0 0 0 2 2 2 2
ph11= 1 1 3 3
ph12= 3 3 1 1
ph20= 1 1 0 2
ph31= 0 2 2 0

;pl1 : f1 channel - power level for pulse (default)
;pl2 : f2 channel - power level for pulse (default)
;pl3 : f3 channel - power level for pulse (default)
;pl16: f3 channel - power level for CPD/BB decoupling
;pl19: f1 channel - power level for CPD/BB decoupling  [~15kHz]
;sp1 : f1 channel - shaped pulse  90 degree
;spnam1: Sinc1.1000
;sp13: f2 channel - shaped pulse 180 degree (adiabatic)
;spnam13: Crp60,0.5,20.1
;p1 : f1 channel -  90 degree high power pulse
;p2 : f1 channel - 180 degree high power pulse
;p3 : f2 channel -  90 degree high power pulse
;p8 : f2 channel - 180 degree shaped pulse for inversion (adiabatic)
;p11: f1 channel -  90 degree shaped pulse
;p16: homospoil/gradient pulse                         [1 msec]
;p21: f3 channel -  90 degree high power pulse
;p22: f3 channel - 180 degree high power pulse
;p26: f1 channel -  90 degree pulse at pl19            [16.67 us]
;d1 : relaxation delay; 1-5 * T1
;d10 : incremented delay
;d11: delay for disk I/O                               [30 msec]
;d16: delay for homospoil/gradient recovery
;d20: constant CPMG time                               [20-80 msec]
;d24: 1/(4J(NH))                                       [2.688 msec]
;d26: 1/(4J(NH))                                       [2.688 msec]
;cnst19: center of amide 1H in ppm                     [8.1-8.5 ppm]
;l3: l3 >= maximum vc
;inf2: 1/SW(N) = 2 * DW(N)
;in10: 1/(2 * SW(N)) = DW(N)
;nd10: 2
;NS: 4 * n
;DS: >= 16
;td1: number of frequencies in vc-list
;td2: number of experiments in F2
;NBL: = td1
;FnMODE: QF in F1
;FnMODE: Echo-Antiecho in F2
;cpd3: decoupling according to sequence defined by cpdprg3
;pcpd3: f3 channel - 90 degree pulse for decoupling sequence


;use gradient ratio:  gp 0 : gp 1 : gp 2 : gp 3 : gp 4 : gp 5 : gp 6 : gp 7
;                      0.2 :  -40 :   80 : 16.2 :    5 :   -2 :    6 :   40

;for z-only gradients:
;gpz0:  0.2%
;gpz1:  -40%
;gpz2:   80%
;gpz3: 16.2%
;gpz4:    5%
;gpz5:   -2%
;gpz6:    6%
;gpz7:   40%

;use gradient files:
;gpnam1: SMSQ10.100
;gpnam2: SMSQ10.100
;gpnam3: SMSQ10.100
;gpnam4: SMSQ10.100
;gpnam5: SMSQ10.100
;gpnam6: SMSQ10.100
;gpnam7: SMSQ10.100
;gpnam8: SMSQ10.100

                                          ;preprocessor-flags-start
;LABEL_CN: for C-13 and N-15 labeled samples start experiment with
;             option -DLABEL_CN (eda: ZGOPTNS)
                                          ;preprocessor-flags-end
