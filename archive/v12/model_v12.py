#!/usr/bin/env python3
"""
v12: DIC Model — JOINT FIT, Diagnostic-Informed Architecture
==============================================================
Based on G1 vs G2 diagnostic comparison (v11.2).

Key findings incorporated:
  1. kr differs 6× (myelosan accelerates neutrophil clearance)
     → kr_g2 = kr · km, km > 1
  2. tp2 differs 2.3× (shorter inflammatory peak in G2)
     → tp2_g2 = tp2 · tm, 0 < tm < 1
  3. af/cf INVERSION is biological: fib procoag is 76% neutrophil-dependent
     → Strong mechanism-split constraint (W=2.0)
  4. dr/dt = 0 (recalc/thrombin have no Hc term) — confirmed in 4+ runs
  5. Identical between groups: krl, kcl, knd, Hm, s2, bt, df

  27 params = 25 shared + km (myelosan kr modifier) + tm (myelosan tp2 modifier)
  150 datapoints (96 G1 + 54 G2), ratio = 5.6

ODE: 5 states [D, AP, Hc, Hn, X]
  Group differences enter ONLY through:
    - N(t): neutrophil input (measured data)
    - kr_eff = kr·km for G2 (myelosan effect on neutrophil survival)
    - tp2_eff = tp2·tm for G2 (shortened inflammatory response)
  All other parameters are SHARED.

Usage:
  python model_v12.py --quick
  python model_v12.py
"""

import numpy as np
from scipy.integrate import odeint
from scipy.optimize import differential_evolution, minimize
from scipy.interpolate import interp1d
import pickle, time, sys, os

# ================================================================
#  DATA
# ================================================================

T1 = np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,19], dtype=float)
RECALC1 = np.array([0,-38.5,-40.9,-37.8,-22.5,-2.0,5.0,13.6,17.3,148.3,166.3,206.7,110.0,56.8,47.3,6.3])
THROMB1 = np.array([0,-5.6,-4.9,-3.0,-3.5,0.4,1.2,1.5,2.8,7.3,11.6,15.6,12.5,6.2,3.4,0.2])
FIB1    = np.array([0,28.0,31.7,24.0,11.2,-22.9,-26.8,-33.5,-39.1,-44.8,-46.8,-52.6,-40.6,-35.8,-34.1,-2.2])
XIII1   = np.array([0,71.0,72.0,56.0,47.5,5.4,-4.7,-12.3,-20.6,-65.9,-69.1,-76.7,-63.4,-49.3,-40.7,-5.7])
AP1     = np.array([0,0.22,0.36,0.48,0.51,0.38,0.42,0.50,0.54,0.58,0.62,0.84,0.54,0.44,0.31,0.07])
DEG1    = np.array([0,20.7,31.2,35.6,35.8,40.2,40.2,38.6,40.8,51.9,57.0,60.5,58.1,56.5,49.3,8.6])
N1_DATA = np.array([7.3,9.2,9.0,9.3,9.6,8.3,7.8,8.5,9.6,9.7,11.0,11.2,11.0,8.7,8.0,7.6])

T2 = np.array([0,1,2,3,4,5,6,7,8], dtype=float)
RECALC2 = np.array([0,-29.3,-23.3,1.5,9.1,6.7,-0.1,-0.3,-0.5])
THROMB2 = np.array([0,-5.1,-4.4,-2.1,-0.2,1.3,0.5,0.2,-0.1])
FIB2    = np.array([0,6.7,21.8,9.5,-9.6,-3.9,3.9,1.2,0.8])
XIII2   = np.array([0,12.8,10.2,2.5,-9.3,-4.9,2.0,1.8,1.5])
AP2     = np.array([0,0.12,0.22,0.33,0.30,0.25,0.20,0.14,0.07])
DEG2    = np.array([0,8.3,18.6,23.7,24.6,27.3,29.6,19.7,1.8])
N2_DATA = np.array([3.9,3.65,3.78,3.40,3.20,3.30,3.50,3.58,3.73])

N1_BASE = 7.3

_N1 = interp1d(T1, N1_DATA, kind='linear', bounds_error=False, fill_value=(N1_DATA[0],N1_DATA[-1]))
_N2 = interp1d(T2, N2_DATA, kind='linear', bounds_error=False, fill_value=(N2_DATA[0],N2_DATA[-1]))

_T_FINE_G1 = np.linspace(0, 20.0, 250)
_T_FINE_G2 = np.linspace(0, 9.0, 200)

W_SURV = np.array([1.0]*10 + [0.7]*3 + [0.3]*3)

NEUTRO_FRAC = {'recalc': 0.24, 'fib': 0.76, 'xiii': 0.82}

# ================================================================
#  DRIVING FUNCTIONS
# ================================================================

TV_FIX = 1.5; KCD_FIX = 0.2

def _gauss(t,mu,sig): return np.exp(-0.5*((t-mu)/sig)**2)

def _V_scalar(t):
    if t<=0: return 0.0
    r=t/TV_FIX; return r*np.exp(1-r)

def _V(t):
    t=np.asarray(t,dtype=float); r=t/TV_FIX
    return np.where(t>=0, r*np.exp(1-r), 0.0)

# ================================================================
#  ODE: 5 states [D, AP, Hc, Hn, X]
#  kr_eff and tp2_eff passed as extra args
# ================================================================

def _rhs(y, t, pv, Nf, kr_eff, tp2_eff):
    D=max(min(y[0],1),0); AP=max(y[1],0); Hc=max(y[2],0)
    Hn=np.clip(y[3],0,pv[7]*0.999); X=y[4]

    V=_V_scalar(t); Nr=Nf(t)/N1_BASE
    S = V + pv[10]*_gauss(t, tp2_eff, pv[9])*Nr*(1-D)

    dD = pv[0]*S*(1-D) - kr_eff*D          # kr_eff: group-specific
    dAP = pv[2]*D - pv[3]*AP
    dHc = pv[4]*V - KCD_FIX*Hc
    cap = max(1-Hn/pv[7], 0.005)
    dHn = pv[5]*min(AP*AP,10)*cap - pv[6]*Hn
    gHn = Hn/max(1-Hn/pv[7], 0.005)
    liver = max(1-Hn/pv[7], 0.0)
    dX = pv[20]*V + pv[21]*AP*Nr - pv[22]*gHn - pv[23]*liver*X  # dx removed

    return [dD, dAP, dHc, dHn, dX]

def _solve(pv, t_eval, Nf, t_fine, kr_eff, tp2_eff):
    y = odeint(_rhs, [0,0,0,0,0], t_fine,
               args=(pv, Nf, kr_eff, tp2_eff),
               rtol=1e-5, atol=1e-7, mxstep=5000)
    if np.any(np.isnan(y)): raise RuntimeError("NaN")

    interps = [interp1d(t_fine, y[:,i], kind='linear', fill_value='extrapolate') for i in range(5)]
    D=np.clip(interps[0](t_eval),0,1); AP=np.maximum(interps[1](t_eval),0)
    Hc=np.maximum(interps[2](t_eval),0); Hn=np.clip(interps[3](t_eval),0,pv[7]*0.999)
    X=interps[4](t_eval)
    V=_V(t_eval); gHn=Hn/np.maximum(1-Hn/pv[7],0.005); Nr=Nf(t_eval)/N1_BASE

    return dict(D=D*100, AP=AP, Hc=Hc, Hn=Hn, gHn=gHn, V=V, Nr=Nr, X=X,
        recalc   = -pv[11]*V - pv[12]*AP + pv[13]*gHn,
        thrombin = -pv[14]*V             + pv[15]*gHn,
        fib      = +pv[16]*V + pv[17]*AP - pv[18]*gHn - pv[19]*Hc,
        xiii     = X)

# ================================================================
#  PARAMETERS: 26 = 24 shared + km + tm
# ================================================================

NAMES = [
    'kd','kr','krl','kcl','kca',        # 0-4
    'kna','knd','Hm',                    # 5-7
    'tp2','s2','a2',                     # 8-10
    'ar','cr','br',                      # 11-13: recalc
    'at','bt',                           # 14-15: thrombin
    'af','cf','bf','df',                 # 16-19: fib
    'ax','cx','bx','kx',                # 20-23: XIII (dx removed)
    'km',                                # 24: myelosan kr modifier
    'tm',                                # 25: myelosan tp2 modifier
]

BOUNDS = [
    (0.1,  5.0),     # kd
    (0.1,  5.0),     # kr — base value (G1) [expanded from 3]
    (0.3, 20.0),     # krl
    (0.3, 20.0),     # kcl
    (0.1, 100),      # kca
    (1,  1500),      # kna [expanded from 800]
    (0.01, 10.0),    # knd
    (3,  1000),      # Hm
    (6.0, 12.0),     # tp2 — G1 inflammatory peak [narrowed: diagnostic showed 9-10]
    (0.8,  6.0),     # s2
    (0.1, 10.0),     # a2
    (1,   200),      # ar
    (5,   600),      # cr
    (0.005, 15.0),   # br
    (0.5,  25),      # at
    (0.001, 1.5),    # bt
    (1,   120),      # af
    (5,   350),      # cf
    (0.001, 8.0),    # bf [expanded from 5]
    (0.1,  30),      # df
    (1,   250),      # ax
    (10,  600),      # cx [limited — prevent large-number cancellation]
    (0.001, 50.0),   # bx
    (0.05, 15),      # kx
    (1.5, 15.0),     # km — myelosan kr multiplier
    (0.2,  0.8),     # tm — myelosan tp2 multiplier
]

assert len(NAMES) == len(BOUNDS) == 26

SC = dict(recalc=250, thrombin=22, fib=85, xiii=150, AP=0.85, D=62)
W_SPLIT = 2.0  # STRONG mechanism-split constraint (was 0.3)

def _pk(v): return {n:v[i] for i,n in enumerate(NAMES)}

# ================================================================
#  COST — JOINT FIT
# ================================================================

def _cost_core(pv):
    kr_g1 = pv[1]
    kr_g2 = pv[1] * pv[24]   # kr * km
    tp2_g1 = pv[8]
    tp2_g2 = pv[8] * pv[25]  # tp2 * tm

    try:
        o1 = _solve(pv, T1, _N1, _T_FINE_G1, kr_g1, tp2_g1)
        o2 = _solve(pv, T2, _N2, _T_FINE_G2, kr_g2, tp2_g2)
    except Exception:
        return 1e6

    for o in [o1, o2]:
        if any(np.any(np.isnan(o[k])) for k in ['D','AP','recalc','thrombin','fib','xiii']):
            return 1e6

    c = 0.0

    # G1: survivor-weighted
    for k,d,s in [('recalc',RECALC1,SC['recalc']),('thrombin',THROMB1,SC['thrombin']),
                   ('fib',FIB1,SC['fib']),('xiii',XIII1,SC['xiii']),
                   ('AP',AP1,SC['AP']),('D',DEG1,SC['D'])]:
        c += np.sqrt(np.average(((o1[k]-d)/s)**2, weights=W_SURV))

    # G2: clean
    for k,d in [('recalc',RECALC2),('thrombin',THROMB2),('fib',FIB2),
                 ('xiii',XIII2),('AP',AP2),('D',DEG2)]:
        c += np.sqrt(np.mean(((o2[k][:len(d)]-d)/SC[k])**2))

    # Hn saturation
    if np.any(o1['Hn'] > pv[7]*0.99): c += 2.0

    # STRONG mechanism-split at day 2 (G1)
    idx2 = 2
    V2 = o1['V'][idx2]; AP2v = o1['AP'][idx2]; Nr2 = o1['Nr'][idx2]

    if V2 > 1e-6 and AP2v > 1e-6:
        # Recalc: neutro = cr·AP / (ar·V + cr·AP), target 24%
        vr = pv[11]*V2; nr = pv[12]*AP2v
        tot = vr + nr
        if tot > 1: c += W_SPLIT * ((nr/tot) - NEUTRO_FRAC['recalc'])**2

        # Fib: neutro = cf·AP / (af·V + cf·AP), target 76%
        vf = pv[16]*V2; nf = pv[17]*AP2v
        tot = vf + nf
        if tot > 1: c += W_SPLIT * ((nf/tot) - NEUTRO_FRAC['fib'])**2

        # XIII: neutro = cx·AP·Nr / (ax·V + cx·AP·Nr), target 82%
        vx = pv[20]*V2; nx = pv[21]*AP2v*Nr2
        tot = vx + nx
        if tot > 1: c += W_SPLIT * ((nx/tot) - NEUTRO_FRAC['xiii'])**2

    return c

def _cost_bounded(pv):
    for i,(lo,hi) in enumerate(BOUNDS):
        if pv[i]<lo or pv[i]>hi: return 1e6*(1+max(lo-pv[i],pv[i]-hi,0)/(hi-lo))
    return _cost_core(pv)

def _r2(m,d):
    ss=np.sum((d-np.mean(d))**2); return 1-np.sum((m-d)**2)/ss if ss>1e-12 else 0

# ================================================================
#  MAIN
# ================================================================

def main():
    quick = '--quick' in sys.argv
    outdir = os.path.dirname(os.path.abspath(__file__))

    print("="*65)
    print("v12: JOINT FIT — Diagnostic-Informed Architecture")
    print(f"  {len(NAMES)} params = 24 shared + km + tm (myelosan modifiers)")
    print(f"  G1: {len(T1)*6}pts (surv-weighted) + G2: {len(T2)*6}pts = {len(T1)*6+len(T2)*6}")
    print(f"  Data/param: {(len(T1)*6+len(T2)*6)/len(NAMES):.1f}")
    print(f"  Mechanism-split: W={W_SPLIT} (STRONG)")
    print(f"  Mode: {'QUICK' if quick else 'FULL'}")
    print("="*65)

    mid = np.array([(lo+hi)/2 for lo,hi in BOUNDS])
    t0=time.time()
    for _ in range(10): _cost_core(mid)
    ms=(time.time()-t0)/10*1000
    print(f"\nSpeed: {ms:.1f} ms/eval")

    if quick:
        seeds=[42,7]; de_pop,de_iter=8,120; nm_iter,pw_iter=3000,2000
    else:
        seeds=[42,7,123,2024,999]; de_pop,de_iter=12,300; nm_iter,pw_iter=10000,8000

    best_cost=1e6; best_x=None; t_start=time.time()
    for seed in seeds:
        print(f"\n--- DE seed={seed} ---")
        ts=time.time()
        r = differential_evolution(_cost_core, BOUNDS, maxiter=de_iter, popsize=de_pop,
            seed=seed, tol=1e-7, workers=-1, mutation=(0.5,1.5), recombination=0.85,
            disp=False, polish=False)
        print(f"  cost={r.fun:.6f} ({time.time()-ts:.0f}s, {r.nfev} evals)")
        if r.fun<best_cost: best_cost=r.fun; best_x=r.x.copy(); print("  → best!")

    print(f"\nBest DE: {best_cost:.6f}")
    for method,opts in [('Nelder-Mead',{'maxiter':nm_iter,'xatol':1e-9,'fatol':1e-10}),
                         ('Powell',{'maxiter':pw_iter,'ftol':1e-10})]:
        try:
            r=minimize(_cost_bounded,best_x,method=method,options=opts)
            if np.isfinite(r.fun) and r.fun<best_cost:
                best_x=r.x.copy(); best_cost=r.fun
                print(f"  {method}: {r.fun:.6f} → improved!")
            else: print(f"  {method}: {r.fun:.6f}")
        except Exception as e: print(f"  {method}: failed {e}")

    print("--- NM round 2 ---")
    try:
        r=minimize(_cost_bounded,best_x,method='Nelder-Mead',
                   options={'maxiter':nm_iter,'xatol':1e-10,'fatol':1e-11})
        if np.isfinite(r.fun) and r.fun<best_cost:
            best_x=r.x.copy(); best_cost=r.fun; print(f"  {r.fun:.6f} → improved!")
    except: pass

    total_time=time.time()-t_start
    p=_pk(best_x); p['tv']=TV_FIX; p['kcd']=KCD_FIX
    p['kr_g2'] = p['kr']*p['km']
    p['tp2_g2'] = p['tp2']*p['tm']

    # Solve both groups
    o1 = _solve(best_x, T1, _N1, _T_FINE_G1, p['kr'], p['tp2'])
    o2 = _solve(best_x, T2, _N2, _T_FINE_G2, p['kr_g2'], p['tp2_g2'])

    # ---- G1 RESULTS ----
    print(f"\n{'='*65}")
    print(f"GROUP I (cost={best_cost:.6f})")
    print("-"*40)
    m1={}
    for k,d in [('recalc',RECALC1),('thrombin',THROMB1),('fib',FIB1),
                 ('xiii',XIII1),('AP',AP1),('D',DEG1)]:
        r2v=_r2(o1[k],d); rmse=np.sqrt(np.mean((o1[k]-d)**2))
        m1[k]=dict(R2=r2v,RMSE=rmse)
        print(f"  {k:10s}: R²={r2v:+.4f}  RMSE={rmse:.3f}")
    print(f"  {'AVERAGE':10s}: R²={np.mean([v['R2'] for v in m1.values()]):+.4f}")

    # ---- G2 RESULTS ----
    print(f"\n{'='*65}")
    print(f"GROUP II (jointly fit)")
    print("-"*40)
    m2={}
    for k,d in [('recalc',RECALC2),('thrombin',THROMB2),('fib',FIB2),
                 ('xiii',XIII2),('AP',AP2),('D',DEG2)]:
        mv=o2[k][:len(d)]; r2v=_r2(mv,d); rmse=np.sqrt(np.mean((mv-d)**2))
        m2[k]=dict(R2=r2v,RMSE=rmse)
        print(f"  {k:10s}: R²={r2v:+.4f}  RMSE={rmse:.3f}")
    print(f"  {'AVERAGE':10s}: R²={np.mean([v['R2'] for v in m2.values()]):+.4f}")

    # ---- MYELOSAN EFFECT ----
    print(f"\n{'='*65}")
    print("MYELOSAN MODIFIERS")
    print("-"*40)
    print(f"  kr:  G1={p['kr']:.3f}, G2={p['kr_g2']:.3f} (×{p['km']:.1f})")
    print(f"  tp2: G1={p['tp2']:.1f}d, G2={p['tp2_g2']:.1f}d (×{p['tm']:.2f})")

    # ---- MECHANISM SPLIT ----
    print(f"\n{'='*65}")
    print("MECHANISM SPLIT")
    print("-"*40)
    for ti,label in [(2,"Day 2"),(4,"Day 4"),(11,"Day 11")]:
        idx=np.where(T1==ti)[0][0]
        V=o1['V'][idx];AP=o1['AP'][idx];gHn=o1['gHn'][idx];Hc=o1['Hc'][idx];Nr=o1['Nr'][idx]
        print(f"\n  {label}: V={V:.3f}, AP={AP:.3f}, gHn={gHn:.1f}, Hc={Hc:.2f}")
        for name in ['recalc','fib','xiii']:
            if name=='recalc':
                v_p=-p['ar']*V; n_p=-p['cr']*AP; ghn_p=p['br']*gHn; hc_p=0
            elif name=='fib':
                v_p=p['af']*V; n_p=p['cf']*AP; ghn_p=-p['bf']*gHn; hc_p=-p['df']*Hc
            elif name=='xiii':
                v_p=p['ax']*V; n_p=p['cx']*AP*Nr; ghn_p=-p['bx']*gHn; hc_p=0
            total=v_p+n_p+ghn_p+hc_p
            procoag_tot=abs(v_p)+abs(n_p)
            frac_n=abs(n_p)/procoag_tot*100 if procoag_tot>0.1 else 0
            print(f"    {name:8s}: V={v_p:+.1f} AP={n_p:+.1f} gHn={ghn_p:+.1f} Hc={hc_p:+.1f}"
                  f" → {total:+.1f} (neutro={frac_n:.0f}%)")

    # ---- PARAMETERS ----
    print(f"\n{'='*65}")
    print("PARAMETERS")
    print("-"*40)
    at_bound=0
    for i,n in enumerate(NAMES):
        lo,hi=BOUNDS[i]; flag=""
        if best_x[i]-lo<0.01*(hi-lo): flag=" ← LOW"; at_bound+=1
        elif hi-best_x[i]<0.01*(hi-lo): flag=" ← HIGH"; at_bound+=1
        print(f"  {n:6s} = {best_x[i]:12.6f}  [{lo},{hi}]{flag}")
    if at_bound: print(f"\n  WARNING: {at_bound}/{len(NAMES)} at bounds!")
    print(f"\nTime: {total_time:.0f}s ({total_time/60:.1f}min)")

    # ---- SAVE ----
    out=dict(model='v12_diagnostic_informed', params=p, cost=float(best_cost),
             metrics_g1=m1, metrics_g2=m2, elapsed=total_time,
             o1={k:(v.tolist() if hasattr(v,'tolist') else v) for k,v in o1.items()},
             o2={k:(v.tolist() if hasattr(v,'tolist') else v) for k,v in o2.items()},
             T1=T1.tolist(), T2=T2.tolist(), best_x=best_x.tolist())
    pkl_path=os.path.join(outdir,'results_v12.pkl')
    with open(pkl_path,'wb') as f: pickle.dump(out,f)
    print(f"Saved → {pkl_path}")

if __name__=='__main__': main()
