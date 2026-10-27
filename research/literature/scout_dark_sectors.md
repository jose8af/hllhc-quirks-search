# Scout note: dark sectors cluster

Data: `scout_dark_sectors.json` (163 papers, 19 candidate seeds, 151 logged queries). All IDs were returned by `inspire.py` (cached). Gap quotes were taken from PDF text via `arxiv_pdf.py` plus a raw (non-layout) pdftotext pass.

## Intellectual development
- Portals and hidden sectors (2000-2009): Holdom kinetic mixing, millicharged bounds (hep-ph/0001179), Higgs portal (hep-ph/0605188), "four basic ways" through a portal (1112.0493), inelastic DM (hep-ph/0101138). Hidden Valley (hep-ph/0604261) set up the LHC strategy of displaced decays of light states from a confining sector; pure-glue HV (0903.0883).
- Dark photon era (2008-2016): fixed-target and B-factory searches (0906.5614, BaBar 1406.2980), then collider reach via Higgs and Drell-Yan (1412.0018), lepton jets (1002.2952; ATLAS 1409.0746, 1210.0435).
- Strongly coupled dark sectors (2013-2016): dark QCD scale (1306.4676), SIMPs (1402.5143), emerging jets (1502.05409), semi-visible jets (1503.00009), SUEP (1612.00850), neutral naturalness and quirks (1501.05310, 1708.02243). CMS and ATLAS only began dedicated searches in 2021-2025 (CMS EJ 2403.01556, SUEP 2403.05311, lepton-enriched SVJ, ATLAS SVJ 2305.18037/2505.01634, ATLAS EJ 2505.02429, CMS low-mass HV dimuon 2511.11888).
- Community reports (2016-2022): Dark Sectors 2016 (1608.08632), Cosmic Visions (1707.04591), PBC (1901.09966), LLP white papers (1903.04497, 1806.07396), Snowmass dark showers (2203.09503), 2026 confining-sector review (2606.30760).
- Recent trend (2024-2026): shift from "can LHC see it" to model-space coverage: Z-portal and EW-charged dark mesons (2110.10691, 2401.08785, 2507.13430), enriched SVJ (leptons, photons, taus), ML tagging, trigger/scouting, forward LLP experiments (FASER quirk search 2607.26195).

## Gap checks (forward citations)
- 1701.08780 (displaced dark Higgs "left for future work"): forward citations with CMS/ATLAS filter show only prompt (WW, bb, HH*) mono-dark-Higgs searches. No displaced version found by title.
- 1508.03050 (iDM blind spot): followed up by CMS 2305.11649 and 2026 displaced-electron search. Gap partly closed. No ATLAS title hit.
- 1708.02243 (quirk trigger): followed by FASER first quirk search (2607.26195) not CMS/ATLAS.
- 2110.10691 (Z decays "overlooked"): CMS/ATLAS-filtered citations return only 2511.11888 (low-mass HV).
- 2409.04741 (ISR SVJ not explored): CMS/ATLAS enriched-SVJ searches exist but title-level search shows no photon-ISR search.

## Dead ends / cautions
- `abstract "..."` syntax in the methodology gave no hits; `abstracts.value:"..."` works. Title-level `collaboration:` queries miss searches with unusual titles, so "no CMS/ATLAS search found" is weak evidence.
- "lepton jets" title search is swamped by lepton+jets top measurements. "dark photon and date<2012 topcite" is empty because the term was coined later (use "hidden photon"/"paraphoton").
- Dark-sector cosmology/tension hits (e.g. "dark sector interaction") are unrelated and ignored.
- The tools directory is shared with other scouts; scratch files were kept in a private subdirectory.
- No numbers (limits, cross sections) were extracted from papers; the ~1.2 TeV dark-meson bound is quoted from the 2507.13430 abstract.
- Seeds 12-19 in the JSON are weak (breadth only): Higgs dark photon (well covered), low-mass dimuon (well covered), HNL lepton-jets (no gap quote).
- Several 2026 items (recids 3201494, 3186741, 3185627, 3193282) are conference contributions or CMS entries without arXiv ID; contents were not read.
