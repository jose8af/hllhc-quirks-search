# Stage 6: feasibility note on using CMS Open Data to validate Stage-4 inputs (C001 quirks, theory track)

2026-10-13 (revised 2026-10-16, fix R1) · Executor · public information only · no data downloaded, nothing analysed.

**Schedule (B-6).** The project deadline is Sun 2026-10-18 afternoon. **None of the checks below fits it.** The efforts quoted
(1–5 weeks, ESTIMATE) make them follow-up work after this project; no Open Data result should be expected in it.

**What Open Data cannot do.** Nothing in Open Data can test the headline quirk-specific inputs (string dynamics, the
P_fake ~1e-9 PU-combinatorics fake rate, signal efficiency). No released sample contains quirk-like anomalous tracks, so
there is no validation signal.

> **POLICY REMINDER: read before any use.** The user is a CMS member. **Before any CMS Open Data is used for this
> study, the user must confirm the CMS internal policy for members who publish with Open Data**, as well as the Open
> Data terms of use and citation requirements. The portal's research guide tells CMS members to check an internal
> document, *"Rules for use of open access CMS data by individual members of CMS"* (VERIFIED: the guide links to it,
> [cms-guide-for-research](https://opendata.cern.ch/docs/cms-guide-for-research)). The public policy is
> [record 414, "2018 CMS data preservation, re-use and open access policy"](https://opendata.cern.ch/record/414)
> (VERIFIED: title only, contents not read). **This note makes no claim about what either policy allows.** The CC0 terms of the portal datasets do not remove the CMS-member rules.
If any Open Data comparison is ever shown, the Stage-5 labelling rules (no CMS name or logo) must stay.

Tags: **VERIFIED** means checked on 2026-10-13, and re-checked 2026-10-16 for the §4 records, at the cited URL, the portal API (`opendata.cern.ch/api/records/<recid>`,
metadata only) or the CMSSW event-content files on GitHub. **UNVERIFIED** means the claim comes from memory or inference.

## 1. What is available, and what each item could check

**Released years and tiers (B-4).** Hit-level information is in RAW only (2010–2012 and the 2017E record found); AOD, MiniAOD
and NanoAOD have no cluster positions. RAW re-reco in an SLC container is the only route to hits.

| Year | Tiers found | Tag |
|---|---|---|
| 2010–2012 (Run 1) | AOD and RAW (partial; examples in §1 table) | VERIFIED (API, records listed below). Completeness of the release UNVERIFIED |
| 2015D | AOD (e.g. 24116, 2021) | VERIFIED (API) |
| 2016 | UL MiniAODv2 (e.g. ZeroBias 2016G, 30516, published 2024) and UL NanoAODv9 (release string UNVERIFIED), plus PF-NanoAOD subset (31308, 31309) | VERIFIED (API for 30516; portal and CERN announcement for the release; [CMS news](https://openscience.web.cern.ch/node/441)) |
| 2017 | RAW ZeroBias 2017E (93950) and PU MC GEN-SIM-DIGI-RAW (93952) | VERIFIED (API) |


**Data tiers (VERIFIED from CMSSW config only; no Open Data file content inspected).** Source: `RecoLocalTracker_EventContent_cff.py` in
[5_3_X](https://github.com/cms-sw/cmssw/blob/CMSSW_5_3_X/RecoLocalTracker/Configuration/python/RecoLocalTracker_EventContent_cff.py)
and [10_6_X](https://github.com/cms-sw/cmssw/blob/CMSSW_10_6_X/RecoLocalTracker/Configuration/python/RecoLocalTracker_EventContent_cff.py).
- **RECO** keeps `siPixelClusters` and `siStripClusters`.
- **AOD** keeps only `ClusterSummary`. This is a per-subdetector cluster count (BPIX/FPIX/TIB/TOB/TID/TEC, UNVERIFIED at
  that granularity), not cluster positions.
- **MiniAOD** keeps strip and pixel clusters only on muon track extras (UNVERIFIED, from memory).
- **NanoAOD** keeps no clusters.

So per-layer or per-cm² cluster densities need RECO, or RAW re-reconstructed in a container. RAW records state that
"the reconstruction step can be repeated" with a supplied configuration (VERIFIED,
[record 62](https://opendata.cern.ch/record/62)).

**Config-vs-file caveat (B-3).** Event-content configs are not the content of the released files, which were produced with
specific releases and may differ. The first step of any check must be `edmDumpEventContent` on one file. The 10_6
`inclusiveSecondaryVertices` claim is from config only; its presence in released 2016 files is UNVERIFIED.

**Secondary-vertex collections in AOD (VERIFIED from config only,
[`RecoVertex_EventContent_cff.py`](https://github.com/cms-sw/cmssw/blob/CMSSW_10_6_X/RecoVertex/Configuration/python/RecoVertex_EventContent_cff.py)
and `RecoEgamma_EventContent_cff.py`, 5_3_X and 10_6_X):**
- AOD keeps `nuclearInteractionMaker`, `generalV0Candidates`, `allConversions`/`conversions` and
  `offlinePrimaryVerticesFromCosmicTracks`.
- 10_6 AOD also keeps `inclusiveSecondaryVertices`.
- MiniAOD keeps `slimmedKshortVertices`, `slimmedLambdaVertices` and `reducedEgamma` conversions, but no
  nuclear-interaction collection (VERIFIED, `MicroEventContent_cff.py` 10_6_X).

| Stage-4 input (plan §) | Candidate public sample (recid) | Tier / content | Status |
|---|---|---|---|
| Cluster density vs PU (§1.4 top-up ratios ×1.5–7, V4-2) | `/MinimumBias/Run2012B-v1/RAW` (62; 2.7 M ev, 307 GB), `/MinimumBias/Run2011A-v1/RAW` (35), `/MinimumBias/Run2010B-v1/RAW` (42) | RAW: re-reco gives clusters | VERIFIED (API) |
| same, Run 2 | `/ZeroBias/Run2017E-v1/RAW` (93950; 198 files, ≈1.0 TB; runs 304125–304144; published 2025) | RAW; record metadata sparse (no container, no event count) | VERIFIED (API). PU of these runs UNVERIFIED |
| same, matched simulation | `/SingleNeutrino/RunIISummer20UL17HLT-PUForTRKv2…/GEN-SIM-DIGI-RAW` (93952; 35 files, 120 GB) and a QCD μ-enriched partner (93951) | pure-PU full Geant4 MC, 2017 conditions | VERIFIED (API, title and size). PU profile, SimHit content and intended use UNVERIFIED |
| same, coarse | `/ZeroBias/Run2015D-16Dec2015-v1/AOD` (24116; 198 M ev, 13 TB; container `cmssw_7_6_7`), 2012 MinimumBias AOD (6013, 6039, 24408, 24452) | AOD `ClusterSummary` vs nPV | VERIFIED (API and CMSSW config) |
| NI vertex rate vs r (beam pipe, pixel layers) (§4.2 NI toy, r_NI) | the AODs above | `nuclearInteractionMaker` (AOD only) | VERIFIED from config; file content not inspected. A public CMS tracker-material NI study exists in the literature, UNVERIFIED here |
| γ conversion rate (§4.2 photon gun × Pythia spectrum) | the AODs above; 2016 ZeroBias MiniAOD (30516, 30549; container `cmssw_10_6_30`) | `allConversions` (AOD), `reducedEgamma` (MiniAOD) | VERIFIED |
| K⁰_S / Λ rate (§4.2 V0) | same | `generalV0Candidates` / `slimmed*Vertices` | VERIFIED |
| Loopers (§4.2; looper-pair top-up variant) | RAW re-reco only (clusters plus low-pT tracking); AOD `generalTracks` has no dedicated looper product | RECO | UNVERIFIED that low-pT loopers are reconstructible enough to be useful |
| Possible rough cosmic/halo rate (§4.2 "argument") | No Cosmics primary dataset found in a portal search (only HLT cosmic configs). `/NoBPTX/Run2012{B,C,D}-22Jan2013-v1/AOD` (6018, 6044, 24457; ≈0.33 TB each) are triggered in empty bunches, so an in-time rate needs trigger-efficiency and live-time bookkeeping | AOD | VERIFIED (search result and records). Cosmic content of NoBPTX UNVERIFIED. Fallback: cite the published CMS cosmic-muon rate |
| Direct anomalous-track look | `/MET/Run2015D-16Dec2015-v1/AOD` (24106; 2.4 TB), HTMHT 2015/2016 (24108, 30507). No MET RAW found | AOD drops unassociated clusters, so quirk hits are invisible unless re-reco from RAW | VERIFIED (records). 2012/2016 MET availability UNVERIFIED |

Citation: each record carries a DOI, for example 10.7483/OPENDATA.CMS.ZEN1.FJX6 for record 93950 (VERIFIED). The portal
datasets are CC0 ([terms of use](https://opendata.cern.ch/docs/terms-of-use), VERIFIED). The research guide gives no
citation format beyond the DOIs (VERIFIED). CMS-specific citation and acknowledgement rules: see the policy box.

## 2. Caveats

- **Detector.** Every check here is made with the Run-1 or Run-2 CMS tracker, not the Phase-2 tracker:
  - different radii, material and pitch;
  - Run 1 and 2015–16 used the Phase-0 pixel detector; 2017 used the Phase-1 pixel detector;
  - the beam-pipe radius also changed at LS1 (known from memory; values UNVERIFIED here).

  The data can validate **mechanisms and per-interaction rates** (NI/V0/conversion vertices per pp interaction versus
  radius and material; the in-time versus total cluster ratio). They cannot validate Phase-2 numbers directly. Every
  transfer needs a model: Fatras on a Run-2-like geometry, or a CMSSW-MC/data ratio applied to our Phase-2 Fatras numbers.
- **Pile-up.** Run 1 and 2 have ⟨PU⟩ of about 10–60 (UNVERIFIED for the specific runs; ESTIMATE from memory: mean about 21 in 2012, about 27 in 2016), against 200 in Stage 4. A PU
  slope measured at about 30 is extrapolated by about ×4–7. Out-of-time effects depend on the bunch spacing (50 ns in
  2012, 25 ns from 2015).
- **Tiers.** Cluster-level checks need RAW, a re-reco and the conditions. AOD gives counts and secondary vertices only.
- **Software.** Containers are x86_64 SLC6/SLC7, for example `cmssw_5_3_32`, `cmssw_7_6_7` and `cmssw_10_6_30`
  (VERIFIED from record metadata).
  - On Apple-silicon Macs they would run under emulation (slow; UNVERIFIED by how much). The Windows PC under WSL2/Docker is
    the natural host.
  - The 2017 RAW and MC records list no container (VERIFIED: the metadata field is empty).
- **Cost (rough ESTIMATE).**
  - An AOD skim: about 10–50 ms/event. 10⁶ events take about 10 CPU-h, and streaming over XRootD (UNVERIFIED for these
    records) or 20–50 GB of files is enough.
  - A RAW → RECO re-reco: several s/event. 10⁴ events take about 10–30 CPU-h. RAW input is about 1–10 GB (record 62 is about 0.11 MB/event; high-PU 2017 about 1 MB/event, UNVERIFIED).
  - Fatras on a Run-2-like geometry: a new ACTS geometry, about 1–2 weeks of work.

## 3. Ranked checks (if the policy allows)

1. **NI, V0 and conversion vertex rates per pp interaction versus radius (AOD).**
   - Constrains: the NI toy's r_NI weights and the conversion and V0 rates folded into B_NI, B_γ and B_V0 (§4.2), probably to
     tens of % (ESTIMATE). The Stage-4 NI background is a pattern-mimicry probability after PU overlay (f_pre, 8–9 decades of
     extrapolation); Open Data constrains the input rates only and cannot test the extrapolation or the final mimic rate.
   - Also gives a data-driven material map near the beam pipe (the ×0.5/×2 material systematic, §7).
   - Samples: 2012 MinimumBias AOD plus 2015D ZeroBias AOD (two beam-pipe and pixel configurations), versus nPV.
   - Effort: about 1–2 weeks, about 10–30 CPU-h, under 100 GB streamed. **Highest value per effort.**
2. **Cluster density: total versus in-time-only, and its PU slope.**
   - Validates: the §1.4 top-up ratios, which are the weakest Stage-4 input (IT ratio ×1.5–5), and the looper-pair
     variant.
   - Method: 2017 ZeroBias RAW re-reco (layer-resolved clusters) against the 2017 SingleNeutrino PU MC (93952) and
     against Fatras in-time PU on a Run-2-like geometry. AOD `ClusterSummary` versus nPV gives a quick coarse version.
   - Effort: about 3–5 weeks, about 50–100 CPU-h, a few tens of GB of RAW (ESTIMATE). The geometry port dominates the effort.
3. **Rough cosmic/halo rate from NoBPTX 2012 AOD (may fail).**
   - Might give a rough in-time cosmic/halo rate if NoBPTX contains them (needs trigger-efficiency and live-time bookkeeping,
     then × 25 ns × d0<1 mm acceptance); otherwise cite the published CMS cosmic-muon rate for §4.2.
   - Effort: about 1 week, under 10 CPU-h.
   - A direct anomalous-track search (MET AOD) is **not recommended**: AOD lacks unassociated clusters, and it would be a
     physics result, which is the most policy-sensitive use.

## 4. Kinematic checks Open Data can do (B-1)

Cheap and bearing on the signal side rather than the tracker. NanoAOD needs no CMSSW: the records list `root-vnc` and
`python-vnc` container images, so uproot/ROOT suffice (VERIFIED, API, record 30530).
- **Datasets (VERIFIED, API, 2026-10-16):** data: SingleMuon 2016G/H NanoAODv9 (30530, 30563), MET 2016G/H (30526, 30559),
  JetHT 2016G/H (30525, 30558). MC: UL2016 NanoAODv9 NANOAODSIM exists, for example ZJetsToNuNu Zpt-100to200 and
  Zpt-200toInf (74908, 74910). Which DY/W+jets/QCD NANOAODSIM samples exist is UNVERIFIED, so data-vs-MC may need the
  user's own Pythia/MG.
- **Z(μμ) / V+jets pT and the leading-jet tail** (SingleMuon) against Pythia/MG: tests the ISR hard-jet tail behind the
  Stage-2 signal normalisation and its LO-MLM +12..+15 / −11..−13 % uncertainty.
- **MET scale, resolution and tails, and MET recoil against the leading jet** (MET, JetHT). For Z(νν), the proxy is Z(μμ)
  with the muons removed from the MET (recoil proxy), cross-checked against the ZJetsToNuNu MC above.
- Effort: about 1 week (ESTIMATE), also follow-up work.

Limits: detector-level MET is not truth-level quirk recoil. The quirk MET is the pair's recoil with no jet-like deposit, so
only the ISR and SM-MET side is checkable. Run-2 PU is about 25–35, not 200. This is data against Pythia/MG, not a validation
of the quirk model.

> **POLICY REMINDER (repeated).** None of the checks above should start until the user has confirmed the CMS internal
> rules for members publishing with CMS Open Data, and the Open Data terms of use and citation requirements. This note
> makes no claim about that policy.
