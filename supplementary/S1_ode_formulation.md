# S1. Full ODE formulation and observable equations

*Part of the Supplementary Information for the manuscript “A mechanistic model of neutrophil-driven disseminated intravascular coagulation…” Main-text cross-reference: see Methods §2 and Results §3.*

Auto-generated from `src/model.py`. Includes the five state equations (D, AP, Hc, Hn, X), the definition gHn = Hn/(1 − Hn/Hm), and the six observable maps. *Etymological note:* in the source dissertation the inducer-derived and neutrophil-derived pools (Hc, Hn) were associated with hyaline microthrombi — fibrin clots in the microvasculature, a hallmark of DIC; in the ODE these are abstract coagulation pools rather than literal microthrombi, and the present text uses "inducer-derived" and "neutrophil-derived coagulation pool" accordingly.
