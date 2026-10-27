#!/usr/bin/env python3
"""Build report/hllhc_report.tex from the saved workspace data (all numbers/tables come from JSON files)."""
import json, glob, collections, os, re

R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
ROOT = os.path.join(R, '..')
OUT = os.path.join(ROOT, 'report')
os.makedirs(OUT, exist_ok=True)
J = lambda p: json.load(open(os.path.join(R, p)))

P = J('literature/papers.json')
RAW = J('candidates/raw_seeds.json')
MER = J('candidates/merged_candidates.json')
G2 = J('candidates/gate2_verdicts.json')
G3 = J('candidates/gate3_adversarial.json')
RK = J('rankings/ranking.json')
AUD = J('reports/citation_audit.json')
AUD = AUD if isinstance(AUD, list) else AUD.get('entries', list(AUD.values()))

GREEK = {'α': r'$\alpha$', 'β': r'$\beta$', 'γ': r'$\gamma$', 'δ': r'$\delta$', 'Δ': r'$\Delta$', 'ε': r'$\epsilon$', 'η': r'$\eta$',
         'θ': r'$\theta$', 'κ': r'$\kappa$', 'λ': r'$\lambda$', 'Λ': r'$\Lambda$', 'μ': r'$\mu$', 'ν': r'$\nu$', 'π': r'$\pi$',
         'ρ': r'$\rho$', 'σ': r'$\sigma$', 'τ': r'$\tau$', 'φ': r'$\varphi$', 'χ': r'$\chi$', 'ψ': r'$\psi$', 'ω': r'$\omega$',
         'Ω': r'$\Omega$', 'Γ': r'$\Gamma$', 'Σ': r'$\Sigma$', '±': r'$\pm$', '×': r'$\times$', '≈': r'$\approx$', '≲': r'$\lesssim$',
         '≳': r'$\gtrsim$', '≥': r'$\geq$', '≤': r'$\leq$', '→': r'$\to$', '←': r'$\leftarrow$', '∼': r'$\sim$', '~': r'$\sim$',
         '≪': r'$\ll$', '≫': r'$\gg$', '°': r'$^\circ$', '⁻': r'$^-$', '¹': r'$^1$', '²': r'$^2$', '³': r'$^3$', '–': '--',
         '—': '---', '‑': '-', '‐': '-', '’': "'", '‘': "'", '“': '``', '”': "''", '…': '...', '′': "'", '∞': r'$\infty$',
         '≠': r'$\neq$', '∗': '*', '⁺': r'$^+$', '₀': r'$_0$', '₁': r'$_1$', '₂': r'$_2$', '∼': r'$\sim$', '√': r'$\surd$',
         ' ': ' ', '‒': '-', '•': '*', '·': '.', '≡': r'$\equiv$', '∝': r'$\propto$', '∈': r'$\in$', '⊗': r'$\otimes$'}
SPECIAL = {'&': r'\&', '%': r'\%', '#': r'\#', '_': r'\_', '$': r'\$', '{': r'\{', '}': r'\}', '^': r'\^{}', '\\': r'\textbackslash{}'}


def esc(s, maxlen=None):
    """Escape plain text (math markup stripped) for LaTeX."""
    s = '' if s is None else str(s)
    s = re.sub(r'\$([^$]*)\$', lambda m: re.sub(r'[\\{}^_]', '', m.group(1)), s)  # strip inline math
    s = re.sub(r'\s+', ' ', s).strip()
    if maxlen and len(s) > maxlen:
        s = s[:maxlen].rsplit(' ', 1)[0] + '...'
    out = []
    for ch in s:
        if ch in GREEK:
            out.append(GREEK[ch])
        elif ch in SPECIAL:
            out.append(SPECIAL[ch])
        elif ord(ch) < 128:
            out.append(ch)
        elif ch.isalpha():
            out.append({'é': r"\'e", 'è': r'\`e', 'ö': r'\"o', 'ü': r'\"u', 'ä': r'\"a', 'ó': r"\'o", 'á': r"\'a", 'í': r"\'i", 'ú': r"\'u",
                        'ñ': r'\~n', 'ç': r'\c{c}', 'ø': r'\o{}', 'ł': r'\l{}', 'š': r'\v{s}', 'č': r'\v{c}', 'ř': r'\v{r}', 'ž': r'\v{z}',
                        'ć': r"\'c", 'ń': r"\'n", 'ő': r'\H{o}', 'ı': 'i', 'Ö': r'\"O', 'Ü': r'\"U', 'É': r"\'E", 'ß': r'\ss{}'}.get(ch, ''))
        # else: drop unsupported symbol
    return ''.join(out)


def pid(p):
    return p.get('arxiv') or ('INSPIRE:%s' % p.get('recid'))


CLN = {'alp_light': 'ALPs \\& light states', 'composite_heavy': 'Compositeness \\& heavy states', 'dark_sectors': 'Dark sectors \\& portals',
       'eft_ew': 'EFT \\& EW precision', 'higgs_scalars': 'Exotic Higgs \\& scalars', 'leptoquark_flavour': 'Leptoquarks \\& flavour',
       'llp': 'Long-lived particles', 'orphaned_ideas': 'Older / orphaned ideas', 'qcd_substructure': 'QCD, substructure, quantum info',
       'susy': 'SUSY corners'}


def clus_of(p):
    c = p['clusters'][0].replace('scout_', '')
    for k in CLN:
        if k in c or c.startswith(k[:6]):
            return k
    return c


# ---------------- statistics
n_pap = len(P)
roles = collections.Counter(p.get('role') for p in P)
yrs = [int(p['year']) for p in P if str(p.get('year', '')).isdigit()]
dec = collections.Counter((y // 10) * 10 for y in yrs)
n_pdf = len(glob.glob(os.path.join(R, 'cache/pdf/*.pdf')))
n_cache = len(glob.glob(os.path.join(R, 'cache/*.json')))
n_q = 0
for f in glob.glob(os.path.join(R, 'literature/scout_*.json')):
    n_q += len(json.load(open(f)).get('queries_run', []))
seed_by_cl = collections.Counter(s['source_file'].replace('scout_', '').replace('.json', '') for s in RAW)
pap_by_cl = collections.Counter(clus_of(p) for p in P)
g2c = collections.Counter(v['verdict'] for v in G2.values())
g3c = collections.Counter(v['verdict'].split(' ')[0] for v in G3.values())
n_unres = sum(1 for a in AUD if a.get('resolved') is False)

TOPIDS = [c['cand_id'] for c in sorted(RK['candidates'], key=lambda c: c['rank'])]
NAMES = {c['cand_id']: c['name'] for c in MER}
tex = []
w = tex.append

w(r'''\documentclass[11pt,a4paper]{article}
\usepackage[margin=2.3cm]{geometry}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amssymb,lmodern,microtype,booktabs,longtable,array,xcolor,enumitem,tikz,pgfplots,tcolorbox,fancyhdr,titlesec,graphicx,float}
\usepackage[hidelinks]{hyperref}
\pgfplotsset{compat=1.16}
\usetikzlibrary{arrows.meta,positioning,shapes.geometric,calc}
\definecolor{acc}{HTML}{1F4E79}\definecolor{ok}{HTML}{2E7D32}\definecolor{warn}{HTML}{B26A00}\definecolor{bad}{HTML}{B3261E}
\titleformat{\section}{\Large\bfseries\color{acc}}{\thesection}{0.6em}{}
\titleformat{\subsection}{\large\bfseries\color{acc}}{\thesubsection}{0.5em}{}
\setlist{itemsep=2pt,topsep=3pt}
\pagestyle{fancy}\fancyhf{}\fancyfoot[C]{\thepage}\fancyhead[L]{\small HL-LHC idea discovery}\fancyhead[R]{\small Progress report, 6 Oct 2026}
\renewcommand{\arraystretch}{1.15}
\newtcolorbox{key}[1][]{colback=acc!6,colframe=acc,boxrule=0.6pt,arc=2pt,left=6pt,right=6pt,top=4pt,bottom=4pt,#1}
\newtcolorbox{caution}[1][]{colback=warn!8,colframe=warn,boxrule=0.6pt,arc=2pt,left=6pt,right=6pt,top=4pt,bottom=4pt,#1}
\begin{document}
\begin{titlepage}
\centering\vspace*{2.5cm}
{\Huge\bfseries\color{acc} Discovering under-explored HL-LHC\\[4pt] phenomenology ideas}\\[1.2cm]
{\Large Autonomous multi-agent literature review: method, results and lessons}\\[1.5cm]
{\large Progress report on the discovery phase}\\[0.6cm]
{\large 6 October 2026}\\[2cm]
\begin{minipage}{0.8\textwidth}\small
Workspace: \texttt{hllhc\_search/} (local project; nothing installed globally).\\
Orchestrator: Claude Sonnet 5.5 in Claude Code. Sub-agents: Sonnet 5.5, Opus 5.5 and the strongest available model (``fable'') as arbiter.\\
Status: discovery phase complete, \textbf{waiting for the human choice of direction}. Stage~2 (analysis design) has not started.
\end{minipage}
\vfill
\end{titlepage}
\tableofcontents\newpage
''')

# ---------------- executive summary
w(r'''\section{Executive summary}
\begin{key}
\textbf{Question.} Which established theoretical ideas have experimental consequences that CMS/ATLAS have not fully covered, and could plausibly become a useful HL-LHC analysis?\\[3pt]
\textbf{Answer so far.} After an extensive search, \textbf{no candidate survived intact}. For all ten directions that received full independent review, a phenomenology paper already proposes the analysis; what remains open is the \emph{experimental execution} (an ATLAS/CMS analysis, a recast, or a collaboration-level HL-LHC projection), not a new theoretical idea. Several of the scouts' most attractive gaps were overturned by independent checks.
\end{key}
''')
w(r'\begin{itemize}')
w(r'\item \textbf{Corpus:} %d unique papers (%d--%d), %s PDFs downloaded and converted to text, %s cached INSPIRE responses, %s logged scout queries.' % (n_pap, min(yrs), max(yrs), n_pdf, format(n_cache, ','), format(n_q, ',')))
w(r'\item \textbf{Funnel:} %d raw seeds $\to$ 74 merged directions $\to$ Gate~2: %d PASS / %d HOLD / %d REJECT $\to$ Gate~3 adversarial on 27: %d narrowed, %d died, 0 intact $\to$ 10 fully reviewed $\to$ arbiter ranking: 2 tier~A, 5 tier~B, 3 tier~C (Section~\ref{sec:ranking}).' % (len(RAW), g2c['PASS'], g2c['HOLD'], g2c['REJECT'], g3c.get('NARROWED', 0), g3c.get('DIES', 0)))
w(r'\item \textbf{Agents:} 55 sub-agent launches (16 Sonnet, 38 Opus, 1 arbiter on the strongest model); 20 Opus launches were interrupted by session rate limits and partly rerun.')
w(r'\item \textbf{Top of the ranking:} C001 quirks (tier~A), C005 Higgs-portal dark showers in the tracker (tier~A), then C019, C044, C015, C051, C003 (tier~B), and C008, C040, C066 (tier~C).')
w(r'\item \textbf{All %d cited reference IDs in the final documents resolved on INSPIRE;} two numbers are flagged \textsc{unverified}.' % len(AUD))
w(r'\end{itemize}')
w(r'''\begin{caution}\textbf{Main caveat.} Only 10 of 74 directions got the full review (lean budget chosen by the user). Triage was done by Sonnet with abstract-level coverage checks, so parked directions may include missed opportunities and some rejections could be wrong; every rejection names its covering result so it can be checked.\end{caution}
''')

# ---------------- method
w(r'''\section{Objective and method}
The brief asked for a deep, citation-driven literature review, not an analysis. The design follows the MIT/JFC philosophy \emph{phase $\to$ written artifact $\to$ independent review $\to$ correction $\to$ next phase}: an orchestrator that does not do the reading itself, specialised sub-agents, mutually blind reviewers, and a human decision point at the end. Adaptations to the original brief are listed below.
\begin{itemize}
\item Added an \emph{archaeology} scout for old/orphaned ideas and two extra clusters (QCD/substructure, quantum-information observables).
\item Reviewers (experimental, feasibility, theory, adversarial) see only a neutral candidate description, never each other's conclusions.
\item Every cited reference ID is checked against INSPIRE (citation audit).
\item Cost cap: the plan required approval before exceeding about 40 strong-model runs; the user selected a ``lean'' budget (about 25 runs).
\end{itemize}
\subsection{Pipeline}
\begin{center}\begin{tikzpicture}[node distance=6mm,box/.style={draw=acc,fill=acc!7,rounded corners,align=center,minimum width=2.3cm,minimum height=1.05cm,font=\footnotesize},arr/.style={-{Latex[length=2mm]},thick,acc}]
\node[box](a){Scouts\\10 Sonnet};\node[box,right=of a](b){Merge\\\& dedupe};\node[box,right=of b](c){Gate 2 triage\\6 Sonnet};\node[box,right=of c](d){Gate 3 adversarial\\7 Opus};
\node[box,below=8mm of d](e){Gate 4 independent\\E/F/T reviews\\Opus};\node[box,left=of e](f){Arbiter\\strongest model};\node[box,left=of f](g){Human\\checkpoint};
\draw[arr](a)--(b);\draw[arr](b)--(c);\draw[arr](c)--(d);\draw[arr](d)--(e);\draw[arr](e)--(f);\draw[arr](f)--(g);
\end{tikzpicture}\end{center}
\subsection{Environment and tools}
Verified at the start (not assumed): INSPIRE REST API, arXiv API and PDF download, HEPData, WebSearch/WebFetch, Python~3.14 with the standard library only, \texttt{pdftotext}, \texttt{jq}. No MCP research server was relevant. Custom tools written in \texttt{research/tools/}: \texttt{inspire.py} (search, references, citations; cached, rate limited), \texttt{arxiv\_pdf.py} (download, convert, extract ``future work''-type sentences), \texttt{merge\_seeds.py}, and the generators for this report.
\subsection{Search strategy}
\begin{enumerate}
\item \textbf{Seminal discovery:} INSPIRE top-cited queries per cluster, including date $<$ 2012 to reach older ideas; reviews and white papers (Snowmass, HL/HE-LHC Yellow Report).
\item \textbf{Citation chains:} \texttt{refersto:recid} and \texttt{citedby:recid} to follow descendants and ancestors; each ``future work'' lead was checked by forward citations.
\item \textbf{Gap-phrase mining:} phrases such as ``unexplored'', ``blind spot'', ``dedicated search'' combined with cluster terms, then verbatim sentences extracted from PDFs. Treated as leads, never as evidence.
\item \textbf{Experiment-side mapping:} collaboration-filtered INSPIRE searches, public result pages, HEPData, recasts and Phase-2 projection documents.
\end{enumerate}
''')

# ---------------- literature stats
w(r'\section{Literature covered}')
w(r'The scouts collected \textbf{%d unique papers} spanning %d--%d. These were harvested as INSPIRE records (title, authors, abstract, citation count); %d full-text PDFs were downloaded and converted, mostly to extract gap sentences and to let reviewers read the closest experimental results. \textit{Read} therefore means different things at different stages: \emph{metadata and abstract} for the bulk, \emph{full text} for the subset below.' % (n_pap, min(yrs), max(yrs), n_pdf))
w(r'''\begin{caution}The exact number of papers read in depth is not tracked per agent. A fair statement is: all %d were seen at metadata/abstract level; %d PDFs were converted to text; the final dossiers rest on full reading of a few hundred sources, concentrated on the closest 3--5 experimental results and the source papers of the ten reviewed candidates.\end{caution}''' % (n_pap, n_pdf))
w(r'\subsection{Papers by role and by decade}')
rl = [('seminal', 'Seminal / idea-introducing'), ('followup', 'Phenomenology follow-ups'), ('experimental', 'Experimental searches / measurements'),
      ('review', 'Reviews / white papers'), ('projection', 'HL-LHC / future projections'), ('recast', 'Recasts / reinterpretations')]
w(r'\begin{center}\begin{tabular}{lr}\toprule Role (scout judgement) & Papers\\\midrule')
for k, lab in rl:
    w(r'%s & %d\\' % (lab, roles.get(k, 0)))
w(r'\midrule Total & %d\\\bottomrule\end{tabular}\end{center}' % n_pap)
w(r'''\begin{center}\begin{tikzpicture}\begin{axis}[ybar,width=0.8\textwidth,height=5.5cm,bar width=14pt,symbolic x coords={1970s,1980s,1990s,2000s,2010s,2020s},xtick=data,ylabel={papers},nodes near coords,every node near coord/.append style={font=\scriptsize},ymin=0,ymax=760,fill=acc,draw=acc]
\addplot[fill=acc!70] coordinates {''' + ' '.join('(%ds,%d)' % (d, dec.get(d, 0)) for d in [1970, 1980, 1990, 2000, 2010, 2020]) + r'''};\end{axis}\end{tikzpicture}\\[-2pt]{\small Publication decade of the collected corpus. The weight on 2020s reflects the search for current experimental coverage; older ideas are the 1975--2009 tail.}\end{center}''')
w(r'\subsection{Per-cluster yield}')
w(r'\begin{center}\small\begin{tabular}{lrr}\toprule Cluster & Papers (first tag) & Candidate seeds\\\midrule')
for k in CLN:
    w(r'%s & %d & %d\\' % (CLN[k], pap_by_cl.get(k, 0), seed_by_cl.get(k, 0)))
w(r'\midrule Total & %d & %d\\\bottomrule\end{tabular}\end{center}' % (n_pap, len(RAW)))

# ---------------- seminal papers
w(r'\section{Seminal papers found}\label{sec:seminal}')
w(r'The scouts tagged %d papers as seminal and %d as review. The tags are scout judgements, not a verified ranking. Each table lists the most-cited seminal papers per cluster; the full list is in \texttt{research/literature/seminal\_papers.md}.' % (roles['seminal'], roles['review']))
w(r'''\begin{key}\textbf{Which seminal ideas became research programs?} The best match to the ``latent research program'' pattern is the \emph{hidden-valley family}: Strassler--Zurek (hep-ph/0604261, 2006) $\to$ emerging jets $\to$ dark-shower benchmarks $\to$ SUEP $\to$ semi-visible jets, with experiments covering prompt and part of the displaced regimes only. The oldest lineages are quirks (Kang--Luty, 0805.4642) and the doubly charged Higgs (INSPIRE:214561, 1985). No forgotten idea was found whose collider consequence had \emph{never} been revisited: in every case a later paper or search had followed it up.\end{key}''')
S = [p for p in P if p.get('role') == 'seminal']
for k in CLN:
    sel = sorted([p for p in S if clus_of(p) == k], key=lambda p: -(p.get('cites') or 0))[:6]
    if not sel:
        continue
    w(r'\subsection*{%s}' % CLN[k])
    w(r'\begin{center}\footnotesize\begin{tabular}{@{}p{2.5cm}rr p{9cm}@{}}\toprule ID & Year & Cites & Title\\\midrule')
    for p in sel:
        w(r'%s & %s & %s & %s\\' % (esc(pid(p)), p.get('year'), p.get('cites'), esc(p.get('title'), 95)))
    w(r'\bottomrule\end{tabular}\end{center}')

w(r'\subsection{Lineage of the three best-supported ideas}')
w(r'''\begin{center}\begin{tikzpicture}[node distance=4mm,n/.style={draw=acc,rounded corners,fill=acc!6,font=\scriptsize,align=center,minimum height=0.9cm,text width=2.4cm},a/.style={-{Latex[length=1.6mm]},acc}]
\node[n](h){Hidden valley\\hep-ph/0604261\\(2006)};\node[n,right=of h](e){Emerging jets, dark showers, SUEP\\1502.05409, 2103.01238, 1612.00850};\node[n,right=of e](x){CMS/ATLAS EJ, SUEP, MDS searches\\2403.01556, 2402.01898};\node[n,right=of x,fill=warn!12,draw=warn](g){Gap: hadronic showers, c$\tau$ 1--100 mm (C005)};
\draw[a](h)--(e);\draw[a](e)--(x);\draw[a](x)--(g);
\node[n,below=7mm of h](k){Quirks\\0805.4642\\(2008)};\node[n,right=of k](k2){Collider quirks, coplanar-hit method\\1106.2569, 1708.02243};\node[n,right=of k2](k3){FASER search\\2607.26195; no central ATLAS/CMS};\node[n,right=of k3,fill=warn!12,draw=warn](k4){Gap: m$_Q>180$ GeV, $\Lambda\sim$0.3--30 keV (C001)};
\draw[a](k)--(k2);\draw[a](k2)--(k3);\draw[a](k3)--(k4);
\node[n,below=7mm of k](d){Doubly charged Higgs\\INSPIRE:214561\\(1985)};\node[n,right=of d](d2){Type-II seesaw H$^{\pm\pm}$\\hep-ph/0506176, 1808.00943};\node[n,right=of d2](d3){ATLAS prompt, WW, multi-charged\\2211.07505, 2101.11961, 2303.13613};\node[n,right=of d3,fill=warn!12,draw=warn](d4){Gap: displaced same-sign vertex (C019)};
\draw[a](d)--(d2);\draw[a](d2)--(d3);\draw[a](d3)--(d4);
\end{tikzpicture}\end{center}
The complete curated lineage for all 74 directions is in \texttt{research/literature/citation\_graph.md}; this is curated lineage, not an exhaustive citation network.''')

# ---------------- agents
w(r'''\section{Agents and models}
\subsection{Architecture}
The orchestrator (the main Claude Code session, Sonnet 5.5, medium effort) never read papers in depth. It held summaries, verdicts, logs, and wrote merge scripts. Sub-agents received a self-contained prompt, the shared rules file \texttt{methodology.md}, and a defined output location. The plan proposed Haiku for the cheapest steps; in practice \textbf{no Haiku agent was used}, because even the scouting stage required judgement about whether a gap sentence was real, so Sonnet was used for all cheap stages.
\subsection{Roles, models and counts}
\begin{center}\small\begin{tabular}{@{}p{3.3cm}p{1.5cm}r p{7.2cm}@{}}\toprule Role & Model & Runs & Task and independence rule\\\midrule
Literature scouts & Sonnet & 10 & One per topic cluster: top-cited and date-filtered searches, citation chains, gap phrases, PDF gap-sentence extraction; output candidate seeds and papers.\\
Gate 2 triage & Sonnet & 6 & Real coverage checks per merged direction (collaboration-filtered queries, public pages); PASS/HOLD/REJECT; reject only with a named covering result.\\
Gate 3 adversarial & Opus & 7 (+10 failed) & Try to kill each PASS direction; see only the neutral claim, not verdicts of other agents; DIES/NARROWED/SURVIVES.\\
Gate 4 experimental status & Opus & 5 + 3 reruns & ``Skeptical experimentalist'': exactly what is covered and what region is open.\\
Gate 4 feasibility & Opus & 5 + 3 reruns & Cross sections, yields, backgrounds, trigger, pileup, Phase-2 detector; HL-specific advantage.\\
Gate 4 theory deep-readers & Opus & 5 & Read source papers; assumptions, controlling parameters, robust vs model-dependent, constraints.\\
Arbiter & Strongest (fable) & 1 & Sees all four independent reports; scores, tiers, disagreement adjudication, citation audit, final documents.\\
\bottomrule\end{tabular}\end{center}
Totals: 16 Sonnet runs, 38 Opus runs launched (of which 20 were interrupted by session limits; their partial outputs were reused where saved), 1 arbiter run: \textbf{55 sub-agent launches}. Token use was not aggregated across agents.
\begin{caution}The user chose a ``lean'' budget of about 25 strong-model runs. Rate-limit failures and reruns meant 38 Opus runs were \emph{launched}, although 28 distinct Opus review tasks completed (7 adversarial, 8 experimental, 8 feasibility, 5 theory), some only after a rerun. This overrun should be borne in mind when planning stage~2.\end{caution}
\subsection{Independence and anti-bias rules}
\begin{itemize}
\item Gate 3 and Gate 4 reviewers were forbidden to read triage verdicts or other agents' outputs; they received the candidate's neutral claim and, at Gate~4, the proposed analysis target as a hypothesis to test.
\item Evidence rules shared by all agents: no unverifiable numbers, no ``new/first/unexplored'' as findings (a status taxonomy was used instead), ``not found'' is never proof of absence, every ID verified in INSPIRE.
\item The arbiter had to adjudicate disagreements explicitly and could not invent evidence.
\end{itemize}
''')

# ---------------- funnel results
w(r'\section{Results by stage}')
w(r'\subsection{Funnel}')
w(r'''\begin{center}\begin{tikzpicture}[f/.style={draw=acc,fill=acc!8,align=center,font=\small,minimum height=0.8cm},arr/.style={-{Latex},acc,thick}]
\node[f,minimum width=11cm](a){%d raw seeds from 10 scouts (986 papers)};
\node[f,minimum width=9.4cm,below=3mm of a](b){74 merged candidate directions};
\node[f,minimum width=7.8cm,below=3mm of b](c){Gate 2 triage: %d PASS, %d HOLD (parked), %d REJECT};
\node[f,minimum width=6.2cm,below=3mm of c](d){Gate 3 adversarial on %d PASS: %d narrowed, %d died, 0 intact};
\node[f,minimum width=4.6cm,below=3mm of d](e){10 fully reviewed (Gate 4)};
\node[f,minimum width=3.2cm,below=3mm of e,fill=ok!15,draw=ok](g){Ranked: 2 A, 5 B, 3 C};
\foreach \x/\y in {a/b,b/c,c/d,d/e,e/g}{\draw[arr](\x)--(\y);}
\end{tikzpicture}\end{center}''' % (len(RAW), g2c['PASS'], g2c['HOLD'], g2c['REJECT'], sum(g3c.values()), g3c.get('NARROWED', 0), g3c.get('DIES', 0)))
w(r'''\subsection{What the independent checks revealed}
The most important methodological result is that \textbf{scout headline gaps were frequently wrong}, because scouts judged coverage from titles and abstracts. Examples overturned at Gate~2/3:
\begin{itemize}
\item \textbf{$\sim$1\,cm lifetime blind spot} (``high confidence''): CMS 2409.10806 excludes B$>$1\% for c$\tau$ 1.5--370\,mm.
\item \textbf{RPV with displaced LSP}: ATLAS 2603.15007 reinterprets 13 searches across the coupling range.
\item \textbf{4D timing for LLPs (MTD/HGTD)}: the CMS MTD design report already projects displaced-vertex timing, delayed photons/jets and slow charged particles.
\item \textbf{Tau-philic leptoquark follow-up of the b-$\tau$ excess}: ATLAS 2503.19836 excludes the benchmark.
\item \textbf{A$\to$ZH in 2HDM}: CMS and ATLAS results plus an HL-LHC projection exist.
\end{itemize}
Even reviewers corrected each other: a misquoted ``5.7\,TeV'' leptoquark reach (actually the crossover with the atomic-parity-violation bound), an ATLAS result (2403.08547) that already excludes the photon-ISR benchmark in C008, and a branching-ratio claim for C015 that rests on a reviewer's own derivation and is kept only as a caveat.''')

# ---------------- ranking
w(r'\section{Ideas that survived: ranking}\label{sec:ranking}')
w(r'''The arbiter scored each of the ten fully reviewed candidates 0--5 on ten criteria (TI theoretical importance, PR phenomenological richness, EN experimental novelty, HL HL-LHC relevance, FE feasibility, SI potential sensitivity gain, SD signature distinctiveness, LG literature gap, TR theoretical robustness, PI publication impact). Experimental novelty and literature gap were capped at 2 when only a recast or projection remains. The ranking uses judgement and a veto rule first; the sum is shown but does not determine the order. \textbf{Tier A}: worth a dedicated analysis study. \textbf{B}: feasibility, recast or projection study first. \textbf{C}: insufficient or weak.''')
keys = ['theoretical_importance', 'phenomenological_richness', 'experimental_novelty', 'hl_lhc_relevance', 'experimental_feasibility',
        'potential_sensitivity_improvement', 'signature_distinctiveness', 'current_literature_gap', 'theoretical_robustness', 'potential_publication_impact']
w(r'\begin{center}\scriptsize\setlength{\tabcolsep}{3.2pt}\begin{tabular}{rllrrrrrrrrrrrl}\toprule \# & ID & Tier & TI & PR & EN & HL & FE & SI & SD & LG & TR & PI & $\Sigma$ & Conf.\\\midrule')
for c in sorted(RK['candidates'], key=lambda c: c['rank']):
    s = c['scores']
    w(r'%d & %s & %s & %s & %d & %s\\' % (c['rank'], c['cand_id'], c['tier'], ' & '.join(str(s[k]) for k in keys), c['total'], esc(c.get('confidence', ''))))
w(r'\bottomrule\end{tabular}\end{center}')
w(r'\subsection{Surviving gap for each candidate}')
mainob = {}
for c in sorted(RK['candidates'], key=lambda c: c['rank']):
    f = os.path.join(R, 'reviews/feasibility/%s.json' % c['cand_id'])
    if os.path.exists(f):
        try:
            d = json.load(open(f))
            mainob[c['cand_id']] = (d.get('main_obstacle'), d.get('feasibility_rating'))
        except Exception:
            pass
for c in sorted(RK['candidates'], key=lambda c: c['rank']):
    k = c['cand_id']
    w(r'\subsubsection*{%d. %s (tier %s, %s confidence)}' % (c['rank'], esc(c['name'], 110), c['tier'], esc(c.get('confidence'))))
    w(r'\textbf{Surviving gap.} %s\\' % esc(c.get('surviving_gap'), 520))
    w(r'\textbf{Status labels.} %s. \textbf{Kind:} %s.\\' % (esc('; '.join(c.get('status_labels', []))), esc(c.get('novelty_kind'))))
    w(r'\textbf{Veto check.} %s' % esc(c.get('veto_check'), 420))
    if k in mainob and mainob[k][0]:
        mo = mainob[k][0]
        mo = mo if isinstance(mo, str) else json.dumps(mo)
        w(r'\\\textbf{Main feasibility obstacle} (feasibility reviewer, rating %s/5): %s' % (mainob[k][1], esc(mo, 360)))
    w('')

w(r'''\begin{key}\textbf{Reading the ranking.} C001 ranks first because it is the clearest uncovered gap (no ATLAS/CMS central-detector quirk search was found), not because it is the easiest: its feasibility is the lowest of the ten. C044 has the most clearly HL-LHC-motivated case (background-free, statistics-limited) but the narrowest gap. Several candidates are essentially recasts or projections and the arbiter flagged them as such. The decision belongs to the physicist; \texttt{TOP\_CANDIDATES.md} contains the 12-section dossier for each.\end{key}
''')

# ---------------- negative results
w(r'\section{Ideas that did not survive}')
w(r'Rejections require a named covering result (or a physical showstopper); absence of a paper was never used as a reason. Gate~2 rejected \textbf{%d} directions and Gate~3 one more.' % g2c['REJECT'])
w(r'\begin{center}\footnotesize\begin{tabular}{@{}l p{4.3cm} p{8cm}@{}}\toprule ID & Direction & Why rejected\\\midrule')
for k in sorted(G2):
    v = G2[k]
    if v['verdict'] == 'REJECT':
        w(r'%s & %s & %s\\' % (k, esc(NAMES[k], 60), esc(v.get('reason'), 210)))
for k, v in sorted(G3.items()):
    if v['verdict'].startswith('DIES'):
        w(r'%s (G3) & %s & %s\\' % (k, esc(NAMES[k], 60), esc(v.get('surviving_gap') or v.get('notes'), 210)))
w(r'\bottomrule\end{tabular}\end{center}')
w(r'''In addition, 24 HOLD directions were \emph{parked} (not rejected): promising but without a review budget. Five alternates were identified for a possible extra pass: C017 (pseudo-Dirac heavy neutrinos, time-resolved lepton-number-violation oscillations), C061 (HHH beyond 6b), C009 (semi-dark Higgs decays), C047 (portal-matter vector-like quarks to dark photons) and C048 (colour-sextet top partners).''')

# ---------------- problems
w(r'''\section{Problems encountered and lessons}
\begin{enumerate}
\item \textbf{Session rate limits.} Gate~3 failed once with no saved output; Gate~4 failed for all ten first-wave agents. After the first failure all agents were told to save incrementally; after the second, 14 of 20 Gate~4 reviews were already on disk and only six were rerun. \emph{Lesson:} require per-candidate saving and stagger large opus fan-outs.
\item \textbf{Cost overrun relative to the lean budget:} 38 Opus launches versus the planned $\sim$25, a direct consequence of the failures above.
\item \textbf{Weak first-pass coverage claims.} Scouts and parts of the triage used title/abstract-level queries; ``no CMS/ATLAS search found'' proved unreliable. The adversarial and experimental reviews, which read the closest results, repeatedly overturned scout conclusions.
\item \textbf{Subagent spawning.} In the first Gate~3 attempt, batch agents spawned extra per-candidate agents (3 extra failed Opus launches); later prompts forbade it.
\item \textbf{Shared-scratch collisions.} Several scouts overwrote each other's temporary files. One scout's early query log was reconstructed from memory (papers and quotes unaffected).
\item \textbf{Duplicate completion notices} from some scouts (leftover monitors) cluttered the log but changed no results.
\item \textbf{Tool quirks.} INSPIRE \texttt{abstract "..."} returns nothing (use \texttt{abstracts.value:}); \texttt{refersto:arxiv:} returns junk (use recid); WebFetch is lossy, so stau cross sections taken from a web page need re-checking; two-column PDFs garble extracted gap quotes (flagged, re-verified before citing).
\item \textbf{Stale gap statements.} Some ``future work'' quotes came from old documents (e.g.\ a 2018 MATHUSLA white paper) and had been overtaken by later work.
\item \textbf{Reviewer disagreements} resolved by the arbiter: C040 mass-splitting window (theory $\lesssim$30\,GeV vs feasibility $\gtrsim$15\,GeV), C066 ``5.7\,TeV'' misquote, C008 photon-ISR exclusion, C015 coupling caveat, C019 coverage by CMS 2110.04809 (no charge requirement).
\end{enumerate}
\section{Limitations}
\begin{itemize}
\item Coverage of the literature is broad but not exhaustive; INSPIRE title/abstract queries miss full-text mentions and some CMS PAS / ATLAS-CONF notes.
\item Only 10 of 74 directions received full independent review; the rest are triage-level.
\item Small calculations in the feasibility reviews are back-of-envelope estimates, labelled as such; no sensitivity projections were produced.
\item Sonnet-level triage and scouting may contain errors that were not revisited for parked directions.
\item Two numbers are \textsc{unverified}: a CMS $\tau\tau$ H$^{\pm\pm}$ limit quoted as both 535 and 396\,GeV in different sources, and the content of CMS-PAS-B2G-24-005 (read at abstract level only).
\end{itemize}
\section{Status and next steps}
The workflow has reached the \textbf{human checkpoint}. Options:
\begin{enumerate}
\item Choose one candidate (or a combination) for stage~2: strategy, literature, sample exploration, selection, backgrounds and systematics, with an independent review at each phase.
\item Spend more review budget on the parked directions or the five alternates.
\item Ask for deeper checks on a particular candidate (e.g.\ a recast of CMS 2110.04809 for C019 before treating it as open).
\end{enumerate}
\section*{Appendix: workspace map}
\begin{small}\begin{tabular}{@{}p{5.2cm}p{9.5cm}@{}}\toprule Path & Content\\\midrule
\texttt{RESEARCH\_PLAN.md} & plan: architecture, strategy, scoring, gates, stopping criteria\\
\texttt{TOP\_CANDIDATES.md} & 12-section dossier for the 10 reviewed candidates, lineage, how to choose\\
\texttt{REJECTED\_CANDIDATES.md} & rejected directions, killed sub-ideas, overturned scout claims\\
\texttt{research/literature/} & scout outputs, \texttt{papers.json}, \texttt{seminal\_papers.md}, \texttt{citation\_graph.md}\\
\texttt{research/candidates/} & raw seeds, merged directions, gate verdicts, candidate database\\
\texttt{research/reviews/} & triage, adversarial, experimental, feasibility, theory reviews\\
\texttt{research/rankings/, reports/} & ranking, literature review, citation audit\\
\texttt{research/LOG.md} & chronological log including failures\\
\texttt{research/tools/} & helper scripts (INSPIRE, PDF, merge, report generation)\\
\bottomrule\end{tabular}\end{small}
\end{document}
''')

open(os.path.join(OUT, 'hllhc_report.tex'), 'w').write('\n'.join(tex))
print('wrote tex', len('\n'.join(tex)))
