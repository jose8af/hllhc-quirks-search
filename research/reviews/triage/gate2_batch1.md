# Gate-2 triage batch 1 (C001-C013)

## C001 - PASS (proposed-not-searched, conf medium)
- Observable: Quirk pairs: non-helical/anomalously ionising tracks, out-of-time or stopped deposits, and (microscopic-string regime) resonance + soft unclustered low-pT track/energy pattern; TeV dijet resonance with anomalous soft tracks.
- Gap: INSPIRE (collaboration:CMS/ATLAS + 'quirk' in abstract) returns no CMS or ATLAS quirk search; only FASER (forward, QCD-colourless, charge +-1) and phenomenology (2504.02940, 2506.11192, 1708.02243) exist. Open: central-detector search for EW-charged quirks (non-helical tracks / soft-track anomalies + resonance) and its HL-LHC reach.
- Closest: arXiv:2607.26195 (FASER); arXiv:2403.05311 (CMS); arXiv:2605.20015 (ATLAS); arXiv:2601.09023 (LHCb (phenomenology))
- HL-LHC: Higher statistics for low-rate EW-charged quirks (few hundred GeV); Phase-2 track trigger/L1 tracking and MTD timing for slow/non-helical tracks; weakly-supervised resonance+soft-track search benefits from larger samples.
- Reason: Identifiable observable; no CMS/ATLAS quirk search found with several synonym queries; closest (SUEP) is prompt/isotropic and not designed for quirk string dynamics. Exhaustiveness limited by INSPIRE abstract indexing.

## C002 - HOLD (searched-limited-regime, conf low)
- Observable: Displaced vertices (muon system/calorimeter/tracker) from Higgs -> glueball pairs; multiple DVs in top-partner-pair events (glueball cτ down to sub-cm).
- Gap: Higgs->glueball DV is covered by many Run-2/3 Higgs->LLP searches; a residual gap (top-partner pair -> glueballs, sub-cm decay lengths, theory refs 1512.05782, 2310.13731) is plausible but no search/reinterpretation evidence checked in detail.
- Closest: arXiv:2503.20445 (ATLAS); arXiv:2409.10806 (CMS); arXiv:2402.01898 (CMS); arXiv:2603.01991 (ATLAS)
- HL-LHC: Phase-2 L1 displaced-vertex track trigger; larger Higgs sample for rare h->LLP; muon-system reach.
- Reason: Dominant signature (h->LLP) is well covered by ATLAS/CMS; the genuinely open sub-case is narrow and overlaps C001/C005. Hold pending a concrete top-partner+DV efficiency study.

## C003 - PASS (searched-limited-regime, conf medium)
- Observable: High-multiplicity isotropic soft tracks with displaced decays of dark photons/dark mesons (displaced SUEP), and non-ggF/non-prompt production modes.
- Gap: All CMS/ATLAS SUEP searches (2403.05311, 2607.09621, 2604.05996, 2605.20015) assume prompt dark-photon decay; no search with displaced dark-meson decays (cτ >~ mm) or VBF/non-ggF production found (abstracts.value:SUEP and displaced returned nothing).
- Closest: arXiv:2403.05311 (CMS); arXiv:2607.09621 (CMS); arXiv:2604.05996 (CMS); arXiv:2605.20015 (ATLAS)
- HL-LHC: Phase-2 L1 track trigger / displaced-vertex track trigger (recid2908980), MTD timing, L1 scouting lower HT thresholds.
- Reason: Prompt SUEP now well covered, but the displaced-SUEP regime is explicit in the soft-bomb paper's deferrals and untouched by the four experimental papers read; HL-LHC tracking/trigger upgrades are directly relevant.

## C004 - HOLD (indirectly-covered, conf medium)
- Observable: Anomaly score (autoencoder/flow) on jets/events as trigger or offline tag for dark showers/SUEP/SVJ; not a fixed signature.
- Gap: Not a signature gap: a method. Open item is only robustness of AE tagging to dark-hadronisation parameters; no measurable distinct observable.
- Closest: recid3188808 (CMS); arXiv:2505.01634 (ATLAS); recid2751629 (CMS); arXiv:2502.09770 (ATLAS)
- HL-LHC: L1/HLT anomaly triggers are in use at CMS; Phase-2 hardware extends them.
- Reason: Technique rather than collider signature (Q1 weak); CMS/ATLAS already deploy AD triggers and AD searches in SVJ/dijet. Not rejected only because no search quantifies hadronisation robustness for dark showers; merge into C003/C005/C008 as an analysis option.

## C005 - PASS (searched-limited-regime, conf low)
- Observable: Displaced multi-vertex/trackless dark-shower jets from (i) EW pair-produced dark-quark mediators with leptons/MET, (ii) Higgs-portal (VBF/VH) production with hadronic dark-pion decays, dark-pion masses above ~20 GeV.
- Gap: Run-2/3 EJ searches target QCD-produced t/s-channel mediators with m_pi 10-20 GeV; the muon-rich Higgs-decay search covers m_pi 1-12 GeV. Hadronic displaced dark showers from Higgs-portal (VBF/VH-tagged) and from EW pair production are not covered by a published full search found.
- Closest: arXiv:2403.01556 (CMS); arXiv:2511.11888 (CMS); arXiv:2505.02429 / arXiv:2510.12347 (ATLAS); recid3201494 (ATLAS); arXiv:2503.20445 (ATLAS)
- HL-LHC: Phase-2 L1 displaced-track trigger and scouting for Higgs-portal showers (ggF cleaner via VBF/VH tag); MTD timing.
- Reason: Large crowded field, several sub-gaps remain; recommend splitting into (a) Higgs-portal hadronic displaced dark showers and (b) EW-production dark showers. Seeds partly stale (Snowmass 2022 quote predates 2511.11888).

## C006 - HOLD (proposed-not-searched, conf low)
- Observable: Z -> dark quarks -> dark pions -> bb mumu / displaced multi-track vertices; Z -> chi chi + dark photon with displaced dimuon + MET.
- Gap: No ATLAS/CMS/LHCb search found for Z -> dark-shower bbmumu (only Higgs-sourced analogues). Viability depends on soft-muon/b trigger acceptance, not verified.
- Closest: recid2181655 (CMS); arXiv:2306.07413 (ATLAS); arXiv:2511.11888 (CMS); recid3132638 (CMS)
- HL-LHC: Huge Z sample with Phase-2 L1 scouting/track trigger could open soft muon+b final states; trigger thresholds are the question.
- Reason: Signature identifiable and apparently unsearched, but rate x trigger acceptance and competition from LHCb/Tera-Z not assessed; second seed is mainly a forward-detector story (2605.03427).

## C007 - HOLD (one-observable-not-another, conf medium)
- Observable: Lund-jet-plane density / graph-network tagging and energy correlators of dark-shower jets.
- Gap: No CMS/ATLAS dark-shower analysis using LJP/EEC found (INSPIRE queries empty); only theory 2301.07732 and 2609.11692 (ML tagging).
- Closest: arXiv:2505.01634 (ATLAS); arXiv:2507.07775 (CMS); arXiv:2608.05323 (CMS)
- HL-LHC: Statistics-limited substructure; no specific HL-LHC hardware link.
- Reason: Observable is a tagger technique for prompt dark jets; value depends on a model that already has a search; HL-LHC specificity weak.

## C008 - PASS (theory-explored-untested, conf medium)
- Observable: Semi-visible jets recoiling against ISR photon/jet; MET aligned with jet; rinv reconstruction; low-mass (0.5-1 TeV) Z' where dijet resonance searches lose sensitivity.
- Gap: Lepton/tau-enriched s-channel SVJ now searched by CMS; ISR-recoil SVJ (photon or jet, 2409.04741: 'ISR channel not yet explored') and low-mass Z' (0.5-1 TeV) have no CMS/ATLAS search found.
- Closest: arXiv:2608.05323 (CMS); recid2963506 (CMS); arXiv:2305.18037 (ATLAS); arXiv:2505.01634 (ATLAS); recid3185627 (CMS)
- HL-LHC: ISR+SVJ is statistics-driven (HL-LHC 3 ab-1); lower-threshold photon/jet triggers and scouting.
- Reason: Seed gap partly closed (lepton/tau) but the ISR-recoil channel remains a specific, measurable, unsearched signature; added value at HL-LHC statistics.

## C009 - PASS (theory-explored-untested, conf medium)
- Observable: gg/VBF/ZH -> h -> Z(ll) + invisible X (m_X 1-32 GeV) and ZH with H -> ll/jj + MET: recoil mass and Z-MET alignment.
- Gap: No ATLAS/CMS search for h -> Z + invisible X found (INSPIRE: only photon+MET and bb+MET exotic Higgs decays); theory-only HL-LHC projections exist.
- Closest: arXiv:2212.09649 (ATLAS); arXiv:2606.14362 (ATLAS); arXiv:2301.10731 (ATLAS); arXiv:2206.01214 (phenomenology)
- HL-LHC: Limited by statistics near the SM h->Zνν 'neutrino floor'; 3 ab-1 needed.
- Reason: Clear observable, no experimental search found, projections exist from theory only; irreducible SM h->Zνν makes reach limited, hence moderate confidence.

## C010 - REJECT (well-covered, conf medium)
- Observable: MET + soft displaced lepton/track pairs from compressed iDM, higgsino or LLP spectra.
- Gap: Residual only: ATLAS iDM analogue and iDM with Delta/m1 < 10%; not a distinct signature.
- Closest: arXiv:2305.11649 (CMS); recid3186741 (CMS); arXiv:2511.20042 (ATLAS); arXiv:2401.14046 (ATLAS); arXiv:2511.16394 (CMS); arXiv:2511.08212 (CMS); arXiv:1905.13059 / arXiv:2409.18762 (CMS/ATLAS)
- HL-LHC: Covered by existing HL-LHC compressed-EWkino projections; ATLAS iDM analogue would be incremental.
- Reason: Positive evidence of broad coverage by 8+ CMS/ATLAS results over iDM, higgsino, VBF-compressed variants, plus HL-LHC projections. If re-raised, narrow to small-splitting (1-5%) iDM.

## C011 - HOLD (searched-limited-regime, conf medium)
- Observable: MET recoiling against a displaced dark-Higgs decay (bb/WW) ; Z -> A' h_D with displaced A'/h_D; lepton-jets from dark Higgs-strahlung.
- Gap: Displaced mono-dark-Higgs (MET + displaced bb/WW decay) has no dedicated interpretation; generic DV+MET (2603.12051) could be recast. Prompt Z->A'h_D already searched (2306.07413).
- Closest: arXiv:2306.07413 (ATLAS); arXiv:2604.20999 (CMS); arXiv:2407.10549 (ATLAS); arXiv:2603.12051 (ATLAS)
- HL-LHC: Displaced DV trigger and larger data; moderate.
- Reason: Seed-2 premise outdated; seed-1 is mostly a reinterpretation of an existing DV+MET search. HOLD pending recast check.

## C012 - HOLD (indirectly-covered, conf low)
- Observable: DV+MET, disappearing tracks, HSCP, non-pointing/delayed photon (+MET) with lifetimes set by freeze-in/low reheating.
- Gap: Mostly a cosmological framing of existing LLP signatures; only potential gap is HL-LHC timing-based delayed-photon reach; not established.
- Closest: arXiv:2209.01029 (ATLAS); arXiv:1909.06166 (CMS); arXiv:2603.12051 (ATLAS); arXiv:2402.01898 (CMS)
- HL-LHC: MTD/HGCAL timing for delayed photons is a genuine HL-LHC feature but no projection found.
- Reason: No new signature; benchmark choice only. Hold as input for LLP benchmark selection.

## C013 - PASS (searched-limited-regime, conf medium)
- Observable: Heavily ionising tracks with charge 8<=|z|<=19 (between ATLAS multi-charged and HECO searches) and sub-e/3 fractional charges in main detectors via dE/dx and timing.
- Gap: No ATLAS/CMS result found for 8<=|z|<=19 (ATLAS stops at 7 and restarts at 20; CMS 13 TeV multi-charged coverage UNVERIFIED) and for FCP charges below e/3 in main detectors (CMS stops at e/3; ATLAS has no result).
- Closest: arXiv:2303.13613 (ATLAS); arXiv:2308.04835 (ATLAS); arXiv:2402.09932 (CMS); arXiv:2311.06509 (MoEDAL); recid2961271 (ATLAS)
- HL-LHC: Luminosity x20-ish for Drell-Yan (z^4-enhanced rates at high z); Phase-2 trigger/timing and dE/dx.
- Reason: Precisely locatable charge gaps between published results from verified text; HL-LHC added value moderate; theory motivation of z 8-19 unclear.
