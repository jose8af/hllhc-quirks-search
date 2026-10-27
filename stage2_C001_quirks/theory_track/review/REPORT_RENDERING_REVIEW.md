# Rendering review (RP-render) of report/quirks_theory_report.pdf

Date: 2026-10-08. Page numbers below are the PRINTED numbers (cover unnumbered, so PDF page = printed + 1). All 45 PDF pages were viewed.

## Build check
Clean rebuild (`latexmk -C` then `latexmk -pdf -interaction=nonstopmode`) in a copy under the session scratchpad: exit 0, 45 pages, 0 errors, 0 LaTeX warnings, 0 Overfull/Underfull boxes, 0 undefined references/citations, 0 "??" in the extracted text. Build is clean.

## Verdict: ITERATE (0 A, 6 B, 9 C). No unreadable/broken content; the B items are layout/legibility fixes.

## Passes
Cover with status box and labels legend (fine); TOC present, correct page numbers, hyperlinked (blue); consistent header/footer on all numbered pages; math renders (Eqs. 1-3, subscripts, \lesssim, \tilde E); colour boxes (blue status, orange warning/errors, green EXPLOIT / amber WORTH A CHECK words) readable; long paths wrap in tables and mono text; cross-refs (Section, Table, Fig.) resolve; bibliography [1]-[33] fine; Fig. 1 and Fig. 2 (TikZ) crisp and legible.

## A (unreadable/broken)
None.

## B (should fix)
1. p.28: heading "6.1 To the project documents" is orphaned at the page bottom; its table starts on p.29 (and "(a1)" subheading is on p.29). Add keep-with-next / \needspace before the heading.
2. p.38: heading "10.3 Where the errors came from" is orphaned at the bottom; Table 21 is on p.39.
3. p.35 Fig. 13 (coverage map): in-plot labels are about 4-5 pt at page size and hard to read (box texts, "exclusive gamma gamma" strip, axis labels). Regenerate larger-font or rotate to a full-width landscape float.
4. p.11 Fig. 3 (T1 overview): axis labels, legend and in-plot annotations are ~4-5 pt; the title banner text is barely legible. Same for p.19-20 Figs. 9, 10, 11 (legends, subpanel y-labels in Fig. 10 are tiny) and Fig. 12 legend. Suggest enlarging fonts in the plotting scripts (or making the figures one-per-row).
5. p.24-26 Tables 8 and 9 (and p.27 Table 10 slightly): tables extend ~7 pt past the right text margin (they run past the header rule). Narrow the last column(s) or use \small with tabularx.
6. p.12-13 Figs. 4 and 5: each sits alone on a page with roughly half a page blank above and below (float placement); likewise p.21 (about 1/3 page blank before Table 6) and p.34 (about 2/3 blank after Table 17, caused by Fig. 13 float). Tighten with [t]/[!htbp] or reorder so text fills the gaps; with B3 fixed the blanks may disappear.

## C (polish)
1. p.2: Section 1 starts on the TOC continuation page (p.3 printed, after the TOC tail); insert \clearpage after \tableofcontents.
2. p.1: executive summary is a dense wall of nested bullets with long inline numbers; a CMS reader would benefit from a 4-5 line "key numbers" table or bold run-in headers (already partly there). Acronyms IT/OT/PS/2S, BTL, PU, HSCP, JFC, SBI, MET-strip are used on first appearance (pp.1-3) without definition; the glossary is only on p.44 and is not pointed to. Add "see Appendix C" in the exec summary and define JFC on p.1.
3. p.13 Fig. 5 top-right: the "NR limit 2/3" annotation overlaps the panel title; bottom-left y-axis has no label.
4. p.16 Fig. 7: legend in the m_Q = 200 GeV panel overlaps the data points and the dashed formula line; move legend outside or to an empty corner.
5. p.38 Fig. 14: x-axis tick labels collide ("3x10^4" overlapping "4x10^0"); the withdrawn-figure caption is otherwise clear.
6. p.26 Table 9 Status column: words break as "UNVERI-FIED", "au-dited"; widen column or use \raggedright.
7. p.29-31: Tables 12 and 13 are uncaptioned (counter jumps from Table 11 to Table 14); add short captions or use unnumbered tables consistently.
8. p.8 and p.7: about 1/3 page blank before Fig. 1 / after 3.1 (float spacing).
9. p.19 Fig. 11 right: legend text small; Fig. 10 panel labels "(a) ... (a) ... (a)" are all "(a)" in the top row (and "(b)" in the bottom row), which is confusing; should read (a1) (a2) (a3) or similar.
